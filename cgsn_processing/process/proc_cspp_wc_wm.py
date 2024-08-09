#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_wc_wm
@file cgsn_processing/process/proc_cspp_wc_wm.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP winch motor data from JSON formatted source data
"""
import numpy as np
import os
import re
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_WINCH
from cgsn_processing.process.configs.attr_common import SHARED


def proc_cspp_wc_wm(infile, platform, deployment, lat, lon, depth):
    """
    CSPP winch controller status data from the winch motor. Loads the JSON
    formatted parsed data and converts data into a NetCDF data file using
    xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: site depth where the CSPP is deployed

    :return cspp_wc_wm: xarray dataset with the winch controller data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the suspect timestamp column, vendor isn't even certain what it is supposed to mean
    df.drop_vars(columns=['suspect_timestamp'], inplace=True)

    # create an xarray data set from the data frame
    wc_wm = xr.Dataset.from_dataframe(df)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub('\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # finalize the dataset and assign attributes
    wc_wm['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(wc_wm.time)).astype(str))
    wc_wm['profile_id'] = xr.Variable(('time',), np.repeat(profile_id, len(wc_wm.time)).astype(str))
    attrs = dict_update(CSPP_WINCH, CSPP)  # create the CSPP Winch Controller attributes
    attrs = dict_update(attrs, SHARED)  # add the shared attributes
    wc_wm = update_dataset(wc_wm, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    wc_wm.attrs['processing_level'] = 'parsed'

    return wc_wm


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

    # process the uCSPP Winch Controller winch motor status data and save the results to disk
    wc_wm = proc_cspp_wc_wm(infile, platform, deployment, lat, lon, depth)
    if wc_wm:
        wc_wm.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
