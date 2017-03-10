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

from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries

from cgsn_processing.process.common import inputs
from cgsn_processing.process.configs.attr_mmp import MMP_ADATA, MMP_CDATA, MMP_EDATA

from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries

def json2dataframes(j):
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

    # now store time indices in "time" columns
    adata['time'] = adata.index
    cdata['time'] = cdata.index
    edata['time'] = edata.index
    
    return {
        'adata': adata,
        'cdata': cdata,
        'edata': edata
    }

class ADataTimeseries(OrthogonalMultidimensionalTimeseries):
    def nc_attributes(self):
        attrs = super(ADataTimeseries, self).nc_attributes()
        return dict_update(attrs, MMP_ADATA)
    
class CDataTimeseries(OrthogonalMultidimensionalTimeseries):
    def nc_attributes(self):
        attrs = super(CDataTimeseries, self).nc_attributes()
        return dict_update(attrs, MMP_CDATA)
    
class EDataTimeseries(OrthogonalMultidimensionalTimeseries):
    def nc_attributes(self):
        attrs = super(EDataTimeseries, self).nc_attributes()
        return dict_update(attrs, MMP_EDATA)
    
def json2netcdf(json_path, out_basepath, lat=0., lon=0.):
    out_basename, _ = os.path.splitext(out_basepath)
    
    with open(json_path) as fin:
        j = json.load(fin)

    dfs = json2dataframes(j)

    def massage_dataframe(df):
        df['y'] = lat
        df['x'] = lon
        df['z'] = 0. # FIXME compute depth
        df['station'] = 0 # FIXME use profile ID?
        df['t'] = df.pop('time')
        # convert all int64s to int32s
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)
        return df

    adf = massage_dataframe(dfs['adata'])
    out_path = '{}-adata.nc'.format(out_basepath)
    ADataTimeseries.from_dataframe(adf, out_path)

    cdf = massage_dataframe(dfs['cdata'])
    out_path = '{}-cdata.nc'.format(out_basepath)
    CDataTimeseries.from_dataframe(cdf, out_path)

    edf = massage_dataframe(dfs['edata'])
    out_path = '{}-edata.nc'.format(out_basepath)
    EDataTimeseries.from_dataframe(edf, out_path)

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
