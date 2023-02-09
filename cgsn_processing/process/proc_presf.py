#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_presf
@file cgsn_processing/process/proc_presf.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for PRESF from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update, epoch_time
from cgsn_processing.process.configs.attr_presf import PRESF
from cgsn_processing.process.configs.attr_common import SHARED


def proc_presf(infile, platform, deployment, lat, lon, depth):
    """
    Sea-Bird 26Plus Seafloor Pressure sensor processing function. Loads the
    JSON formatted parsed data and converts data into a NetCDF data file using
    xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return presf: An xarray dataset with the seafloor pressure data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up the dataframe, getting rid of variables we no longer need
    df['sensor_time'] = [epoch_time(x) for x in df['presf_date_time_string']]
    df.drop(columns=['presf_date_time_string', 'dcl_date_time_string'], inplace=True)

    # convert the absolute seafloor pressure from psi to dbar
    df['absolute_pressure'] = df['absolute_pressure'] * 0.689476

    # create an xarray data set from the data frame
    presf = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    presf['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(presf.time)).astype(str))
    attrs = dict_update(PRESF, SHARED)  # add the shared attributes
    presf = update_dataset(presf, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    presf.attrs['processing_level'] = 'processed'

    return presf


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

    # process the Sea-Bird 26Plus data and save the results to disk
    presf = proc_presf(infile, platform, deployment, lat, lon, depth)
    if presf:
        presf.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
