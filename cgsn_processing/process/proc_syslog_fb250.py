#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_syslog_fb250
@file cgsn_processing/process/proc_syslog_fb250.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for FB250 from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_syslog_fb250 import FB250 
from cgsn_processing.process.configs.attr_common import SHARED


def proc_fbb(infile, platform, deployment, lat, lon, depth):
    """
    Main Fleet Broadband processing function. Loads the JSON formatted parsed
    data and converts data into a NetCDF data file using xarray. Dataset
    processing level attribute is set to "parsed". There is no processing of
    the data, just a straight conversion from JSON to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return: A xarray dataset with the FB250 data
    """
    # load the json data file and return a panda dataframe, adding a default depth and the deployment ID
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some data
    df.drop(columns=['date_time_string'], inplace=True)  # used to calculate time, so redundant

    # rename the latitude and longitude columns to avoid conflicts with NetCDF coordinate variables of the
    # same name. follows the CF Metadata convention of using precise_lat/precise_lon to distinguish
    # between the surveyed, nominal position of the mooring compared to the actual measured position.
    df.rename(columns={'latitude': 'precise_lat', 'longitude': 'precise_lon'}, inplace=True)

    # create an xarray data set from the data frame
    fbb = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    fbb['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(fbb.time)).astype(str))
    attrs = dict_update(FB250, SHARED)
    fbb = update_dataset(fbb, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    fbb.attrs['processing_level'] = 'parsed'

    return fbb


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
    fbb = proc_fbb(infile, platform, deployment, lat, lon, depth)
    if fbb:
        fbb.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
