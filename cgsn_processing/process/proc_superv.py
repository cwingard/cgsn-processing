#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_superv
@file cgsn_processing/process/proc_superv.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the CPM, DCL or STC Supervisor from JSON
    formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_superv import SUPERV
from cgsn_processing.process.configs.attr_common import SHARED


def proc_superv(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main supervisor processing function. Loads the JSON formatted parsed data
    and creates a NetCDF file for use in monitoring the mooring data logger
    system health. Dataset processing level attribute is set to "parsed".
    There is no processing of the data, just a straight conversion from JSON
    to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    **kwargs superv_type: Specify the source of the supervisor log file, either
        a CPM, DCL or STC.

    :return superv: An xarray dataset with the processed supervisor data
    """
    # get the supervisor type and force the string to lowercase if supplied
    superv_type = kwargs.get('superv_type')
    if superv_type and superv_type.lower() in ['cpm', 'dcl', 'stc']:
        superv_type = superv_type.lower()
    else:
        raise ValueError('The supervisor type must be a string set as either cpm, dcl, or stc (case insensitive).')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the date and time string variable.
    dt_str = superv_type + '_date_time_string'
    df.drop(columns=[dt_str], inplace=True)

    # convert the different hex strings (already converted to an integer in the parser) to unsigned integers
    for col in df.columns:
        if col in ['wake_code', 'ground_fault_enable', 'dcl_power_state',
                   'error_flags', 'error_flags1', 'error_flags2']:
            df[col] = df[col].astype(np.uintc)

    # create an xarray data set from the data frame
    superv = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    superv['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(superv.time)).astype(str))
    attrs = dict_update(SUPERV[superv_type], SUPERV['common'])
    attrs = dict_update(attrs, SHARED)
    superv = update_dataset(superv, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    superv.attrs['processing_level'] = 'parsed'

    return superv


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
    superv_type = args.switch

    # process the supervisor data and save the results to disk
    superv = proc_superv(infile, platform, deployment, lat, lon, depth, superv_type=superv_type)
    if superv:
        superv.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
