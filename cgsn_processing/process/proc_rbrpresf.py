#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_rbrpresf
@file cgsn_processing/process/proc_rbrpresf.py
@author Paul Whelan
@brief Creates a NetCDF dataset for the RBR Presf data from the JSON formatted data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, json2df, dict_update, update_dataset
from cgsn_processing.process.configs.attr_rbrpresf import RBRQ3
from cgsn_processing.process.configs.attr_common import SHARED


def proc_rbrpresf(infile, platform, deployment, lat, lon, depth):
    """
    Processing function for the RBR PRESF sensor. Loads the JSON formatted
    parsed data and converts the data into a NetCDF data file using xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return rbrq3: An xarray dataset with the processed RBRQ3 data
    """
    # load the json data file as a panda data frame for further processing
    rbrpf = json2df(infile)
    if rbrpf.empty:
        # json data file was empty, exiting
        return None

    rbrpf.drop(columns=['unix_date_time_ms', 'date_time_string'], inplace=True)

    # create an xarray data set from the data frame
    rbrq3 = xr.Dataset.from_dataframe(rbrpf)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    rbrq3['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(rbrq3.time)).astype(str))
    attrs = dict_update(RBRQ3, SHARED)  # add the shared attributes
    rbrq3 = update_dataset(rbrq3, platform, deployment, lat, lon, [depth, depth, depth], RBRQ3)
    rbrq3.attrs['processing_level'] = 'processed'
    return rbrq3


def main(argv=None):
    """
    Command line function to process the RBR PRESF data using the proc_rbrpresf
    function. Command line arguments are parsed and passed to the function.

    :param argv: List of command line arguments
    """
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # process the RBR Q3 (PRESF) data and save the results to disk
    rbrq3 = proc_rbrpresf(infile, platform, deployment, lat, lon, depth)
    if rbrq3:
        rbrq3.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
