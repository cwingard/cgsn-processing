#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_velpt
@file cgsn_processing/process/proc_velpt.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the buoy 3D accelerometer data 
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json_sub2df, update_dataset, dict_update, ENCODING
from cgsn_processing.process.configs.attr_velpt import VELPT
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.generic_functions import magnetic_declination, magnetic_correction


def proc_velpt(infile, platform, deployment, lat, lon, depth):
    """
    Main VELPT processing function. Loads the JSON formatted parsed data and
    converts data into a NetCDF data file using xarray.  The eastward and
    northward seawater velocities are corrected for magnetic declination
    based on the date, time, latitude and longitude.

    :param infile: JSON formatted parsed data file.
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return velpt: An xarray dataset with the VELPT data
    """
    # load the json data file and return a panda dataframe
    df = json_sub2df(infile, 'velocity')
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some the variables
    df.drop(columns='date_time_array', inplace=True)

    # correct the eastward and northward velocity components for magnetic declination
    theta = magnetic_declination(lat, lon, df['time'].values.astype(float) / 1e9)
    u_cor, v_cor = magnetic_correction(theta.mean(), df.velocity_east.values, df.velocity_north.values)

    # add the corrected velocities to the data frame
    df['eastward_seawater_velocity'] = u_cor / 1000
    df['northward_seawater_velocity'] = v_cor / 1000

    # create an xarray data set from the data frame
    velpt = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    velpt['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(velpt.time)).astype(str))
    attrs = dict_update(VELPT, SHARED)
    velpt = update_dataset(velpt, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    velpt.attrs['processing_level'] = 'processed'

    return velpt

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

    # process the VELPT data and save the results to disk
    velpt = proc_velpt(infile, platform, deployment, lat, lon, depth)
    if velpt:
        velpt.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
