#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_ctdpf
@file cgsn_processing/process/proc_cspp_ctdpf.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP CTDPF data from JSON formatted source data
"""
import numpy as np
import os
import re

from pocean.utils import dict_update
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTP
from gsw import z_from_p, SA_from_SP, CT_from_t, rho

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_CTDPF


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

    # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(df['salinity'], df['pressure'], lon, lat)   # absolute salinity
    ct = CT_from_t(sa, df['temperature'], df['pressure'])       # conservative temperature
    df['in_situ_density'] = rho(sa, ct, df['pressure'])         # in-situ density

    # setup some further parameters for use with the OMTP class
    df['deploy_id'] = deployment
    df['site_depth'] = site_depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['z'] = -1 * z_from_p(df['pressure'], lat)                    # uses CTD pressure record
    df['t'] = df['time'][0]                                         # set profile time to time of first data record
    df['precise_time'] = np.int64(df.pop('time')) * 10 ** -9        # rename time record
    df['station'] = 0

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    ctdpf_attr = CSPP

    ctdpf_attr['global'] = dict_update(ctdpf_attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    ctdpf_attr = dict_update(ctdpf_attr, CSPP_CTDPF)

    nc = OMTP.from_dataframe(df, outfile, attributes=ctdpf_attr)
    nc.close()

if __name__ == '__main__':
    main()
