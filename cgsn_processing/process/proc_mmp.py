#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_mmp
@file cgsn_processing/process/proc_mmp.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for the MMP from JSON formatted source data
"""
import os
import json
import datetime

import numpy as np
import pandas as pd

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs
from gsw import z_from_p

from cgsn_processing.process.common import inputs
from cgsn_processing.process.configs.attr_mmp import MMP, MMP_ADATA, MMP_CDATA, MMP_EDATA

from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries

def json2dataframes(j, lat=0.):
    # split adata "beams" into multiple columns
    adata = j['adata']
    adata['beams1'] = [b[1] for b in adata['beams']]
    adata['beams2'] = [b[2] for b in adata['beams']]
    adata['beams3'] = [b[3] for b in adata['beams']]
    adata['beams4'] = [b[4] for b in adata['beams']]
    adata['beams'] = [b[0] for b in adata['beams']]

    # convert to time-indexed dataframes
    
    def from_xdata(j):
        df = pd.DataFrame(j)
        df.index = [datetime.datetime.utcfromtimestamp(u) for u in df.time]
        # convert int64s to int32s
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)
        return df
    
    adata = from_xdata(j['adata'])
    cdata = from_xdata(j['cdata'])
    edata = from_xdata(j['edata'])

    # interpolate adata pressure from cdata
    adata['pressure'] = np.nan
    pressure = adata.pop('pressure')
    pressure = pressure.append(cdata.pressure)
    pressure.sort_index(inplace=True)
    ipressure = pressure.interpolate(method='time')[np.isnan(pressure)]
    adata['pressure'] = ipressure

    # convert pressure to depth
    def compute_depth(df):
        df['depth'] = [0 - z_from_p(p, lat) for p in df['pressure']]

    compute_depth(adata)
    compute_depth(cdata)
    compute_depth(edata)
                       
    # now store time indices in "time" columns
    adata['time'] = adata.index
    cdata['time'] = cdata.index
    edata['time'] = edata.index
    
    return {
        'adata': adata,
        'cdata': cdata,
        'edata': edata
    }
    
def json2netcdf(json_path, out_basepath, lat=0., lon=0.):
    out_basename, _ = os.path.splitext(out_basepath)
    
    with open(json_path) as fin:
        j = json.load(fin)

    dfs = json2dataframes(j)

    def massage_dataframe(df):
        df['y'] = lat
        df['x'] = lon
        # in the timeseries representation, there's one z per station
        # this will be fixed when using the profile representation
        df['z'] =  j['profile']['start_depth']
        df['station'] = 0
        df['t'] = df.pop('time')
        # convert all int64s to int32s
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)
        return df
    
    adf = massage_dataframe(dfs['adata'])
    out_path = '{}-adata.nc'.format(out_basepath)
    attrs = dict_update(MMP, MMP_ADATA)
    OMTs.from_dataframe(adf, out_path, attributes=attrs)

    cdf = massage_dataframe(dfs['cdata'])
    out_path = '{}-cdata.nc'.format(out_basepath)
    attrs = dict_update(MMP, MMP_CDATA)
    OMTs.from_dataframe(cdf, out_path, attributes=attrs)

    edf = massage_dataframe(dfs['edata'])
    out_path = '{}-edata.nc'.format(out_basepath)
    attrs = dict_update(MMP, MMP_EDATA)
    OMTs.from_dataframe(edf, out_path, attributes=attrs)

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

    json2netcdf(infile, out_basepath, lat=lat, lon=lon)
    
if __name__ == '__main__':
    main()
