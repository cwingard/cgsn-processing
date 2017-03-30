#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_spkir
@file cgsn_processing/process/proc_spkir.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for SPKIR from JSON formatted source data
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
from cgsn_processing.process.configs.attr_spkir import SPKIR

def json2dataframe(j):
    # split channels
    j['raw_channel1'] = [cs[0] for cs in j['raw_channels']]
    j['raw_channel2'] = [cs[1] for cs in j['raw_channels']]
    j['raw_channel3'] = [cs[2] for cs in j['raw_channels']]
    j['raw_channel4'] = [cs[3] for cs in j['raw_channels']]
    j['raw_channel5'] = [cs[4] for cs in j['raw_channels']]
    j['raw_channel6'] = [cs[5] for cs in j['raw_channels']]
    j['raw_channel7'] = [cs[6] for cs in j['raw_channels']]
    del j['raw_channels']

    # convert time to datetime
    j['time'] = [datetime.datetime.utcfromtimestamp(u) for u in j['time']]

    return pd.DataFrame(j)
    
def json2netcdf(json_path, netcdf_path, lat=0., lon=0., depth=7.0, platform='', deployment=''):
    with open(json_path) as fin:
        j = json.load(fin)

    df = json2dataframe(j)

    df = df2omtdf(df, lat, lon, depth)
    
    attrs = SPKIR
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
