#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_lisst
@file cgsn_processing/process/proc_lisst.py
@author Samuel Dahlberg
@brief Creates a NetCDF dataset for the LISST data from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update, epoch_time
from cgsn_processing.process.configs.attr_lisst import LISST
from cgsn_processing.process.configs.attr_common import SHARED


def proc_lisst(infile, platform, deployment, lat, lon, depth):
    """
    LISST Particle Size Analyzer processor. Load the JSON formatted parsed
    data and converts data into a NetCDF data file using xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return lisst: xarray dataset with the particle data
    """

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # compare the instrument clock (from the transmission_date_string) to the GPS based DCL time stamp ('time')
    df['instrument_timestamp'] = [epoch_time(x) for x in df['instrument_timestamp']]
    df['clock_offset'] = (df['time'].values.astype(float) / 10 ** 9) - df['instrument_timestamp']

    # clean up the dataframe, getting rid of the time string variables we no longer need
    df.drop_vars(columns=['date_time_string'], inplace=True)

    # pop the 2d particle size data array out of the dataframe for manipulation
    particle_concentration = np.array(np.vstack(df.pop('lisst_volume_concentration')))

    # Create a list of the lower sizes, to use as a column
    lower_particle_size = [1.00, 1.48, 1.74, 2.05, 2.42, 2.86, 3.38, 3.98, 4.70, 5.55, 6.55, 7.72, 9.12, 10.8, 12.7,
                           15.0, 17.7, 20.9, 24.6, 29.1, 34.3, 40.5, 47.7, 56.3, 66.5, 78.4, 92.6, 109, 129, 152, 180,
                           212, 250, 297, 354, 420]

    # convert the 1D variables to a xarray data set
    ds = xr.Dataset.from_dataframe(df)

    particles = xr.Dataset({'lisst_volume_concentration': (['time', 'lower_particle_size'], particle_concentration)}
    , coords={'time': (['time'], pd.to_datetime(df.time, unit='s')), 'lower_particle_size': lower_particle_size})

    # create a xarray data set from the 1D and 2D data
    lisst = xr.merge([ds, particles])

    # grab the minimum and maximum recorded depth of the instrument
    depth_max = lisst.depth.max().values
    depth_min = lisst.depth.min().values

    # clean up the dataset and assign attributes
    lisst['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(lisst.time)).astype(str))
    attrs = dict_update(LISST, SHARED)  # add the shared attributes
    lisst = update_dataset(lisst, platform, deployment, lat, lon, [depth, depth_min, depth_max], attrs)
    lisst.attrs['processing_level'] = 'parsed'

    return lisst


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

    # process the LISST data and save the results to disk
    lisst = proc_lisst(infile, platform, deployment, lat, lon, depth)
    if lisst:
        lisst.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
