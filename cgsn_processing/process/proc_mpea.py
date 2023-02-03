#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_mpea
@file cgsn_processing/process/proc_mpea.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the MPEA from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_mpea import MPEA
from cgsn_processing.process.configs.attr_common import SHARED


def proc_mpea(infile, platform, deployment, lat, lon, depth):
    """
    MFN Power Electronics Assembly (MPEA) processing function. Loads the JSON
    formatted parsed data and converts data into a NetCDF data file using
    xarray. Dataset processing level attribute is set to "parsed". There is no
    processing of the data, just a straight conversion from JSON to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return mpea: An xarray dataset with the mooring power system data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the date and time string variable.
    df.drop(columns=['dcl_date_time_string'], inplace=True)

    # While originally intended to provide power for AUV docks, that functionality of the CVT was never used. There
    # are multiple channels for which we have no data, and at this time never will. Dropping them to make a cleaner
    # data set.
    df.drop(columns=['cv3_state', 'cv3_voltage', 'cv3_current',
                     'cv4_state', 'cv4_voltage', 'cv4_current',
                     'cv5_state', 'cv5_voltage', 'cv5_current',
                     'cv6_state', 'cv6_voltage', 'cv6_current',
                     'cv7_state', 'cv7_voltage', 'cv7_current'], inplace=True)

    # convert the different hex strings (already converted to an integer in the parser) used for flags
    # to unsigned integers
    for col in df.columns:
        if col in ['error_flag1', 'error_flag2']:
            df[col] = df[col].astype(np.uintc)

    # create an xarray data set from the data frame
    mpea = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    mpea['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(mpea.time)).astype(str))
    attrs = dict_update(MPEA, SHARED)
    mpea = update_dataset(mpea, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    mpea.attrs['processing_level'] = 'parsed'

    return mpea


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

    # process the MFN power electronics assembly (MPEA) data and save the results to disk
    mpea = proc_mpea(infile, platform, deployment, lat, lon, depth)
    if mpea:
        mpea.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
