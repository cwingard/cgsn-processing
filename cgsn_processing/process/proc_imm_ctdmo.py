#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_imm_ctdmo
@file cgsn_processing/process/proc_imm_ctdmo.py
@author Christopher Wingard
@brief Creates NetCDF datasets for the CTDMO data from inductive modem hosted instruments on Global Surface Moorings.
"""
import os
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, dict_update, epoch_time, join_df, \
    json2obj, json_obj2df, update_dataset
from cgsn_processing.process.configs.attr_ctdmo import CTDMO, CTD
from gsw import SP_from_C, SA_from_SP, CT_from_t, rho


def main(argv=None):
    """
    :param argv:
    :return:
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

    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # create a data frame with the CTD status information
    status = json_obj2df(data, 'status')
    status['status_time'] = epoch_time(status['date_time_string'].values[0])
    status.drop(columns='date_time_string', inplace=True)
    prange = status['pressure_range'].values[0]  # extract the pressure range from the data frame

    # create a data frame with the raw CTD data
    ctd = json_obj2df(data, 'ctd')
    ctd.pop('ctd_time')  # ctd_time is duplicated by the time variable, remove as variable and use time

    # convert the raw measurements from counts to scientific units
    ctd['conductivity'] = ctd['raw_conductivity'] / 100000.0 - 0.5
    ctd['temperature'] = ctd['raw_temperature'] / 10000.0 - 10.0
    prange = (prange - 14.7) * 0.6894757     # convert the pressure range from absolute PSI to dbar
    ctd['pressure'] = ctd['raw_pressure'] * prange / (0.85 * 65536.0) - 0.05 * prange

    # derive salinity and in-situ density
    ctd['salinity'] = SP_from_C(ctd['conductivity'] * 10.0, ctd['temperature'], ctd['pressure'])
    sa = SA_from_SP(ctd['salinity'], ctd['pressure'], lon, lat)  # absolute salinity from practical salinity
    ct = CT_from_t(sa, ctd['temperature'], ctd['pressure'])      # conservative temperature
    ctd['density'] = rho(sa, ct, ctd['pressure'])                # in-situ density

    # join the status and ctd data together into a single data frame, keeping track of data types and fill values
    joined = join_df(ctd, status)

    # create a final data set with the raw and derived CTD data and merged status data
    ctd = xr.Dataset.from_dataframe(joined)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    attrs = dict_update(CTDMO, CTD)
    ctd = update_dataset(ctd, platform, deployment, lat, lon, [depth, depth, depth], attrs)

    # save the data
    ctd.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
