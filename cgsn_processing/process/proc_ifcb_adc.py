#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_ifcb_adc
@file cgsn_processing/process/proc_ifcb_adc.py
@author Paul Whelan
@brief Creates a NetCDF dataset for IFCB ADC files from JSON formatted source data
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
from cgsn_processing.process.configs.attr_ifcb_adc import IFCB_ADC

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


def proc_ifcb_adc(infile, platform, deployment, lat, lon, depth) :
    """
    Main IFCB ADC processing function. Loads the JSON formatted parsed data. 
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
    adc_json = read_json(infile)
    if adc_json is None:
        print("Processing of IFCB ADC file {0} aborted".format(infile))
        return None

    df = pd.DataFrame( adc_json )
    #df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    df = df.apply( pd.to_numeric )

    # Create time variable from file name timestamp + image offset as unixtime UTC
    fname = os.path.basename(infile)
    dtstring = fname[1: fname.find('_')-1]
    dt = datetime.strptime( dtstring, '%Y%m%dT%H%M%S' )
    startfileUTC = dt.replace( tzinfo=timezone.utc ).timestamp()
    df.insert(0, 'time', df['ADCtime'] , True)
    df['time'] = pd.to_numeric( df['time'] ) + startfileUTC
    df.index = df['time']

    # Remove '#' from trigger column
    df = df.rename(columns={'trigger#': 'triggerNumber'})

    # create an xarray data set from the data frame
    df = xr.Dataset.from_dataframe(df)

    df['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(df.time)).astype(str))
    df = update_dataset(df, platform, deployment, lat, lon, [depth, depth, depth], IFCB_ADC)
    df.attrs['processing_level'] = 'processed'

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

    df = proc_ifcb_adc( infile, platform, deployment, lat, lon, depth )
    if df:
        df.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)
    
if __name__ == '__main__':
    main()
