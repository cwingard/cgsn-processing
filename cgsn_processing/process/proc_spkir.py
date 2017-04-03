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

from cgsn_processing.process.common import inputs, json2df, df2omtdf, split_column
from cgsn_processing.process.configs.attr_spkir import SPKIR


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude

    # load the json data file and return a panda dataframe, adding a default depth and the deployment ID
    df = json2df(infile)
    df['depth'] = 7.0
    df['deploy_id'] = deployment

    # TODO: Add code to convert spectral irradiance values from counts to uE/m^2/s via pyseas (opt_functions)

    # convert the 7 spectral irradiance values from an array to singular values
    split_column(df, 'raw_channels', 7, singular='raw_channel')

    # convert the dataframe to a format suitable for the pocean OMTs
    df = df2omtdf(df, lat, lon, 7.0)

    # add to the global attributes for the SPKIR
    attrs = SPKIR
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    OMTs.from_dataframe(df, outfile, attributes=attrs)

if __name__ == '__main__':
    main()
