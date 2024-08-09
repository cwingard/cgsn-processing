#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_syslog_irid
@file cgsn_processing/process/proc_syslog_irid.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for IRID from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_syslog_irid import IRID 
from cgsn_processing.process.configs.attr_common import SHARED


def proc_irid(infile, platform, deployment, lat, lon, depth):
    """
    Main Iridium processing function. Loads the JSON formatted parsed data and
    converts the data into a NetCDF file using xarray. Dataset processing level
    attribute is set to "parsed". There is no processing of the data, just a
    straight conversion from JSON to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return: A xarray dataset with the Iridium connection statistics data
    """
    # load the json data file and return a panda dataframe, adding a default depth and the deployment ID
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some data
    df.drop_vars(columns=['date_time_string'], inplace=True)  # used to calculate time, so redundant

    # create an xarray data set from the data frame
    irid = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    irid['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(irid.time)).astype(str))
    attrs = dict_update(IRID, SHARED)
    irid = update_dataset(irid, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    irid.attrs['processing_level'] = 'parsed'

    return irid


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

    # process the FB250 data and save the results to disk
    irid = proc_irid(infile, platform, deployment, lat, lon, depth)
    if irid:
        irid.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
