#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_flort
@file cgsn_processing/process/proc_cspp_flort.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP FLORT data from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import re
import xarray as xr

from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_FLORT
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_flort import Calibrations

from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


def proc_cspp_flort(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main FLORT processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the processing level attribute is set to "processed". Otherwise, filled
    variables are returned and the dataset processing level attribute is set
    to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed
    **serial_number: serial number of the FLORT instrument
    **ctd_name: Name of directory with data from a co-located CTD. This
        data will be used to apply temperature and salinity corrections to
        the optical backscatter data. Otherwise, the optical backscatter
        data is filled with NaN's

    :return flort: xarray dataset with the processed FLORT data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')
    serial_number = kwargs.get('serial_number')

    # load the json data file as a dataframe for further processing
    df = json2df(infile)
    if df.empty:
        # json data file was empty, exiting
        return None

    # remove the FLORT date/time string from the dataset
    df.drop(columns=['suspect_timestamp', 'flort_date_time_string'], inplace=True)

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'flort.cal_coeffs.json')
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
        csv_url = find_calibration('FLORT', str(serial_number), sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True

    # processed variables to be created if calibration coefficients and a co-located CTD are available
    empty_data = np.atleast_1d(df['serial_number']).astype(np.int32) * np.nan
    df['depth'] = empty_data
    df['ctd_pressure'] = empty_data
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data
    df['bback'] = empty_data

    if proc_flag:
        # Apply the scale and offset correction factors from the factory calibration coefficients
        df['estimated_chlorophyll'] = flo_scale_and_offset(df['raw_signal_chl'], dev.coeffs['dark_chla'],
                                                           dev.coeffs['scale_chla'])
        df['fluorometric_cdom'] = flo_scale_and_offset(df['raw_signal_cdom'], dev.coeffs['dark_cdom'],
                                                       dev.coeffs['scale_cdom'])
        df['beta_700'] = flo_scale_and_offset(df['raw_signal_beta'], dev.coeffs['dark_beta'],
                                              dev.coeffs['scale_beta'])

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    depth_range = [depth, 0.0, depth]  # default values for the global attributes
    ctd = pd.DataFrame()
    if ctd_name:
        ctd_file = re.sub('_TRIP', '_CTD', os.path.basename(infile))
        ctd_dir = re.sub('nutnr', 'ctdpf', os.path.dirname(infile))

        if os.path.isfile(os.path.join(ctd_dir, ctd_file)):
            ctd = json2df(os.path.join(ctd_dir, ctd_file))

    if not ctd.empty:
        # interpolate the CTD data into the profile
        pressure = np.interp(df['time'], ctd['time'], ctd['pressure'])
        df['ctd_pressure'] = pressure

        temperature = np.interp(df['time'], ctd['time'], ctd['temperature'])
        df['ctd_temperature'] = temperature

        salinity = np.interp(df['time'], ctd['time'], ctd['salinity'])
        df['ctd_salinity'] = salinity

        # calculate the depth range for the NetCDF global attributes: deployment depth and the profile min/max range
        df['depth'] = -1 * z_from_p(df['ctd_pressure'], lat)
        depth_range = [depth, df['depth'].min(), df['depth'].max()]

        # calculate the optical backscatter using the CTD temperature and salinity data
        df['bback'] = flo_bback_total(df['beta_700'], temperature, salinity, dev.coeffs['scatter_angle'],
                                      dev.coeffs['wavelength'], dev.coeffs['chi_factor'])

    # create an xarray data set from the data frame
    flort = xr.Dataset.from_dataframe(df)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    flort['deploy_id'] = xr.Variable('time', np.tile(deployment, len(flort.time)).astype(str))
    flort['profile_id'] = xr.Variable('time', np.tile(profile_id, len(flort.time)).astype(str))

    attrs = dict_update(CSPP_FLORT, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    flort = update_dataset(flort, platform, deployment, lat, lon, depth_range, attrs)
    if proc_flag:
        flort.attrs['processing_level'] = 'processed'
    else:
        flort.attrs['processing_level'] = 'partial'

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
    ctd_name = args.devfile  # name of co-located CTD
    serial = args.serial  # serial number of the FLORT instrument

    # process the FLORT data and save the results to disk
    flort = proc_cspp_flort(infile, platform, deployment, lat, lon, depth, ctd_name=ctd_name, serial_number=serial)
    if flort:
        flort.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
