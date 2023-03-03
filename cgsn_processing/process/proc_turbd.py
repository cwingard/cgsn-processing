#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_turbd
@file cgsn_processing/process/proc_turbd.py
@author Paul Whelan
@brief Creates a NetCDF dataset for the TURBD data from the JSON formatted data
"""
import numpy as np
import os
import xarray as xr

from gsw import SP_from_C, SA_from_SP, CT_from_t, rho

from cgsn_processing.process.common import ENCODING, inputs, epoch_time, json2df, update_dataset
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_turbd import TURBD


def proc_turbd(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the Seapoint Turbidity sensor. Loads the JSON
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

    :return turbd: An xarray dataset with the processed TURBD data
    """
    # process the variable length keyword arguments
    #ctd_type = kwargs.get('ctd_type')
    #if ctd_type:
    #    ctd_type = ctd_type.lower()
    #flort_serial = kwargs.get('flort_serial')


    # load the json data file as a panda data frame for further processing
    turbdf = json2df(infile)
    if turbdf.empty:
        # json data file was empty, exiting
        return None

    turbdf['sensor_time'] = epoch_time(turbdf['turbd_date_time_string'].values[0])
    turbdf.drop(columns=['turbd_date_time_string', 'dcl_date_time_string', 'turbd_units'], inplace=True)

    # add the deployment id, used to subset data sets
    turbdf['deploy_id'] = deployment

    # create an xarray data set from the data frame
    turbxr = xr.Dataset.from_dataframe(turbdf)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    turbxr = update_dataset(turbxr, platform, deployment, lat, lon, [depth, depth, depth], TURBD)
    turbxr.attrs['processing_level'] = 'processed'
    return turbxr

def main(argv=None):
    """
    Command line function to process the TURBD data using the proc_turbd
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
    turbd = proc_turbd(infile, platform, deployment, lat, lon, depth)
    if turbd:
        turbd.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
