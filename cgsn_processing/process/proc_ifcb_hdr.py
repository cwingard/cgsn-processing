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

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs

from cgsn_processing.process.common import inputs, json2df, df2omtdf
from cgsn_processing.process.configs.attr_ifcb import IFCB


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

    # load the json data file and return a panda dataframe, adding a deployment depth and ID
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    df['depth'] = depth
    df['deploy_id'] = deployment

    # convert the dataframe to a format suitable for the pocean OMTs
    df = df2omtdf(df, lat, lon, depth)

    # add to the global attributes for the IFCB
    attrs = IFCB
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTs.from_dataframe(df, outfile, attributes=attrs)
    nc.close()
    
if __name__ == '__main__':
    main()
