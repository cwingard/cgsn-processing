#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_mmp
@file cgsn_processing/process/proc_mmp_coastal.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for the MMP from JSON formatted source data
"""
import os
import json
import re

import numpy as np
import pandas as pd

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs
from gsw import z_from_p

from cgsn_processing.process.common import inputs
from cgsn_processing.process.configs.attr_mmp import MMP, MMP_ADATA, MMP_CDATA, MMP_EDATA


def json2dataframes(j, lat=0.):
    # convert to time-indexed dataframes
    def from_xdata(j):
        df = pd.DataFrame(j)
        df['time'] = pd.to_datetime(df.time, unit='s')
        df.index = df['time']

        # convert int64s to int32s
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)
        return df

    # convert pressure to depth
    def compute_depth(df):
        df['depth'] = [0 - z_from_p(p, lat) for p in df['pressure']]

    # create dataframes from the E and C data files
    cdata = from_xdata(j['cdata'])
    edata = from_xdata(j['edata'])

    # calculate the depth from the pressure records
    compute_depth(cdata)
    compute_depth(edata)

    # grab the A data, and if it actually exists, process it
    adata = j['adata']

    if adata:
        # split adata "beams" into multiple columns
        adata['beam1'] = [b[1] for b in adata['beams']]
        adata['beam2'] = [b[2] for b in adata['beams']]
        adata['beam3'] = [b[3] for b in adata['beams']]
        adata['beam4'] = [b[4] for b in adata['beams']]
        adata['beams'] = [b[0] for b in adata['beams']]

        # create a data frame for the A data
        adata = from_xdata(j['adata'])

        # interpolate adata pressure from cdata
        adata['pressure'] = np.nan
        pressure = adata.pop('pressure')
        pressure = pressure.append(cdata.pressure)
        pressure.sort_index(inplace=True)
        ipressure = pressure.interpolate(method='time')[np.isnan(pressure)]
        adata['pressure'] = ipressure

        # calculate the depth from the pressure record
        compute_depth(adata)
    else:
        adata = None

    return {
        'adata': adata,
        'cdata': cdata,
        'edata': edata
    }


def json2netcdf(json_path, out_basepath, lat=0., lon=0., platform='', deployment=''):
    out_basename, _ = os.path.splitext(out_basepath)
    
    with open(json_path) as fin:
        j = json.load(fin)

    dfs = json2dataframes(j, lat=lat)

    def massage_dataframe(df):
        df['y'] = lat
        df['x'] = lon
        df['profile_id'] = j['profile']['profile_id']
        # in the timeseries representation, there's one z per station
        # this will be fixed when using the profile representation
        df['z'] = j['profile']['start_depth']
        df['station'] = 0
        df['t'] = df.pop('time')
        # convert all int64s to int32s
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)
        return df

    shared_attrs = MMP
    shared_attrs['global'] = dict_update(shared_attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    def write_netcdf(key, attrs):
        df = massage_dataframe(dfs[key])
        out_path = '{}-{}.nc'.format(out_basepath, key)
        attrs = dict_update(shared_attrs, attrs)
        nc = OMTs.from_dataframe(df, out_path, attributes=attrs)
        nc.close()

    write_netcdf('cdata', MMP_CDATA)
    write_netcdf('edata', MMP_EDATA)
    if not dfs['adata'].empty:
        write_netcdf('adata', MMP_ADATA)


def main():
    # load  the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    out_basepath, _ = os.path.splitext(outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude

    json2netcdf(infile, out_basepath, lat=lat, lon=lon, platform=platform, deployment=deployment)
    
if __name__ == '__main__':
    main()
