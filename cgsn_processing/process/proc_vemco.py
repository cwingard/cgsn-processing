#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_vemco
@file cgsn_processing/process/proc_vemco.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the VEMCO data from the JSON formatted data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, json2obj, json_obj2df, update_dataset
from cgsn_processing.process.configs.attr_vemco import VEMCO


def proc_vemco(infile, platform, deployment, lat, lon, depth):
    """
    Processing function for the Vemco VR2C Acoustic Fish Tag Receiver. Loads
    the JSON formatted parsed data and the dataset processing level attribute
    is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return status: An xarray dataset with the processed VR2C status data
    :return tags: An xarray dataset with the processed VR2C tag detections
    """
    # load the json data file as a hierarchical dictionary for further processing
    vemco = json2obj(infile)
    if not vemco:
        # json data file was empty, exiting
        return None, None

    # rename the VR2C Date and Time variable and calculate the clock offset (used to track the VR2C clock drift)
    x = vemco['status'].pop('vr2c_date_time', None)
    vemco['status']['sensor_time'] = x
    vemco['status']['clock_offset'] = [vemco['status']['time'][i] - x[i] for i in range(len(x))]

    # create the status data set and update the metadata attributes
    status = json_obj2df(vemco, 'status')
    status = xr.Dataset.from_dataframe(status)
    status['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(status.time)).astype(str))
    status = update_dataset(status, platform, deployment, lat, lon, [depth, depth, depth], VEMCO)
    status.attrs['processing_level'] = 'parsed'

    # now do the same for the tag messages, if they are present
    tags = None  # we always have status messages, but we won't always have tag detections
    if vemco['tags']['time']:
        # create the tags data set and update the metadata attributes
        tags = json_obj2df(vemco, 'tags')
        tags = xr.Dataset.from_dataframe(tags)
        tags['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(tags.time)).astype(str))
        tags = update_dataset(tags, platform, deployment, lat, lon, [depth, depth, depth], VEMCO)
        tags.attrs['processing_level'] = 'parsed'

    # return the processed data
    return status, tags


def main(argv=None):
    """
    Command line function to process the VEMCO data using the proc_vemco
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

    # process the VEMCO data and save the results to disk
    status, tags = proc_vemco(infile, platform, deployment, lat, lon, depth)
    if status is not None:
        status.to_netcdf(outfile.replace('.nc', '_status.nc'), mode='w', format='NETCDF4',
                         engine='netcdf4', encoding=ENCODING)

    if tags is not None:
        tags.to_netcdf(outfile.replace('.nc', '_tags.nc'), mode='w', format='NETCDF4',
                       engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
