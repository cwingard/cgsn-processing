#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_pco2a
@file cgsn_processing/process/proc_pco2a.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the PCO2A from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_pco2a import PCO2A
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.co2_functions import co2_ppressure


def proc_pco2a(infile, platform, deployment, lat, lon, depth):
    """
    Main PCO2A processing function. Loads the JSON formatted parsed data and
    converts data into a NetCDF data file using xarray.  Partial pressure of
    CO2 (uatm) in air or seawater is calculated from the CO2 mole fraction
    (ppm), the gas stream pressure (mbar) and standard atmospheric pressure set
    to a default of 1013.25 mbar/atm.

    :param infile: JSON formatted parsed data file.
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return pco2a: An xarray dataset with the PCO2A data.
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some of the data
    df.drop(['dcl_date_time_string', 'co2_date_time_string'], axis=1, inplace=True)

    # rename the CO2 measurement variable to remove the word "water" since it can be from either air or water, and
    # use the terminology from the vendor documentation.
    df.rename(columns={'measured_water_co2': 'co2_mole_fraction'}, inplace=True)

    # calculate the partial pressure of CO2 in the air and water samples
    df['pCO2'] = co2_ppressure(df['co2_mole_fraction'], df['gas_stream_pressure'])

    # create an xarray data set from the data frame
    pco2a = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    pco2a['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(pco2a.time)).astype(str))
    attrs = dict_update(PCO2A, SHARED)  # add the shared attributes
    pco2a = update_dataset(pco2a, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    pco2a.attrs['processing_level'] = 'processed'

    return pco2a

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

    # process the PCO2A data and save the results to disk
    pco2a = proc_pco2a(infile, platform, deployment, lat, lon, depth)
    if pco2a:
        pco2a.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
