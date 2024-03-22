#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_flort
@file cgsn_processing/process/proc_flort.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the FLORT from JSON formatted source data
ppw 02082024 - updated to support turbidity calculations, as follows:
Utilize the optional --switch parameter to support processing flort data to produce ONLY turbidity. 
Makes use of new calibration files being pushed to asset-management, having the naming scheme 
“CGINS-TURBDX-{s/n}__{date}.csv. These will live in a separate TURBDX subdirectory in asset 
management, per the CGSN data team. The value of the --switch flag should be “TURBDX” to compute 
turbidity; otherwise, standard FLORT outputs are calculated. The shell scripts for running 
processors or both parsers and processors have been updated accordingly.
"""
import numpy as np
import os
import pandas as pd
import re
import xarray as xr

from gsw import SP_from_C, p_from_z

from cgsn_processing.process.common import Coefficients, inputs, json2df, colocated_ctd, update_dataset, \
    ENCODING, dict_update
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_flort import FLORT
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the FLORT factory calibration coefficients for a unit. Values
        come from either a serialized object created per instrument and
        deployment (calibration coefficients do not change in the middle of a
        deployment), or from parsed CSV files maintained on GitHub by the OOI
        CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from an ECO Triplet (aka FLORT) device file already
        parsed and stored on GitHub as a CSV files. Note, the formatting of
        those files puts some constraints on this process. If someone has a
        cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # scale and offset correction factors
            if row.iloc[1] == 'CC_dark_counts_cdom':
                coeffs['dark_cdom'] = row.iloc[2]
            if row.iloc[1] == 'CC_scale_factor_cdom':
                coeffs['scale_cdom'] = row.iloc[2]

            if row.iloc[1] == 'CC_dark_counts_chlorophyll_a':
                coeffs['dark_chla'] = row.iloc[2]
            if row.iloc[1] == 'CC_scale_factor_chlorophyll_a':
                coeffs['scale_chla'] = row.iloc[2]

            if row.iloc[1] == 'CC_dark_counts_volume_scatter':
                coeffs['dark_beta'] = row.iloc[2]
            if row.iloc[1] == 'CC_scale_factor_volume_scatter':
                coeffs['scale_beta'] = row.iloc[2]

            # optical backscatter correction factors
            if row.iloc[1] == 'CC_angular_resolution':
                coeffs['chi_factor'] = row.iloc[2]
            if row.iloc[1] == 'CC_measurement_wavelength':
                coeffs['wavelength'] = row.iloc[2]
            if row.iloc[1] == 'CC_scattering_angle':
                coeffs['scatter_angle'] = row.iloc[2]

            # turbidity calculation factors
            if row.iloc[1] == 'CC_dark_counts_turbd':
                coeffs['dark_turbd'] = int(row.iloc[2])
            if row.iloc[1] == 'CC_scale_factor_turbd':
                coeffs['scale_turbd'] = float(row.iloc[2])

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_flort(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main FLORT processing function. Loads the JSON formatted, parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the dataset processing level attribute is set to "processed". Otherwise,
    filled variables are returned and the dataset processing level attribute
    is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on
    :param deployment: Name of the deployment for the input data file
    :param lat: Latitude of the mooring deployment
    :param lon: Longitude of the mooring deployment
    :param depth: Depth of the platform the instrument is mounted on

    :kwargs serial_number: The instrument serial number, used to find the
        calibration file from the GitHub hosted Asset Management database
    :kwargs ctd_name: Name of directory with data from a co-located CTD. This
        data will be used to calculate the optical backscatter, which
        requires the temperature and salinity data from the CTD. Otherwise,
        the optical backscatter is filled with NaN's
    :kwargs burst: Boolean flag to indicate whether to apply burst averaging
        to the data. Default is to not apply burst averaging

    :return flort: An xarray dataset with the processed FLORT data
    """
    # process the variable length keyword arguments
    serial_number = kwargs.get('serial_number')
    ctd_name = kwargs.get('ctd_name')
    burst = kwargs.get('burst')

    # load the json data file as a dictionary object for further processing
    flort = json2df(infile)
    if flort.empty:
        # json data file was empty, exiting
        return None

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'flort.cal_coeffs.json')
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # check for the source of the calibration coefficients and load accordingly
    if serial_number:
        if os.path.isfile(coeff_file):
            # we always want to use this file if it already exists
            dev.load_coeffs()
            proc_flag = True
        else:
            # load from the CI hosted CSV files
            sampling_time = flort['time'][0].value / 10.0 ** 9
            csv_url = find_calibration('FLORT', str(serial_number), sampling_time)
            if csv_url:
                dev.read_csv(csv_url)
                dev.save_coeffs()
                proc_flag = True

    # clean up dataframe and create an empty data variable
    flort.drop(columns=['dcl_date_time_string', 'flort_date_time_string'], inplace=True)
    empty_data = np.atleast_1d(flort['time']).astype(np.int32) * np.nan

    # processed variables to be created if a device file and a co-located CTD is available
    flort['estimated_chlorophyll'] = empty_data
    flort['fluorometric_cdom'] = empty_data
    flort['beta_700'] = empty_data
    flort['ctd_pressure'] = empty_data
    flort['ctd_temperature'] = empty_data
    flort['ctd_salinity'] = empty_data
    flort['bback'] = empty_data

    # use a default depth array for later metadata settings (will update if co-located CTD data is available)
    depth = [depth, depth, depth]

    # if the calibration coefficients are available, apply them.
    if proc_flag:
        # Apply the scale and offset correction factors from the factory calibration coefficients
        flort['estimated_chlorophyll'] = flo_scale_and_offset(flort['raw_signal_chl'], dev.coeffs['dark_chla'],
                                                              dev.coeffs['scale_chla'])
        flort['fluorometric_cdom'] = flo_scale_and_offset(flort['raw_signal_cdom'], dev.coeffs['dark_cdom'],
                                                          dev.coeffs['scale_cdom'])
        flort['beta_700'] = flo_scale_and_offset(flort['raw_signal_beta'], dev.coeffs['dark_beta'],
                                                 dev.coeffs['scale_beta'])

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if proc_flag and not ctd.empty:
        # set the CTD and FLORT time to the same units of seconds since 1970-01-01
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9
        flr_time = flort.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this FLORT file
        coverage = ctd_time.min() <= flr_time.min() and ctd_time.max() >= flr_time.max()

        # interpolate the CTD data if we have full coverage
        if coverage:
            # The Global moorings may use the data from the METBK-CT for FLORT mounted on the buoy
            # subsurface plate. We'll rename the data columns from the METBK to match other CTDs
            # and process accordingly.
            if re.match('metbk', ctd_name):
                # rename temperature and salinity
                ctd = ctd.rename(columns={
                    'sea_surface_temperature': 'temperature',
                    'sea_surface_conductivity': 'conductivity'
                })
                # set the depth in dbar from the measured depth in m below the water line.
                if re.match('metbk1', ctd_name):
                    ctd['pressure'] = p_from_z(-1.3661, lat)
                elif re.match('metbk2', ctd_name):
                    ctd['pressure'] = p_from_z(-1.2328, lat)
                else:  # default of 1.00 m
                    ctd['pressure'] = p_from_z(-1.0000, lat)

            pressure = np.interp(flort['time'], ctd['time'], ctd['pressure'])
            flort['ctd_pressure'] = pressure
            depth[1] = pressure.min()
            depth[2] = pressure.max()

            temperature = np.interp(flort['time'], ctd['time'], ctd['temperature'])
            flort['ctd_temperature'] = temperature

            salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
            salinity = np.interp(flort['time'], ctd['time'], salinity)
            flort['ctd_salinity'] = salinity

            # calculate the pressure and salinity corrected oxygen concentration
            flort['bback'] = flo_bback_total(flort['beta_700'], temperature, salinity,
                                             dev.coeffs['scatter_angle'], dev.coeffs['wavelength'],
                                             dev.coeffs['chi_factor'])

    # create an xarray data set from the data frame
    flort = xr.Dataset.from_dataframe(flort)

    # apply burst averaging if selected
    if burst:
        # resample to a 15-minute interval and shift the clock to center the averaging window
        flort = flort.resample(time='900s', base=3150, loffset='450s').median(dim='time', keep_attrs=True)

        # resampling will fill in missing time steps with NaNs. Use the raw_internal_temp variable
        # as a proxy variable to find cases where data is filled with a NaN, and delete those records.
        flort = flort.where(~np.isnan(flort.raw_internal_temp), drop=True)

        # reset original integer values
        int_arrays = ['measurement_wavelength_beta', 'raw_signal_beta', 'measurement_wavelength_chl',
                      'raw_signal_chl', 'measurement_wavelength_cdom', 'raw_signal_cdom', 'raw_internal_temp']
        for k in flort.variables:
            if k in int_arrays:
                flort[k] = flort[k].astype(np.intc)  # explicitly setting as a 32-bit integer

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    flort['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(flort.time)).astype(str))
    attrs = dict_update(FLORT, SHARED)
    flort = update_dataset(flort, platform, deployment, lat, lon, depth, attrs)
    if proc_flag:
        flort.attrs['processing_level'] = 'processed'
    else:
        flort.attrs['processing_level'] = 'parsed'

    return flort


def main(argv=None):
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth
    serial_number = args.serial
    ctd_name = args.devfile  # name of co-located CTD
    burst = args.burst

    flort = proc_flort(infile, platform, deployment, lat, lon, depth,
                       serial_number=serial_number, ctd_name=ctd_name, burst=burst)
    if flort:
        flort.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
