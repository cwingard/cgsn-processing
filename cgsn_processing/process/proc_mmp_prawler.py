#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_mmp_prawler
@file cgsn_processing/process/proc_mmp_prawler.py
@author Paul Whelan
@brief Creates a NetCDF dataset for the Prawler MMP data from the JSON formatted data
"""
import numpy as np
import os
import json
import pandas as pd
import xarray as xr
from pathlib import Path
from gsw import z_from_p

from cgsn_processing.process.common import ENCODING, inputs, epoch_time, json2df, update_dataset
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_mmp_prawler import PRAWLER, PRAWLER_SCI

def read_json(infile):
    """
    Reads a json file into a dictionary, which gets returned.
    If file nonexistent or empty, return NONE.
    """
    
    jf = Path(infile)
    if not jf.is_file():
        # if not, return an empty data frame
        print("JSON data file {0} was not found, returning empty data frame".format(infile))
        return None
    
    else:
        # otherwise, read in the data file
        with open(infile) as jf:
            try:
                json_data = json.load(jf)
            except JSONDecodeError:
                print("Invalid JSON syntax in {0} found".format(infile))
                return None

    return json_data
            

def proc_mmp_prawler(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the McLane Prawler MMP sensor. Loads the JSON
    formatted parsed data and applies appropriate calibration coefficients to
    convert the raw parsed data into engineering units. 

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return prawler: An xarray dataset with the processed Prawler data
    """

    # load the json from file. If valid, make a dataframe from the
    # science profile data within the json dictionary
    
    prawler_json = read_json(infile)
    if prawler_json is None:
        print("Processing of Prawler MMP file {0} aborted".format(infile))
        return None
    
    # replace epoch_time with time
    prawler_json['scidata'][ 'time'] = prawler_json['scidata'].pop( 'epoch_time')

    # create a Pandas dataframe from the science profiles within the prawler data

    prawler_df = pd.DataFrame( prawler_json["scidata"] )
    if prawler_df.empty:
        print("No science profiles found in file {0}".format(infile))
        
    # rename the epoch time column to time

    prawler_df['time'] = pd.to_datetime(prawler_df['time'], unit='s')
    prawler_df.index = prawler_df['time']

    # add the deployment id, used to subset data sets
    prawler_df['deploy_id'] = deployment

    # calculate depth from pressure
    prawler_df['depth'] = z_from_p( prawler_df['pressure'], lat)  # keep for compat w/ early data ingests

    # add the summary data fields as singleton values in the science profile data frame

    #for key in prawler_json["summarydata"]:
    #    prawler_df[ key ] = prawler_json["summarydata"][key][0]

    prawler_xr = xr.Dataset.from_dataframe( prawler_df )

    prawler_xr = update_dataset(prawler_xr, platform, deployment, lat, lon, [depth, depth, depth], PRAWLER)

    prawler_xr.attrs['processing_level'] = 'processed'

    # add back some of the useful prawler summary data fields as attributes
    prawler_xr.attrs['prawler_id'] = prawler_json['summarydata']['ID'][0]
    prawler_xr.attrs['serial_no'] = prawler_json['summarydata']['serial_number'][0]

    return prawler_xr


def main(argv=None):
    """
    Command line function to process the Prawler MMP data using the proc_mmp_prawler
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


    # process the science profile data and save the results to disk
    prawler = proc_mmp_prawler(infile, platform, deployment, lat, lon, depth)
    if prawler:
        prawler.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
