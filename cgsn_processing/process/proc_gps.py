#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_gps
@file cgsn_processing/process/proc_gps.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the GPS data from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING
from cgsn_processing.process.configs.attr_gps import GPS


def proc_gps(infile, platform, deployment, lat, lon, depth):
    """
    Main GPS processing function. Loads the JSON formatted parsed data and
    converts data into a NetCDF data file using xarray. Dataset processing
    level attribute is set to "parsed". There is no processing of the
    data, just a straight conversion from JSON to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return gps: An xarray dataset with the GPS data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # rename the latitude and longitude columns to avoid conflicts with NetCDF coordinate variables of the
    # same name. follows the CF Metadata convention of using precise_lat/precise_lon to distinguish
    # between the surveyed, nominal position of the mooring compared to the actual measured position.
    df.rename(columns={'latitude': 'precise_lat', 'longitude': 'precise_lon'}, inplace=True)

    # clean up some of the data
    df.drop(columns=['date_time_string'], inplace=True)  # used to calculate time, so redundant

    # set the data types for the date, time latitude and longitude strings
    for col in df.columns:
        if col in ['longitude_string', 'latitude_string', 'gps_date_string', 'gps_time_string']:
            df[col] = df[col].astype('S12')

    # create an xarray data set from the data frame
    gps = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    gps['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(gps.time)).astype(str))
    gps = update_dataset(gps, platform, deployment, lat, lon, [depth, depth, depth], GPS)
    gps.attrs['processing_level'] = 'parsed'

    return gps

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

    # process the GPS data and save the results to disk
    gps = proc_gps(infile, platform, deployment, lat, lon, depth)
    if gps:
        gps.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
