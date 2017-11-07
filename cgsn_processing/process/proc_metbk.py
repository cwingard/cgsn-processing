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
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_metbk import METBK


def main(argv=None):
    # load  the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    
    # load the json data file and return a panda data frame
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    df['depth'] = 0.0       # default depth, will update for sensors below
    df['deploy_id'] = deployment

    # calculate the practical salinity of the surface seawater from the temperature and conductivity measurements
    df['psu'] = gsw.SP_from_C(df['sea_surface_conductivity'] * 10, df['sea_surface_temperature'], 0)
    # calculate the in-situ density of the surface seawater from the absolute salinity and conservative temperature
    sa = gsw.SA_from_SP(df['psu'], 0.0, lon, lat)                   # absolute salinity
    ct = gsw.CT_from_t(sa, df['sea_surface_temperature'], 0.0)      # conservative temperature
    df['rho'] = gsw.rho(sa, ct, 0.0)                                # density

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Bulk Meteorological (METBK) Measurements',
        'summary': (
            'Measures surface meteorology and provides the data required to compute '
            'air-sea fluxes of heat, freshwater, and momentum.'
        ),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    }

    ts = TimeSeries(
            output_directory=outpath,
            latitude=lat,
            longitude=lon,
            station_name=platform,
            global_attributes=global_attributes,
            times=df.time.values.astype(np.float) * 10**-9,
            verticals=df.depth.values,
            output_filename=outfile,
            vertical_positive='down')

    # add the data from the data frame and set the attributes
    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # add the met sensor altitudes as variables
    # depth of the METBK-CT sensor
    d = nc.createVariable('z_ct', 'f4')
    d.setncatts(METBK['z_ct'])
    d[:] = 1.366
    # altitude of the METBK-BPR sensor
    d = nc.createVariable('z_bpr', 'f4')
    d.setncatts(METBK['z_bpr'])
    d[:] = -4.065
    # altitude of the METBK-IRR sensors (LWR and SWR)
    d = nc.createVariable('z_irr', 'f4')
    d.setncatts(METBK['z_irr'])
    d[:] = -4.320
    # altitude of the METBK-PRC sensor
    d = nc.createVariable('z_prc', 'f4')
    d.setncatts(METBK['z_prc'])
    d[:] = -4.100
    # altitude of the METBK-RH sensor
    d = nc.createVariable('z_rh', 'f4')
    d.setncatts(METBK['z_rh'])
    d[:] = -4.255
    # altitude of the METBK-WND sensor
    d = nc.createVariable('z_wnd', 'f4')
    d.setncatts(METBK['z_wnd'])
    d[:] = -4.740

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(METBK[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(METBK[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=METBK[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
