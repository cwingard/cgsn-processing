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
from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_DOSTA
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_dosta import Calibrations
from pyseas.data.do2_functions import do2_phase_to_doxy, do2_salinity_correction


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
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed
    **ctd_name: Name of directory with data from a co-located CTD. This
        data will be used to apply salinity and density corrections to the
        data. Otherwise, the salinity corrected oxygen concentration is
        filled with NaN's

    :return dosta: xarray dataset with the processed DOSTA data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')

    # load the json data file as a dataframe for further processing
    df = json2df(infile)
    if df.empty:
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
        sampling_time = df['time'][0].value / 10.0 ** 9
        csv_url = find_calibration('DOSTA', str(df['serial_number'][0]), sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True

    # clean up dataframe and rename selected variables
    df.drop_vars(columns=['suspect_timestamp'], inplace=True)
    df.rename(columns={
            'estimated_oxygen_concentration': 'oxygen_concentration',
            'estimated_oxygen_saturation': 'oxygen_saturation',
            'optode_temperature': 'optode_thermistor',
            'raw_temperature': 'raw_optode_thermistor',
        }, inplace=True)

    # processed variables to be created if calibration coefficients and a co-located CTD are available
    empty_data = np.atleast_1d(df['serial_number']).astype(np.int32) * np.nan
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data
    df['svu_oxygen_concentration'] = empty_data
    df['oxygen_concentration_corrected'] = empty_data

    # rename the depth to ctd_pressure and then calculate the depth range for the NetCDF global attributes:
    # deployment depth and the profile min/max range
    df['ctd_pressure'] = df['depth']
    df['depth'] = -1 * z_from_p(df['ctd_pressure'], lat)
    depth_range = [depth, df['depth'].min(), df['depth'].max()]

    # recompute the oxygen concentration from the calibrated phase, optode thermistor temperature and the calibration
    # coefficients
    if proc_flag:
        svu = do2_phase_to_doxy(df['calibrated_phase'], df['optode_thermistor'],
                                dev.coeffs['svu_cal_coeffs'], dev.coeffs['two_point_coeffs'])
        df['svu_oxygen_concentration'] = svu

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
        do_time = df.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this DOSTA file
        td = timedelta(minutes=5)
        coverage = ctd['time'].min() - td <= df['time'].min() and ctd['time'].max() + td >= df['time'].max()

        # interpolate the CTD data if we have full coverage
        if coverage:
            temperature = np.interp(do_time, ctd_time, ctd.temperature)
            df['ctd_temperature'] = temperature

            salinity = np.interp(do_time, ctd_time, ctd.salinity)
            df['ctd_salinity'] = salinity

            # calculate the pressure and salinity corrected oxygen concentration
            df['oxygen_concentration_corrected'] = do2_salinity_correction(df['svu_oxygen_concentration'].values,
                                                                           df['ctd_pressure'].values,
                                                                           df['ctd_temperature'].values,
                                                                           df['ctd_salinity'].values, lat, lon)

    # create an xarray data set from the data frame
    dosta = xr.Dataset.from_dataframe(df)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    dosta['deploy_id'] = xr.Variable('time', np.tile(deployment, len(dosta.time)).astype(str))
    dosta['profile_id'] = xr.Variable('time', np.tile(profile_id, len(dosta.time)).astype(str))

    attrs = dict_update(CSPP_DOSTA, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    dosta = update_dataset(dosta, platform, deployment, lat, lon, depth_range, attrs)
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
