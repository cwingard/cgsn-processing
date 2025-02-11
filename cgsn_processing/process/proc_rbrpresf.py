#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_rbrpresf
@file cgsn_processing/process/proc_rbrpresf.py
@author Paul Whelan
@brief Creates a NetCDF dataset for the RBR Presf data from the JSON formatted data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, epoch_time, json2df, update_dataset
from cgsn_processing.process.configs.attr_rbrpresf import RBRQ3


def proc_rbrpresf(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the RBR Presf sensor. Loads the JSON
    formatted parsed data and applies appropriate calibration coefficients to
    convert the raw parsed data into engineering units. If no calibration
    coefficients are available, filled variables are returned and the dataset
    processing level attribute is set to "parsed". If the calibration,
    coefficients are available then the dataset processing level attribute is
    set to "processed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return rbrpxr: An xarray dataset with the processed RBRQ3 data
    """
    # load the json data file as a panda data frame for further processing
    rbrpf = json2df(infile)
    if rbrpf.empty:
        # json data file was empty, exiting
        return None

    rbrpf.drop(columns=['unix_date_time_ms', 'date_time_string'], inplace=True)

    # add the deployment id, used to subset data sets
    rbrpf['deploy_id'] = deployment

    # create an xarray data set from the data frame
    rbrpxr = xr.Dataset.from_dataframe(rbrpf)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    rbrpxr = update_dataset(rbrpxr, platform, deployment, lat, lon, [depth, depth, depth], RBRQ3)
    rbrpxr.attrs['processing_level'] = 'processed'
    return rbrpxr


def main(argv=None):
    """
    Command line function to process the RBR Presf data using the proc_rbrpresf
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

    # process the RBR Presf data and save the results to disk
    rbrp = proc_rbrpresf(infile, platform, deployment, lat, lon, depth)
    if rbrp:
        rbrp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
