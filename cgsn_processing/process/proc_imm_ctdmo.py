#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_imm_ctdmo
@file cgsn_processing/process/proc_imm_ctdmo.py
@author Christopher Wingard
@brief Creates NetCDF datasets for the CTD data from the Global Mooring inductive modem hosted instruments
"""
import datetime
import json
import numpy as np
import os
import pandas as pd
import xarray as xr
import re

from cgsn_processing.process.common import inputs, dict_update
from cgsn_processing.process.configs.attr_imm_ctdmo import CTDMO, STATUS, RAW, DERIVED
from pyseas.data.ctd_functions import ctd_density, ctd_pracsal, ctd_sbe37im_condwat, \
    ctd_sbe37im_preswat, ctd_sbe37im_tempwat

# correct some encoding inconsistencies between xarray and a CF compliant NetCDF file
ENCODING = {
    'time': {'_FillValue': False},
    'lat': {'_FillValue': False},
    'lon': {'_FillValue': False},
    'z': {'_FillValue': False},
    'station': {'dtype': np.int32}
}


def json_sub2df(data, sub):
    """
    Take a JSON formatted data object, read it in as a dict, pull out the subarray of interest, and return the results
    as a panda data frame.
    """
    df = pd.DataFrame(data[sub])
    if df.empty:
        return df

    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', drop=True, inplace=True)

    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

    return df


def update_dataset(ds, platform, deployment, lat, lon, depth, attrs):
    """

    :param ds:
    :param platform:
    :param deployment:
    :param lat:
    :param lon:
    :param depth:
    :param attrs:
    :return:
    """
    # add a default station identifier as a coordinate variable to the data set
    ds.coords['station'] = np.int32(0)
    ds = ds.expand_dims('station', axis=None)

    # add the geospatial coordinates using the station identifier from above as the dimension
    geo_coords = xr.Dataset({
        'lat': ('station', [lat]),
        'lon': ('station', [lon]),
        'z': ('station', [depth])
    }, coords={'station': [np.int32(0)]})

    # merge the geospatial coordinates into the data set
    ds = xr.merge([ds, geo_coords])

    # create a merged metadata attributes dictionary from the default dictionary and the data set specific dictionary
    attrs = dict_update(CTDMO, attrs)   # merge the attributes

    # update the global attributes with deployment specific details
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment)),
        'date_created': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00Z"),
        'geospatial_lat_max': lat,
        'geospatial_lat_min': lat,
        'geospatial_lon_max': lon,
        'geospatial_lon_min': lon,
        'geospatial_vertical_max': depth,
        'geospatial_vertical_min': depth,
        'geospatial_vertical_positive': 'down',
        'geospatial_vertical_units': 'm'
    })

    # assign the updated attributes to the global metadata and the individual variables
    ds.attrs = attrs['global']
    for v in ds.variables:
        if v not in ['time', 'lat', 'lon', 'z', 'station']:
            ds[v].attrs = dict_update(attrs[v], {'coordinates': 'time lat lon z'})
        else:
            ds[v].attrs = attrs[v]

    # return the data set for further work
    return ds


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

    # load the json data file
    with open(infile) as jf:
        data = json.load(jf)

    # create a dataset with the CTD status information
    df = json_sub2df(data, 'status')
    status = xr.Dataset.from_dataframe(df)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the dataset
    status = update_dataset(status, platform, deployment, lat, lon, depth, STATUS)

    # save the CTD status data
    status.to_netcdf(outfile, mode='a', format='NETCDF4', engine='netcdf4', encoding=ENCODING)

    # create a dataset with the raw CTD data
    df = json_sub2df(data, 'ctd')
    raw = xr.Dataset.from_dataframe(df)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the dataset
    raw = update_dataset(raw, platform, deployment, lat, lon, depth, RAW)

    # save the raw CTD data
    raw.to_netcdf(outfile, mode='a', format='NETCDF4', engine='netcdf4', encoding=ENCODING)

    # create a dataset with the processed CTD data
    time = df.index.values.astype(float) / 10.0 ** 9  # Convert from nanoseconds to seconds since 1970
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(time, unit='s')
    df.set_index('time', drop=True, inplace=True)
    df['deploy_id'] = deployment
    ctd = xr.Dataset.from_dataframe(df)

    # convert the raw measurements into scientific units
    ctd['conductivity'] = ctd_sbe37im_condwat(raw['raw_conductivity'])
    ctd['temperature'] = ctd_sbe37im_tempwat(raw['raw_temperature'])
    ctd['pressure'] = ctd_sbe37im_preswat(raw['raw_pressure'], status['pressure_range'])

    # derive salinity and density
    ctd['salinity'] = ctd_pracsal(ctd['conductivity'], ctd['temperature'], ctd['pressure'])
    ctd['rho'] = ctd_density(ctd['salinity'], ctd['temperature'], ctd['pressure'], lat, lon)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the dataset
    ctd = update_dataset(ctd, platform, deployment, lat, lon, depth, DERIVED)

    # save the converted and derived CTD data
    ctd.to_netcdf(outfile, mode='a', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
