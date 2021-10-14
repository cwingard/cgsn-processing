#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_metbk
@file cgsn_processing/process/proc_metbk.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the METBK from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from gsw import SP_from_C, SA_from_SP, CT_from_t, rho

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING
from cgsn_processing.process.configs.attr_metbk import METBK


def proc_metbk(infile, platform, deployment, lat, lon, depth):
    """
    Bulk meteorology processing function. Loads the JSON formatted parsed data
    and converts data into a NetCDF data file using xarray. Sea surface
    salinity and density are calculated using the TEOS-10 equations from the
    Gibbs Sea Water toolbox.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return metbk: An xarray dataset with the METBK data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some of the data
    df.drop(columns=['dcl_date_time_string'], inplace=True)  # used to calculate time, so redundant

    # calculate the practical salinity of the surface seawater from the temperature and conductivity measurements
    df['sea_surface_salinity'] = SP_from_C(df['sea_surface_conductivity'].values * 10,
                                           df['sea_surface_temperature'].values, 0)

    # calculate the in-situ density of the surface seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(df['psu'].values, 0.0, lon, lat)                   # absolute salinity
    ct = CT_from_t(sa, df['sea_surface_temperature'].values, 0.0)      # conservative temperature
    df['sea_surface_density'] = rho(sa, ct, 0.0)                                       # density

    # create an xarray data set from the data frame
    metbk = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    metbk['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(metbk.time)).astype(str))
    metbk = update_dataset(metbk, platform, deployment, lat, lon, [depth, depth, depth], METBK)
    metbk.attrs['processing_level'] = 'processed'

    return metbk

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

    # process the METBK data and save the results to disk
    metbk = proc_metbk(infile, platform, deployment, lat, lon, depth)
    if metbk:
        metbk.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
