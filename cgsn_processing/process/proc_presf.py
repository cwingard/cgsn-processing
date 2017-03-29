#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_presf
@file cgsn_processing/process/proc_presf.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for PRESF from JSON formatted source data
"""
import os
import json
import datetime
import re

import numpy as np
import pandas as pd

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_presf import PRESF

def json2netcdf(json_path, netcdf_path, lat=0., lon=0., platform='', deployment=''):
    df = json2df(json_path)

    df['y'] = lat
    df['x'] = lon
    df['z'] = 0
    df['station'] = 0
    df['t'] = df.pop('time')
    # convert all int64s to int32s
    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

    attrs = PRESF
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    OMTs.from_dataframe(df, netcdf_path, attributes=attrs)

def main():
    # load  the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude

    json2netcdf(infile, outfile, lat=lat, lon=lon, platform=platform, deployment=deployment)
    
if __name__ == '__main__':
    main()
