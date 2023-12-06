#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_presf
@file cgsn_processing/process/proc_presf.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for PRESF from JSON formatted source data
"""
import os
import re

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs

from cgsn_processing.process.common import inputs, json2df, df2omtdf
from cgsn_processing.process.configs.attr_presf import PRESF, RBRQ3
#from pyseas.data.sfl_functions import sfl_sflpres_rtime


def main(argv=None):

    # 11/21/2023 ppw - added support for input argument --switch "string"
    #                  to allow the presf processor to support multiple instrument types
    #                  If no switch passed, default to "presf" from SeaBird. A value
    #                  of "rbrq3" handles the RBR Quartz3 instrument.
    
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth
    
    instrument = args.switch
    if instrument is None:
        instrument = "presf"

    # load the json data file and return a panda dataframe, adding a deployment depth and ID
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    df['depth'] = depth
    df['deploy_id'] = deployment

    # convert the dataframe to a format suitable for the pocean OMTs
    df = df2omtdf(df, lat, lon, depth)

    if instrument == "presf":
        
        # TODO: Will require a fix to the WMM code before this can be implemented
        # convert the absolute (hydrostatic + atmospheric) pressure measurement from psi to dbar
        # df['seafloor_pressure'] = sfl_sflpres_rtime(df['absolute_pressure'])

        # add to the global attributes for the PRESF
        attrs = PRESF

    elif instrument == "rbrq3" :

        # add to the global attributes for the RBRQ3
        attrs = RBRQ3
        
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
       })
        
    nc = OMTs.from_dataframe(df, outfile, attributes=attrs)
    nc.close()
    
if __name__ == '__main__':
    main()
