#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_imm_ctdmo
@file cgsn_processing/process/proc_imm_ctdmo.py
@author Christopher Wingard
@brief Creates NetCDF datasets for the CTDMO data from inductive modem hosted instruments on Global Surface Moorings.
"""
import os
import warnings

import pandas as pd
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, dict_update, epoch_time, join_df, \
    json2obj, json_obj2df, update_dataset
from cgsn_processing.process.configs.attr_ctdmo import CTDMO
from cgsn_processing.process.configs.attr_common import SHARED
from gsw import SP_from_C, SA_from_SP, CT_from_t, rho


def proc_imm_ctdmo(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processes CTDMO data recorded via an inductive modem link.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return: ctdmo - xarray Dataset containing the processed CTDMO data
    """
    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # create a data frame with the CTD status information
    status = json_obj2df(data, 'status')
    status['status_time'] = epoch_time(status['date_time_string'].values[0])
    status.drop(columns='date_time_string', inplace=True)
    status.rename(columns={'main_battery': 'main_battery_voltage',
                           'lithium_battery': 'lithium_battery_voltage',
                           'memory_free': 'sample_slots_free'},
                  inplace=True)
    prange = status['pressure_range'].values[0]  # extract the pressure range from the data frame

    # create a data frame with the raw CTD data
    ctd = json_obj2df(data, 'ctd')
    del ctd['ctd_time']  # ctd_time is duplicated by the time variable, remove as variable and use time

    # check the CTD time against now
    m = ctd.index.to_pydatetime() < pd.Timestamp.now()
    ctd = ctd[m]
    if ctd.empty:
        warnings.warn('The CTD clock is incorrect, reading too far into the future.')
        return None

    # add the deployment id, used to subset data sets
    ctd['deploy_id'] = deployment

    # convert the raw measurements from counts to scientific units
    ctd['conductivity'] = ctd['raw_conductivity'] / 100000.0 - 0.5
    ctd['temperature'] = ctd['raw_temperature'] / 10000.0 - 10.0
    prange = (prange - 14.7) * 0.6894757     # convert the pressure range from absolute PSI to dbar
    ctd['pressure'] = ctd['raw_pressure'] * prange / (0.85 * 65536.0) - 0.05 * prange

    # derive salinity and in-situ density
    ctd['salinity'] = SP_from_C(ctd['conductivity'].values * 10.0, ctd['temperature'].values, ctd['pressure'].values)
    sa = SA_from_SP(ctd['salinity'].values, ctd['pressure'].values, lon, lat)  # absolute salinity from practical salinity
    ct = CT_from_t(sa, ctd['temperature'].values, ctd['pressure'].values)      # conservative temperature
    ctd['density'] = rho(sa, ct, ctd['pressure'].values)                # in-situ density

    # join the status and ctd data together into a single data frame, keeping track of data types and fill values
    joined = join_df(ctd, status)

    # create a final data set with the raw and derived CTD data and merged status data
    ctdmo = xr.Dataset.from_dataframe(joined)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    attrs = dict_update(CTDMO, SHARED)  # add the shared attributes
    ctdmo = update_dataset(ctdmo, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    ctdmo.attrs['processing_level'] = 'processed'
    return ctdmo


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

    # process the CTDMO data and save the results to disk
    ctdmo = proc_imm_ctdmo(infile, platform, deployment, lat, lon, depth)

    # save the data
    if ctdmo:
        ctd.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
