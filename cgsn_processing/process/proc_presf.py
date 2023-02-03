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

from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, epoch_time, update_dataset, dict_update, ENCODING
from cgsn_processing.process.configs.attr_presf import PRESF
from cgsn_processing.process.configs.attr_common import SHARED


def proc_presf(infile, platform, deployment, lat, lon, depth):
    """
    Main PRESF processing function. Loads the JSON formatted parsed data and
    converts data into a NetCDF data file using xarray. Dataset processing
    level attribute is set to "processed" with the absolute pressure reading
    converted from psi to dbar.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return presf: An xarray dataset with the PRESF data
    """
    # load the json data file and return a panda dataframe, adding a deployment depth and ID
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # rename pressure_temp, so I can stop hearing people complain about this variable name
    df.rename(columns={'pressure_temp': 'sensor_temperature'}, inplace=True)

    # clean up the time variables
    df['sensor_time'] = epoch_time(df['presf_date_time_string'].values[0])
    df.drop(columns=['dcl_date_time_string', 'presf_date_time_string'], inplace=True)

    # convert the absolute (hydrostatic + atmospheric) pressure measurement from psi to dbar
    df['seafloor_pressure'] = df['absolute_pressure'] * 0.689475728

    # reset the depth array from the pressure record (removing the standard atmospheric pressure)
    d = z_from_p(df['seafloor_pressure'] - 10.1325, lat)
    depth = [d.mean(), d.min(), d.max()]

    # create an xarray data set from the data frame
    presf = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    presf['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(presf.time)).astype(str))
    attrs = dict_update(PRESF, SHARED)
    presf = update_dataset(presf, platform, deployment, lat, lon, depth, attrs)
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

    # process the PRESF data and save the results to disk
    presf = proc_presf(infile, platform, deployment, lat, lon, depth)
    if presf:
        presf.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)

    
if __name__ == '__main__':
    main()
