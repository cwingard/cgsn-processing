#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_dosta
@file cgsn_processing/process/proc_cspp_dosta.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP DOSTA data from JSON formatted source data
"""
import numpy as np
import os
import re
import pandas as pd
import xarray as xr

from datetime import timedelta

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_DOSTA
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_dosta import Calibrations

from pyseas.data.do2_functions import do2_phase_to_doxy, do2_salinity_correction
from gsw import z_from_p


def proc_cspp_dosta(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main DOSTA processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the oxygen concentration is recalculated from the calibrated phase and
    thermistor temperature and the dataset processing level attribute is set
    to "processed". Otherwise, filled variables are returned and the dataset
    processing level attribute is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: name of the mooring the instrument is mounted on.
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the mooring deployment.
    :param lon: longitude of the mooring deployment.
    :param depth: site depth where the CSPP is deployed

    :kwargs ctd_name: Name of directory with data from a co-located CTD. This
           data will be used to apply salinity and density corrections to the
           data. Otherwise, the salinity corrected oxygen concentration is
           filled with NaN's

    :return dosta: An xarray dataset with the processed DOSTA data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')

    # load the json data file as a dictionary object for further processing
    dosta = json2df(infile)
    if dosta.empty:
        # json data file was empty, exiting
        return None

    # setup the instrument calibration data object
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
    dosta.drop(columns=['suspect_timestamp'], inplace=True)
    dosta.rename(columns={
            'depth': 'ctd_pressure',
            'estimated_oxygen_concentration': 'oxygen_concentration',
            'estimated_oxygen_saturation': 'oxygen_saturation',
            'optode_temperature': 'oxygen_thermistor_temperature',
            'temp_compensated_phase': 'compensated_phase',
            'raw_temperature': 'raw_oxygen_thermistor'
        }, inplace=True)

    # processed variables to be created if calibration coefficients and a co-located CTD are available
    empty_data = np.atleast_1d(dosta['serial_number']).astype(np.int32) * np.nan
    dosta['ctd_temperature'] = empty_data
    dosta['ctd_salinity'] = empty_data
    dosta['svu_oxygen_concentration'] = empty_data
    dosta['oxygen_concentration_corrected'] = empty_data

    # reset the depth array from the CTD pressure record
    d = -1 * z_from_p(dosta['ctd_pressure'], lat)
    dosta['ctd_depth'] = d
    depth = [depth, d.min(), d.max()]

    # recompute the oxygen concentration from the calibrated phase, optode thermistor temperature and the calibration
    # coefficients
    if proc_flag:
        svu = do2_phase_to_doxy(dosta['calibrated_phase'], dosta['oxygen_thermistor_temperature'],
                                dev.coeffs['svu_cal_coeffs'], dev.coeffs['two_point_coeffs'])
        dosta['svu_oxygen_concentration'] = svu

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    ctd = pd.DataFrame()
    if ctd_name:
        ctd_file = re.sub('_OPT', '_CTD', os.path.basename(infile))
        ctd_dir = re.sub('dosta', 'ctdpf', os.path.dirname(infile))

        if os.path.isfile(os.path.join(ctd_dir, ctd_file)):
            ctd = json2df(os.path.join(ctd_dir, ctd_file))

    if proc_flag and not ctd.empty:
        # set the CTD and DOSTA time to the same units of seconds since 1970-01-01
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9
        do_time = dosta.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this DOSTA file
        td = timedelta(minutes=5)
        coverage = ctd['time'].min() - td <= dosta['time'].min() and ctd['time'].max() + td >= dosta['time'].max()

        # interpolate the CTD data if we have full coverage
        if coverage:
            temperature = np.interp(do_time, ctd_time, ctd.temperature)
            dosta['ctd_temperature'] = temperature

            salinity = np.interp(do_time, ctd_time, ctd.salinity)
            dosta['ctd_salinity'] = salinity

            # calculate the pressure and salinity corrected oxygen concentration
            dosta['oxygen_concentration_corrected'] = do2_salinity_correction(dosta['svu_oxygen_concentration'].values,
                                                                              dosta['ctd_pressure'].values,
                                                                              dosta['ctd_temperature'].values,
                                                                              dosta['ctd_salinity'].values, lat, lon)

    # create an xarray data set from the data frame
    dosta = xr.Dataset.from_dataframe(dosta)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    dosta['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(dosta.time)).astype(str))
    profile_id = re.sub(r'\D+', '', os.path.basename(infile))
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    dosta['profile_id'] = xr.Variable(('time',), np.repeat(profile_id, len(dosta.time)).astype(str))

    attrs = dict_update(CSPP_DOSTA, CSPP)  # add the shared attributes
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

    # process the DOSTA data and save the results to disk
    dosta = proc_cspp_dosta(infile, platform, deployment, lat, lon, depth, ctd_name=ctd_name)
    if dosta:
        dosta.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
