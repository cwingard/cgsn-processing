#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_xeos
@file cgsn_processing/process/proc_xeos.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for Xeos Technologies GPS beacon data
    sent via Iridium SBD messaging from the JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_sbd import XEOS
from cgsn_processing.process.configs.attr_common import SHARED


def proc_xeos(infile, platform, deployment, lat, lon, depth):
    """
    Main processing function for Xeos beacon logs sent via the Iridium
    SBD messaging system. Loads the JSON formatted parsed data and
    creates a NetCDF file for use in monitoring the system health.
    Dataset processing level attribute is set to "parsed"; there is
    no processing of the data, just a straight conversion from JSON
    to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return xeos: An xarray dataset with the processed xeosisor data
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the date/time strings and transfer status string variables
    df.drop(columns=['date_time_email', 'transfer_status', 'date_time_xeos'], inplace=True)

    # rename the latitude and longitude variables to match the attribute file
    # convert the raw battery voltage and thermistor values from counts to V and degC, respectively
    df.rename(columns={'latitude': 'precise_latitude', 'longitude': 'precise_longitude',}, inplace=True)

    # create an xarray data set from the data frame
    xeos = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    xeos['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(xeos.time)).astype(str))
    attrs = dict_update(XEOS, SHARED)
    xeos = update_dataset(xeos, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    xeos.attrs['processing_level'] = 'parsed'

    return xeos


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

    # process the xeosisor data and save the results to disk
    xeos = proc_xeos(infile, platform, deployment, lat, lon, depth)
    if xeos:
        xeos.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
