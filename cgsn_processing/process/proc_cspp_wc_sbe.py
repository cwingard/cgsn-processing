#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_wc_sbe
@file cgsn_processing/process/proc_cspp_wc_sbe.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP winch pressure sensor data from JSON formatted source data
"""
import numpy as np
import os
import re
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_WINCH
from cgsn_processing.process.configs.attr_common import SHARED


def proc_cspp_wc_sbe(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    CSPP winch controller data from the SBE 50 pressure sensor (pressure and
    profiler speed). Loads the JSON formatted parsed data and converts data
    into a NetCDF data file using xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    kwarg profile_id: use the profile_id to identify the source data in the output file.

    :return cspp_wc_sbe: xarray dataset with the winch controller data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the suspect timestamp column, vendor isn't even certain what it is supposed to mean
    df.drop(columns=['suspect_timestamp'], inplace=True)

    # create an xarray data set from the data frame
    wc_sbe = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    profile_id = kwargs.get('profile_id')

    wc_sbe['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(wc_sbe.time)).astype(str))
    wc_sbe['profile_id'] = xr.Variable(('time',), np.repeat(profile_id, len(wc_sbe.time)).astype(str))
    attrs = dict_update(CSPP_WINCH, CSPP)  # create the CSPP Winch Controller attributes
    attrs = dict_update(attrs, SHARED)  # add the shared attributes
    wc_sbe = update_dataset(wc_sbe, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    wc_sbe.attrs['processing_level'] = 'parsed'

    return wc_sbe


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

    # process the uCSPP Winch Controller pressure sensor data and save the results to disk
    _, file_name = os.path.split(outfile)
    profile_id = re.sub(r'\D+', '', file_name)
    wc_sbe = proc_cspp_wc_sbe(infile, platform, deployment, lat, lon, depth, profile_id=profile_id)
    if wc_sbe:
        wc_sbe.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
