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

from cgsn_processing.process.common import inputs
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
    
def json2netcdf(json_path, netcdf_path, lat=0., lon=0., platform='', deployment=''):
    with open(json_path) as fin:
        j = json.load(fin)

    df = json2dataframe(j)

    # massage dataframe for pocean
    df['y'] = lat
    df['x'] = lon
    df['z'] = 0
    df['station'] = 0
    df['t'] = df.pop('time')
    # convert all int64s to int32s
    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

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

    json2netcdf(infile, outfile, lat=lat, lon=lon, platform=platform, deployment=deployment)
    
if __name__ == '__main__':
    main()
