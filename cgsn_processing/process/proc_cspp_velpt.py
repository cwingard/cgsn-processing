#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_velpt
@file cgsn_processing/process/proc_cspp_velpt.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP VELPT data from JSON formatted source data
"""
import numpy as np
import os
import re
import xarray as xr

from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_VELPT
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.generic_functions import magnetic_declination, magnetic_correction


def proc_cspp_velpt(infile, platform, deployment, lat, lon, depth):
    """
    Main VELPT processing function. Loads the JSON formatted parsed data and
    creates a NetCDF dataset with the processed data, adding salinity and 
    density as derived data products.

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed

    :return velpt: xarray dataset with the processed VELPT data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up dataframe and rename selected variables
    df.drop_vars(columns=['suspect_timestamp'], inplace=True)  # not even the vendor knows what this is

    # rename the depth to ctd_pressure and then calculate the depth range for the NetCDF global attributes:
    # deployment depth and the profile min/max range
    df['ctd_pressure'] = df['depth']
    df['depth'] = -1 * z_from_p(df['ctd_pressure'], lat)
    depth_range = [depth, df['depth'].min(), df['depth'].max()]

    # correct the eastward and northward velocity components for magnetic declination
    theta = magnetic_declination(lat, lon, df['time'].values.astype(float) / 1e9)
    u_cor, v_cor = magnetic_correction(theta.mean(), df.velocity_east.values, df.velocity_north.values)

    # add the corrected velocities to the data frame
    df['eastward_seawater_velocity'] = u_cor
    df['northward_seawater_velocity'] = v_cor

    # create an xarray data set from the data frame
    velpt = xr.Dataset.from_dataframe(df)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    velpt['deploy_id'] = xr.Variable('time', np.tile(deployment, len(velpt.time)).astype(str))
    velpt['profile_id'] = xr.Variable('time', np.tile(profile_id, len(velpt.time)).astype(str))

    attrs = dict_update(CSPP_VELPT, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    velpt = update_dataset(velpt, platform, deployment, lat, lon, depth_range, attrs)
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
    velpt = proc_cspp_velpt(infile, platform, deployment, lat, lon, depth)
    if velpt:
        velpt.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
