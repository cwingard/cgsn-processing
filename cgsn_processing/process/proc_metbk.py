#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_metbk
@file cgsn_processing/process/proc_metbk.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the METBK from JSON formatted source data
"""
import gsw
import numpy as np
import os

from pyaxiom.netcdf.sensors import TimeSeries
from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_metbk import METBK


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
    
    # load the json data file and return a panda data frame
    df = json2df(infile)
    df['depth'] = 0.0       # default depth, will update for sensors below

    # calculate the practical salinity of the surface seawater from the temperature and conductivity measurements
    df['psu'] = gsw.SP_from_C(df['sea_surface_conductivity'] * 10.0, df['sea_surface_temperature'], 0.0)
    # calculate the in-situ density of the surface seawater from the absolute salinity and conservative temperature
    SA = gsw.SA_from_SP(df['psu'], 0.0, lng, lat)                   # absolute salinity
    CT = gsw.CT_from_t(SA, df['sea_surface_temperature'], 0.0)      # conservative temperature
    df['rho'] = gsw.rho(SA, CT, 0.0)

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'title': 'Bulk Meteorological (METBK) Measurements',
        'summary': (
            'Measures surface meteorology and provides the data required to compute '
            'air-sea fluxes of heat, freshwater, and momentum'
        ),
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org'
    }

    # create/open the netCDF file and set the global attributes and parameters
    ts = TimeSeries(
            output_directory=outdir,
            latitude=lat,
            longitude=lng,
            station_name=platform,
            global_attributes=global_attributes,
            times=df.time.values.astype(np.float) * 10**-9,
            verticals=df.depth.values,
            output_filename=outfile,
            vertical_positive='down')

    # add the met sensor heights as variables
    nc = ts._nc
    # depth of the METBK-CT sensor
    d = nc.createVariable('depth_ct', 'f4', ())
    d.setncatts(METBK['depth_ct'])
    d[:] = 1.25
    # height of the METBK-BPR sensor
    d = nc.createVariable('depth_bpr', 'f4', ())
    d.setncatts(METBK['depth_bpr'])
    d[:] = 3.00
    # height of the METBK-IRR sensors (LWR and SWR)
    d = nc.createVariable('depth_irr', 'f4', ())
    d.setncatts(METBK['depth_irr'])
    d[:] = 3.00
    # height of the METBK-PRC sensor
    d = nc.createVariable('depth_prc', 'f4', ())
    d.setncatts(METBK['depth_prc'])
    d[:] = 3.00
    # height of the METBK-RH sensor
    d = nc.createVariable('depth_rh', 'f4', ())
    d.setncatts(METBK['depth_rh'])
    d[:] = 3.00
    # height of the METBK-WND sensor
    d = nc.createVariable('depth_wnd', 'f4', ())
    d.setncatts(METBK['depth_wnd'])
    d[:] = 3.00

    # add the data from the dataframe and set the attributes
    for c in df.columns:
        if 'object' in df[c].dtype.name:
            if c == 'dcl_date_time_string':
                d = nc.createVariable(c, 'S23', ('time',))
                d.setncatts(METBK[c])
                d[:] = df[c].values.astype(np.str)
            continue
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue
        # print("Adding {}".format(c))
        ts.add_variable(c, df[c].values, attributes=METBK[c])

    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
