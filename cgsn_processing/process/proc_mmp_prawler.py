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
from gsw import SP_from_C, z_from_p
from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total

from cgsn_processing.process.common import ENCODING, inputs, epoch_time, json2df, update_dataset
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_mmp_prawler import PRAWLER, PRAWLER_NO_FLORT, PRAWLER_SCI
from cgsn_processing.process.finding_calibrations import find_calibration, Calibrations

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
            

def proc_mmp_prawler(infile, platform, deployment, lat, lon, depth, coeff_file, serial):
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

    attrs = PRAWLER

    # Do not try to compute calculated fields if no fluorometer exists
    if 'flu_chl_count' in prawler_json['scidata'].keys():

        # If the prawler has a fluorometer, it should have a corresponding calibration coefficients file
        if coeff_file is not None:
            calib_prefix = "FLORT"
            dev = Calibrations(coeff_file)  # initialize calibration class
            if os.path.isfile(coeff_file):
                # we always want to use this file if it exists
                dev.load_coeffs()
            else:
            # load from the CI hosted CSV files
                csv_url = find_calibration(calib_prefix, serial, (prawler_df.time.values.astype('int64') * 10 ** -9)[0])
                if csv_url:
                    dev.read_csv(csv_url)
                    dev.save_coeffs()
                else:
                    print('A source for the FLORT calibration coefficients for {} could not be found'.format(infile))
                    return None

            prawler_df['estimated_chlorophyll'] = flo_scale_and_offset( 
                prawler_df['flu_chl_count'], dev.coeffs['dark_chla'], dev.coeffs['scale_chla'])
            
            prawler_df['fluorometric_cdom'] = flo_scale_and_offset(
                prawler_df['flu_cdom_count'], dev.coeffs['dark_cdom'], dev.coeffs['scale_cdom'])
            
            prawler_df['beta_700'] = flo_scale_and_offset(
                prawler_df['flu_beta_count'], dev.coeffs['dark_beta'], dev.coeffs['scale_beta'])
            
            # calculate the practical salinity of the seawater from the temperature, conductivity and
            # pressure measurements
            prawler_df['salinity'] = SP_from_C( prawler_df['conductivity'].values * 10.0, 
                                            prawler_df['temperature'].values, 
                                            prawler_df['pressure'].values)

            prawler_df['bback'] = flo_bback_total( prawler_df['beta_700'], 
                                                prawler_df['temperature'], 
                                                prawler_df['salinity'], 124., 700., 1.076)
            
    else:
        attrs = PRAWLER_NO_FLORT

    # calculate depth from pressure
    prawler_df['depth'] = z_from_p( prawler_df['pressure'], lat)  # keep for compat w/ early data ingests

    # Translate to xarray, add in attributes
    prawler_xr = xr.Dataset.from_dataframe( prawler_df )
    prawler_xr = update_dataset(prawler_xr, platform, deployment, lat, lon, [depth, depth, depth], attrs)
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
    coeff_file = args.coeff_file
    serial = args.serial

    # process the science profile data and save the results to disk
    prawler = proc_mmp_prawler(infile, platform, deployment, lat, lon, depth, coeff_file, serial)
    if prawler:
        prawler.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
