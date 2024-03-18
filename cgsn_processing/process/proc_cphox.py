#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cphox
@file cgsn_processing/process/proc_cphox.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Sea-Bird Electronics Deep SeapHOx V2
    data from the JSON formatted data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from calendar import timegm
from gsw import SA_from_SP, pt0_from_t, CT_from_pt, sigma0, z_from_p

from cgsn_processing.process.common import ENCODING, inputs, json2df, update_dataset
from cgsn_processing.process.configs.attr_cphox import CPHOX


def proc_cphox(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the Sea-Bird Electronics Deep SeapHOx (combined
    CTD, dissolved oxygen and pH sensor). Loads the JSON formatted parsed
    data and saves the data to a NetCDF file.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform relative to the sea surface.
    :return cphox: xarray dataset with the processed SeapHOx data
    """
    # load the json data file as a pandas data frame
    cphox = json2df(infile)
    if cphox.empty:
        # json data file was empty, exiting
        return None

    # convert SeapHOx date/time string to a pandas.Timestamp date/time object and then to a epoch time in seconds
    utc = pd.to_datetime(cphox['sphox_date_time_string'], format='%Y-%m-%dT%H:%M:%S', utc=True)
    epts = [timegm(t.timetuple()) for t in utc]  # calculate the epoch time as seconds since 1970-01-01 in UTC
    cphox['sensor_time'] = epts

    # drop the DCL date and time string, we no longer need it
    cphox = cphox.drop(columns=['dcl_date_time_string', 'sphox_date_time_string'])

    # reset the error code and serial number to integers
    cphox['error_flag'] = cphox['error_flag'].astype(int)
    cphox['serial_number'] = cphox['serial_number'].astype(int)

    # convert the oxygen concentration from ml/l to umol/L and then to umol/kg per the SBE63 manual
    SA = SA_from_SP(cphox['salinity'].values, cphox['pressure'].values, lon, lat)
    pt0 = pt0_from_t(SA, cphox['temperature'].values, cphox['pressure'].values)
    CT = CT_from_pt(SA, pt0)
    sigma = sigma0(SA, CT)
    cphox['oxygen_molar_concentration'] = cphox['oxygen_concentration'] * 44.6615  # convert to umol/L
    cphox['oxygen_concentration_per_kg'] = cphox['oxygen_concentration'] * 44660 / (sigma + 1000)  # convert to umol/kg
    cphox = cphox.drop(columns=['oxygen_concentration'])

    # replace the deployment depth with the actual depth from the pressure sensor
    depth = z_from_p(cphox['pressure'], lat)  # calculate the depth from the pressure
    darray = [depth.mean(), depth.min(), depth.max()]

    # create an xarray data set from the data frame
    cphox = xr.Dataset.from_dataframe(cphox)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    cphox['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(cphox.time)).astype(str))
    cphox = update_dataset(cphox, platform, deployment, lat, lon, darray, CPHOX)
    return cphox


def main(argv=None):
    """
    Command line function to process the SeapHOx data using the proc_cphox
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

    # process the CTDBP data and save the results to disk
    cphox = proc_cphox(infile, platform, deployment, lat, lon, depth)
    if cphox:
        cphox.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
