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

from cgsn_processing.process.common import inputs, json2df, df2omtdf
from cgsn_processing.process.configs.attr_presf import PRESF

def json2netcdf(json_path, netcdf_path, lat=0., lon=0., depth=0., platform='', deployment=''):
    df = json2df(json_path)
    df = df2omtdf(df, lat, lon, depth)
    df['depth'] = depth

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
    depth = args.depth

    json2netcdf(infile, outfile, lat=lat, lon=lon, depth=depth, platform=platform, deployment=deployment)
    
if __name__ == '__main__':
    main()
