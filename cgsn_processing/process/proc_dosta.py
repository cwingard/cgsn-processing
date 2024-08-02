#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_dosta
@file cgsn_processing/process/proc_dosta.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the dissolved oxygen from the JSON
    formatted source data
"""
import json
import numpy as np
import os
import pandas as pd
import xarray as xr

from datetime import timedelta

from cgsn_processing.process.common import Coefficients, inputs, json2df, colocated_ctd, update_dataset, \
    ENCODING, dict_update
from cgsn_processing.process.configs.attr_dosta import DOSTA
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.do2_functions import do2_phase_to_doxy, do2_salinity_correction
from gsw import SP_from_C, z_from_p


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the DOSTA factory and secondary 2-point calibration coefficients.
        Values come from either a serialized object created per instrument and
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
        Reads the values from a DOSTA calibration file already parsed and
        stored on GitHub as a CSV file. Note, the formatting of those files
        puts some constraints on this process. If someone has a cleaner method,
        I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # scale and offset correction factors from a two-point calibration
            if row[1] == 'CC_conc_coef':
                coeffs['two_point_coeffs'] = np.array(json.loads(row[2]))

            # Stern-Volmer-Uchida calibration coefficients from a multipoint factory calibration
            if row[1] == 'CC_csv':
                coeffs['svu_cal_coeffs'] = np.array(json.loads(row[2]))

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_dosta(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main DOSTA processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the oxygen concentration is recalculated from the calibrated phase and
    thermistor temperature and the dataset processing level attribute is set
    to "processed". Otherwise, filled variables are returned and the dataset
    processing level attribute is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    **kwargs ctd_name: Name of directory with data from a co-located CTD. This
        data will be used to apply salinity and density corrections to the
        data. Otherwise, the salinity corrected oxygen concentration is
        filled with NaN's
    **kwargs burst: Boolean flag to indicate whether to apply burst averaging
        to the data. Default is to not apply burst averaging.

    :return dosta: An xarray dataset with the processed DOSTA data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')
    burst = kwargs.get('burst')

    # load the json data file as a dictionary object for further processing
    dosta = json2df(infile)
    if dosta.empty:
        # json data file was empty, exiting
        return None

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'dosta.cal_coeffs.json')
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it already exists
        dev.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        sampling_time = dosta['time'][0].value / 10.0 ** 9
        csv_url = find_calibration('DOSTA', str(dosta['serial_number'][0]), sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True

    # clean up dataframe and rename selected variables
    dosta.drop(columns=['date_time_string'], inplace=True)
    empty_data = np.atleast_1d(dosta['serial_number']).astype(np.int32) * np.nan
    dosta.rename(columns={'estimated_oxygen_concentration': 'oxygen_concentration',
                          'estimated_oxygen_saturation': 'oxygen_saturation',
                          'optode_temperature': 'optode_thermistor',
                          'temp_compensated_phase': 'compensated_phase',
                          'raw_temperature': 'raw_optode_thermistor'}, inplace=True)

    # processed variables to be created if a device file and a co-located CTD is available
    dosta['svu_oxygen_concentration'] = empty_data
    dosta['oxygen_concentration_corrected'] = empty_data

    # use a default depth array for later metadata settings (will update if co-located CTD data is available)
    depth = [depth, depth, depth]

    # recompute the oxygen concentration from the calibrated phase, optode thermistor temperature and the calibration
    # coefficients
    if proc_flag:
        svu = do2_phase_to_doxy(dosta['calibrated_phase'], dosta['optode_thermistor'],
                                dev.coeffs['svu_cal_coeffs'], dev.coeffs['two_point_coeffs'])
        dosta['svu_oxygen_concentration'] = svu

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    dosta['ctd_pressure'] = empty_data
    dosta['ctd_temperature'] = empty_data
    dosta['ctd_salinity'] = empty_data
    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if proc_flag and not ctd.empty:
        # test to see if the CTD covers our time of interest for this DOSTA file
        td = timedelta(hours=1)
        coverage = ctd['time'].min() <= dosta['time'].min() and ctd['time'].max() + td >= dosta['time'].max()

        # interpolate the CTD data if we have full coverage
        if coverage:
            if ctd_name in ['metbk', 'metbk1', 'metbk2']:
                pressure = depth
                temperature = np.interp(dosta['time'], ctd['time'], ctd.sea_surface_temperature)
                salinity = SP_from_C(ctd.sea_surface_conductivity.values * 10.0, ctd.sea_surface_temperature.values,
                                     depth)
                salinity = np.interp(dosta['time'], ctd['time'], salinity)
            else:
                pressure = np.interp(dosta['time'], ctd['time'], ctd.pressure)
                temperature = np.interp(dosta['time'], ctd['time'], ctd.temperature)
                salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
                salinity = np.interp(dosta['time'], ctd['time'], salinity)

            dosta['ctd_pressure'] = pressure
            dosta['ctd_temperature'] = temperature
            dosta['ctd_salinity'] = salinity

            # calculate the pressure and salinity corrected oxygen concentration
            dosta['oxygen_concentration_corrected'] = do2_salinity_correction(dosta['svu_oxygen_concentration'].values,
                                                                              dosta['ctd_pressure'].values,
                                                                              dosta['ctd_temperature'].values,
                                                                              dosta['ctd_salinity'].values, lat, lon)

    # create an xarray data set from the data frame
    dosta = xr.Dataset.from_dataframe(dosta)

    # apply burst averaging if selected
    if burst:
        # resample to a 15-minute interval and shift the clock to make sure we capture the time "correctly"
        dosta = dosta.resample(time='900s', base=3150, loffset='450s').median(dim='time', keep_attrs=True)
        dosta = dosta.where(~np.isnan(dosta.serial_number), drop=True)

        # resample to a 15-minute interval and shift the clock to make sure we capture the time "correctly"
        dosta = dosta.resample(time='15Min', base=55, loffset='5Min').median(dim='time', keep_attrs=True)

        # reset original integer values
        int_arrays = ['product_number', 'serial_number']
        for k in dosta.variables:
            if k in int_arrays:
                dosta[k] = dosta[k].astype(np.intc)  # explicitly setting as a 32-bit integer

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    dosta['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(dosta.time)).astype(str))
    attrs = dict_update(DOSTA, SHARED)  # add the shared attributes
    dosta = update_dataset(dosta, platform, deployment, lat, lon, depth, attrs)
    if proc_flag:
        dosta.attrs['processing_level'] = 'processed'
    else:
        dosta.attrs['processing_level'] = 'partial'

    return dosta


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
    ctd_name = args.devfile  # name of co-located CTD
    burst = args.burst

    # process the CTDBP data and save the results to disk
    dosta = proc_dosta(infile, platform, deployment, lat, lon, depth, ctd_name=ctd_name, burst=burst)
    if dosta:
        dosta.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
