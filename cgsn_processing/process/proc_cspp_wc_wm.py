#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_wc_wm
@file cgsn_processing/process/proc_cspp_wc_wm.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP WINCH data from JSON formatted source data
"""
import os
import re

from gsw import z_from_p
from pocean.utils import dict_update
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTp

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_WINCH


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
    site_depth = args.depth

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # setup some further parameters for use with the OMTp class
    df['deploy_id'] = deployment
    df['site_depth'] = site_depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['z'] = -1 * z_from_p(df['depth'], lat)                   # uses CTD pressure record
    df['t'] = df.pop('time')[0]                                    # set profile time to time of first data record
    df['precise_time'] = df.t.values.astype('int64') / 1e9         # create a precise time record
    df['station'] = 0

    # clean-up duplicate depth values
    df.drop_duplicates(subset='z', keep='first', inplace=True)

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    attr = CSPP

    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    attr = dict_update(attr, CSPP_WINCH)

    nc = OMTp.from_dataframe(df, outfile, attributes=attr)
    nc.close()

if __name__ == '__main__':
    main()
