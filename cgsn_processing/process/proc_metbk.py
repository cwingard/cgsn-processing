#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_metbk
@file cgsn_processing/process/proc_metbk.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the METBK from JSON formatted source data
"""
import gsw
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

    # set depths for various sensors
    df['depth'] = 0.0
    df['depth_wnd'] = -3.0
    df['depth_bpr'] = -3.0
    df['depth_irr'] = -3.0
    df['depth_prc'] = -3.0
    df['depth_rh'] = -3.0
    df['depth_ct'] = 1.25

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
    ts = TimeSeries(
            output_directory=outdir,
            latitude=lat,
            longitude=lng,
            station_name=platform,
            global_attributes=global_attributes,
            times=df.time.values.astype(np.int64) // 10**9,
            verticals=df.depth.values,
            output_filename=outfile,
            vertical_positive='down')
    
    # create the NetCDF file
    df.columns.tolist()
    for c in df.columns:
        if c in ['time', 'lat', 'lon', 'depth']:
            print("Skipping axis '{}' (already in file)".format(c))
            continue
        if 'object' in df[c].dtype.name:
            print("Skipping object {}".format(c))
            continue
        print("Adding {}".format(c))
        ts.add_variable(c, df[c].values, attributes=METBK[c])

    ts._nc.close()

if __name__ == '__main__':
    main()
