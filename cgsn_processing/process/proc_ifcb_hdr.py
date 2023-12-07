#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_ifcb
@file cgsn_processing/process/proc_ifcb.py
@author Paul Whelan
@brief Creates a NetCDF dataset for IFCB from JSON formatted source data
"""
import os
import re
import numpy as np

from collections.abc import Mapping
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING
from cgsn_processing.process.configs.attr_ifcb import IFCB

def proc_ifcb(infile, platform, deployment, lat, lon, depth) :
    """
    Main IFCB processing function. Loads the JSON formatted parsed data. 
    Filled variables are returned and the dataset
    processing level attribute is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.


    :return df: An xarray dataset with the processed IFCB data
    """

    # load the json data file and return a panda dataframe, adding a deployment depth and ID
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # create an xarray data set from the data frame
    df = xr.Dataset.from_dataframe(df)

    df['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(df.time)).astype(str))
    df = update_dataset(df, platform, deployment, lat, lon, [depth, depth, depth], IFCB)
    df.attrs['processing_level'] = 'parsed'

    return df
    
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

    df = proc_ifcb( infile, platform, deployment, lat, lon, depth )
    if df:
        df.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)
    
if __name__ == '__main__':
    main()
