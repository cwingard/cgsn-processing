#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_dosta
@file cgsn_processing/process/proc_cspp_dosta.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP DOSTA data from JSON formatted source data
"""
import os
import re

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_DOSTA


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    _, fname = os.path.split(outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # setup some further parameters for use with the OMTs class
    df['deploy_id'] = deployment
    df['z'] = depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['t'] = df.pop('time')
    df['station'] = 0
    df.rename(columns={'depth': 'ctd_depth'}, inplace=True)

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    attr = CSPP

    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    attr = dict_update(attr, CSPP_DOSTA)

    nc = OMTs.from_dataframe(df, outfile, attributes=attr)
    nc.close()

if __name__ == '__main__':
    main()
