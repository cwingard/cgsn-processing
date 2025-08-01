#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_ctdpf
@file cgsn_processing/process/proc_cspp_ctdpf.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP CTDPF data from JSON formatted
    source data
"""
import numpy as np
import os
import re
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_CTDPF
from cgsn_processing.process.configs.attr_common import SHARED

from gsw import z_from_p, SP_from_C, CT_from_t, SA_from_SP, rho


def proc_cspp_ctdpf(infile, platform, deployment, lat, lon, depth):
    """
    Main CTDPF processing function. Loads the JSON formatted parsed data and
    creates a NetCDF dataset with the processed data, adding salinity and 
    density as derived data products.

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed

    :return ctdpf: xarray dataset with the processed CTDPF data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up dataframe and rename selected variables
    df.drop(columns=['suspect_timestamp'], inplace=True)  # not even the vendor knows what this is

    # re-calculate the practical salinity of the seawater from the temperature and conductivity measurements using
    # the Gibbs-SeaWater (GSW) Oceanographic Toolbox
    df['salinity'] = SP_from_C(df['conductivity'] * 10.0, df['temperature'], df['pressure'])

    # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(df['salinity'], df['pressure'], lon, lat)   # absolute salinity
    ct = CT_from_t(sa, df['temperature'], df['pressure'])       # conservative temperature
    df['density'] = rho(sa, ct, df['pressure'])                 # in-situ density

    # calculate the depth range for the NetCDF global attributes: deployment depth and the profile min/max range
    df['depth'] = -1 * z_from_p(df['pressure'], lat)
    depth_range = [depth, df['depth'].min(), df['depth'].max()]

    # create an xarray data set from the data frame
    ctdpf = xr.Dataset.from_dataframe(df)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    ctdpf['deploy_id'] = xr.Variable('time', np.tile(deployment, len(ctdpf.time)).astype(str))
    ctdpf['profile_id'] = xr.Variable('time', np.tile(profile_id, len(ctdpf.time)).astype(str))

    attrs = dict_update(CSPP_CTDPF, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    ctdpf = update_dataset(ctdpf, platform, deployment, lat, lon, depth_range, attrs)
    ctdpf.attrs['processing_level'] = 'processed'

    return ctdpf


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

    # process the CTDPF data and save the results to disk
    ctdpf = proc_cspp_ctdpf(infile, platform, deployment, lat, lon, depth)
    if ctdpf:
        ctdpf.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
