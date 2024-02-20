#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_co2pro
@file cgsn_processing/process/proc_co2pro.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Pro-Oceanus pCO2-Pro CV data from the
    JSON formatted data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, json2df, update_dataset
from cgsn_processing.process.configs.attr_co2pro import PCO2W


def proc_co2pro(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the Pro-Oceanus pCO2-Pro CV. Loads the JSON
    formatted parsed data and calculates the partial pressure of CO2 in the
    water samples (uatm). The data is then saved to a NetCDF file.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform relative to the sea surface.
    :return co2: xarray dataset with the processed pCO2-Pro CV data
    """
    # load the json data file as a pandas data frame
    co2 = json2df(infile)
    if co2.empty:
        # json data file was empty, exiting
        return None

    # drop the DCL date and time string, we no longer need it
    co2 = co2.drop(columns=['dcl_date_time_string'])

    # calculate the partial pressure of CO2 in the air and water samples
    co2['pCO2'] = co2['measured_water_co2'] * (co2['gas_stream_pressure'] / 1013.25)

    # create an xarray data set from the data frame
    co2 = xr.Dataset.from_dataframe(co2)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    co2['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(co2.time)).astype(str))
    co2 = update_dataset(co2, platform, deployment, lat, lon, [depth, depth, depth], PCO2W)
    return co2


def main(argv=None):
    """
    Command line function to process the CTDBP data using the proc_co2pro
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
    ctd_type = args.switch
    flort_serial = args.serial  # serial number of the FLORT

    # process the CTDBP data and save the results to disk
    co2 = proc_co2pro(infile, platform, deployment, lat, lon, depth)
    if co2:
        co2.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
