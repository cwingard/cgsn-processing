#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_flort
@file cgsn_processing/process/proc_flort.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the FLORT from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from gsw import SP_from_C, z_from_p

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
        self.coeffs = {}

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

    Updated 2024-02-08 (P. Whelan) to support turbidity calculations with
    further updates add 2024-07-19 (C. Wingard) to support the new TURBDX
    by adding those variables to the dataset rather than creating two
    separate datasets:

        Utilize the optional --switch parameter to support processing flort
        data to produce standard FLORT variables and turbidity. Makes use of
        new calibration files being pushed to asset-management, having the
        naming scheme “CGINS-TURBDX-{s/n}__{date}.csv". These will live in a
        separate TURBDX subdirectory in asset management, per the CGSN data
        team. The value of the --switch flag should be “TURBDX” to compute
        turbidity; otherwise, it will be ignored and only the standard FLORT
        outputs will be calculated.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on
    :param deployment: Name of the deployment for the input data file
    :param lat: Latitude of the mooring deployment
    :param lon: Longitude of the mooring deployment
    :param depth: Depth of the platform the instrument is mounted on

    **kwargs serial_number: The instrument serial number, used to find the
        calibration file from the GitHub hosted Asset Management database
    **kwargs ctd_name: Name of directory with data from a co-located CTD.
        Data will be used to calculate the optical backscatter, which
        requires the temperature and salinity data from the CTD. Otherwise,
        the optical backscatter is filled with NaN's
    **kwargs burst: Boolean flag to indicate whether to apply burst averaging
        to the data. Default is to not apply burst averaging
    **kwargs switch: Optional flag to indicate whether to process the FLORT
        data to produce ONLY turbidity. Default is to process the FLORT data
        to produce standard FLORT outputs.

    :return flort: An xarray dataset with the processed FLORT data
    """
    # process the variable length keyword arguments
    serial_number = kwargs.get('serial_number')
    ctd_name = kwargs.get('ctd_name')
    burst = kwargs.get('burst')
    switch = kwargs.get('switch')

    # load the json data file as a dictionary object for further processing
    df = json2df(infile)
    if df.empty:
        # json data file was empty, exiting
        return None

    # set up the instrument calibration data objects and flags
    coeff_flort = os.path.join(os.path.dirname(infile), 'flort.cal_coeffs.json')
    dev_flort = Calibrations(coeff_flort)  # initialize calibration class
    flort_flag = False

    coeff_turbd = os.path.join(os.path.dirname(infile), 'turbdx.cal_coeffs.json')
    dev_turbd = Calibrations(coeff_turbd)  # initialize calibration class
    turbd_flag = False

    # check for the source of the FLORT calibration coefficients and load accordingly
    if serial_number:
        if os.path.isfile(coeff_flort):
            # we always want to use this file if it already exists
            dev_flort.load_coeffs()
            flort_flag = True
        else:
            # load from the CI hosted CSV files
            sampling_time = df['time'][0].value / 10.0 ** 9
            csv_url = find_calibration('FLORT', str(serial_number), sampling_time)
            if csv_url:
                dev_flort.read_csv(csv_url)
                dev_flort.save_coeffs()
                flort_flag = True

        if switch == 'TURBDX':  # add the TURBDX variables to the dataset
            if os.path.isfile(coeff_turbd):
                # we always want to use this file if it already exists
                dev_turbd.load_coeffs()
                turbd_flag = True
            else:
                # load from the CI hosted CSV files
                sampling_time = df['time'][0].value / 10.0 ** 9
                csv_url = find_calibration('TURBDX', str(serial_number), sampling_time)
                if csv_url:
                    dev_turbd.read_csv(csv_url)
                    dev_turbd.save_coeffs()
                    turbd_flag = True

    # clean up dataframe and create an empty data variable
    df.drop(columns=['dcl_date_time_string', 'flort_date_time_string'], inplace=True)
    df = df.rename(columns={'raw_signal_beta': 'raw_backscatter',
                            'raw_signal_cdom': 'raw_cdom',
                            'raw_signal_chl': 'raw_chlorophyll'})
    empty_data = np.atleast_1d(df['time']).astype(np.int32) * np.nan

    # processed variables to be created if a device file and a co-located CTD is available
    df['estimated_chlorophyll'] = empty_data
    df['fluorometric_cdom'] = empty_data
    df['beta_700'] = empty_data
    df['ctd_pressure'] = empty_data
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data
    df['total_optical_backscatter'] = empty_data
    if switch == 'TURBDX':
        df['turbidity'] = empty_data

    # use a default depth array for later metadata settings (will update if co-located CTD data is available)
    depth_range = [depth, depth, depth]

    # if the calibration coefficients are available, apply them.
    if turbd_flag:
        # Apply the scale and offset correction factors from the factory calibration coefficients
        df['turbidity'] = flo_scale_and_offset(df['raw_backscatter'], dev_turbd.coeffs['dark_turbd'],
                                               dev_turbd.coeffs['scale_turbd'])

    if flort_flag:
        # Apply the scale and offset correction factors from the factory calibration coefficients
        df['estimated_chlorophyll'] = flo_scale_and_offset(df['raw_chlorophyll'], dev_flort.coeffs['dark_chla'],
                                                           dev_flort.coeffs['scale_chla'])
        df['fluorometric_cdom'] = flo_scale_and_offset(df['raw_cdom'], dev_flort.coeffs['dark_cdom'],
                                                       dev_flort.coeffs['scale_cdom'])
        df['beta_700'] = flo_scale_and_offset(df['raw_backscatter'], dev_flort.coeffs['dark_beta'],
                                              dev_flort.coeffs['scale_beta'])

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if not ctd.empty:
        # test to see if the CTD covers our time of interest for this DOSTA file
        td = pd.Timedelta('1h')
        coverage = ctd['time'].min() - td <= df['time'].min() and ctd['time'].max() + td >= df['time'].max()

        # interpolate the CTD data if we have full coverage
        if coverage:
            if ctd_name in ['metbk', 'metbk1', 'metbk2']:
                pressure = np.ones_like(ctd.time) * depth  # set the pressure to the depth of the FLORT
                temperature = np.interp(df['time'], ctd['time'], ctd.sea_surface_temperature)
                salinity = SP_from_C(ctd.sea_surface_conductivity.values * 10.0,
                                     ctd.sea_surface_temperature.values, depth)
                salinity = np.interp(df['time'], ctd['time'], salinity)
            else:
                pressure = np.interp(df['time'], ctd['time'], ctd.pressure)
                temperature = np.interp(df['time'], ctd['time'], ctd.temperature)
                salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
                salinity = np.interp(df['time'], ctd['time'], salinity)

            df['ctd_pressure'] = pressure
            df['ctd_temperature'] = temperature
            df['ctd_salinity'] = salinity

            # re-calculate the depth range for the metadata
            z = -1 * z_from_p(pressure, lat)
            depth_range = [depth, z.min(), z.max()]

            # calculate the pressure and salinity corrected oxygen concentration
            if flort_flag:
                df['total_optical_backscatter'] = flo_bback_total(df['beta_700'], temperature, salinity,
                                                                  dev_flort.coeffs['scatter_angle'],
                                                                  dev_flort.coeffs['wavelength'],
                                                                  dev_flort.coeffs['chi_factor'])

    # create an xarray data set from the data frame
    flort = xr.Dataset.from_dataframe(df)

    # apply burst averaging if selected
    if burst:
        # resample to a 15-minute interval and shift the clock to center the averaging window
        flort['time'] = flort.time + pd.Timedelta('450s')
        flort = flort.resample(time='900s').median(dim='time', keep_attrs=True)

        # resampling will fill in missing time steps with NaNs. Use the raw_internal_temp variable
        # as a proxy variable to find cases where data is filled with a NaN, and delete those records.
        flort = flort.where(~np.isnan(flort.raw_internal_temp), drop=True)

        # reset original integer values
        int_arrays = ['measurement_wavelength_beta', 'raw_backscatter', 'measurement_wavelength_chl',
                      'raw_chlorophyll', 'measurement_wavelength_cdom', 'raw_cdom', 'raw_internal_temp']
        for k in flort.variables:
            if k in int_arrays:
                flort[k] = flort[k].astype(np.intc)  # explicitly setting as a 32-bit integer

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    flort['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(flort.time)).astype(str))
    attrs = dict_update(FLORT, SHARED)
    flort = update_dataset(flort, platform, deployment, lat, lon, depth_range, attrs)
    if flort_flag or turbd_flag:
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
    burst = args.burst  # flag to indicate whether to apply burst averaging
    switch = args.switch  # flag to indicate whether to process the FLORT data to produce ONLY turbidity

    flort = proc_flort(infile, platform, deployment, lat, lon, depth, serial_number=serial_number, ctd_name=ctd_name,
                       burst=burst, switch=switch)
    if flort:
        flort.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
