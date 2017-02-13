#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@package cgsn_processing.process.proc_metbk
@file cgsn_processing/process/proc_metbk.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the METBK from JSON formatted source data
'''
import gsw
import numpy as np
import os
import pandas as pd

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df

def main():
    # load  the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    outdir = '/webdata/cgsn/data/erddap/' + platform + '/' + deployment + '/buoy/metbk'
    lat = args.latitude
    lng = args.longitude
    
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    df['time'] = pd.to_datetime(df.time, unit='s')
    df.index = df['time']
    
    # calculate the salinity of the surface seawater from the temperature and 
    # conductivity measurements
    df['psu'] = gsw.SP_from_C(df['sea_surface_conductivity'], df['sea_surface_temperature'], 1.5)
    
    # Setup the global attributes for the NetCDF file and create the NetCDF
    # timeseries object
    global_attributes = {
        'institution':'Ocean Observatories Initiative', 
        'title':'Bulk Meterological (METBK) Measurements',
        'summary':'Measures surface meteorology and provides the data required to compute air-sea fluxes of heat, freshwater, and momentum',
        'creator_name':'Christopher Wingard',
        'creator_email':'cwingard@coas.oregonstate.edu',
        'creator_url':'http://oceanobservatories.org'
    }

    ts = TimeSeries(
            output_directory = outdir,
            latitude = lat,
            longitude = lng,
            station_name = platform,
            global_attributes = global_attributes,
            times = df.time.values.astype(np.int64) // 10**9,
            verticals = 3.0,
            output_filename = outfile,
            vertical_positive = 'up')
    
    # create the NetCDF file
    df.columns.tolist();
    for c in df.columns:
        if c in ts._nc.variables:
            # print("Skipping '{}' (already in file)".format(c))
            continue
        if c in ['time', 'lat', 'lon', 'depth']: 
            # print("Skipping axis '{}' (already in file)".format(c))
            continue
        if 'object' in df[c].dtype.name: 
            # print("Skipping object {}".format(c))
            continue
        # print("Adding {}".format(c))
        ts.add_variable(c, df[c].values)

if __name__ == '__main__':
    main()
