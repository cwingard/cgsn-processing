#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_fdchp
@file cgsn_processing/process/proc_fdchp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the FDCHP from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_fdchp import FDCHP
from cgsn_processing.process.configs.attr_common import SHARED


def proc_fdchp(infile, platform, deployment, lat, lon, depth):
    """
    Main FDCHP processing function. Loads the JSON formatted parsed data and
    converts data into a NetCDF data file using xarray. Dataset processing
    level attribute is set to "parsed". There is no processing of the
    data, just a straight conversion from JSON to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return fdchp: An xarray dataset with the FDCHP data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some of the data
    df.drop(columns=['dcl_date_time_string'], inplace=True)  # used to calculate time, so redundant

    # create an xarray data set from the data frame
    fdchp = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    fdchp['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(fdchp.time)).astype(str))
    attrs = dict_update(FDCHP, SHARED)
    fdchp = update_dataset(fdchp, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    fdchp.attrs['processing_level'] = 'parsed'

    return fdchp

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

    # process the FDCHP data and save the results to disk
    fdchp = proc_fdchp(infile, platform, deployment, lat, lon, depth)
    if fdchp:
        fdchp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
