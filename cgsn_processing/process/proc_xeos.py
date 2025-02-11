#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_xeos
@file cgsn_processing/process/proc_xeos.py
@author Paul Whelan
@brief Creates a NetCDF dataset for XEOS messages from JSON formatted source data
"""
import os
from pathlib import Path
import json
import re
import numpy as np
from datetime import datetime, timezone
import pandas as pd
from collections.abc import Mapping
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING
from cgsn_processing.process.configs.attr_xeos import XEOS

def read_json(infile):
    """
    Reads a json file into a dictionary, which gets returned.
    If file nonexistent or empty, return NONE.
    """
    
    jf = Path(infile)
    if not jf.is_file():
        # if not, return an empty data frame
        print("JSON data file {0} was not found, returning empty data frame".format(infile))
        return None
    
    else:
        # otherwise, read in the data file
        with open(infile) as jf:
            try:
                json_data = json.load(jf)
            except JSONDecodeError:
                print("Invalid JSON syntax in {0} found".format(infile))
                return None

    return json_data


def proc_xeos(infile, platform, deployment, lat, lon, depth) :
    """
    Main XEOS processing function. Loads the JSON formatted parsed data. 
    Filled variables are returned and the dataset
    processing level attribute is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.


    :return df: An xarray dataset with the processed XEOS data
    """

    # load the json data file and return a panda dataframe, adding a deployment depth and ID
    df = json2df(infile)
    #xeos_json = read_json(infile)
    #if xeos_json is None:
    #    print("Processing of XEOS file {0} aborted".format(infile))
    #    return None

    #df = pd.DataFrame(xeos_json)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # Try adding deploy it to df (not working in ds)
    #df['deploy_id'] = deployment
    #df['time'] = pd.to_datetime( df['time'] )

    # create an xarray data set from the data frame
    ds = xr.Dataset.from_dataframe(df)

    ds['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(ds.time)).astype(str))
    ds = update_dataset(ds, platform, deployment, lat, lon, [depth, depth, depth], XEOS)
    ds.attrs['processing_level'] = 'processed'

    return ds
    
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

    df = proc_xeos( infile, platform, deployment, lat, lon, depth )
    if df:
        df.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)
    
if __name__ == '__main__':
    main()
