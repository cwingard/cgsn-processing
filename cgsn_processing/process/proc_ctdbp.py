#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_ctdbp
@file cgsn_processing/process/proc_ctdbp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the CTDBP data from the JSON formatted data
"""
import numpy as np
import os
import re

from gsw import z_from_p, SP_from_C, SA_from_SP, CT_from_t, rho
from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_ctdbp import CTDBP


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lng = args.longitude
    depth = args.depth

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    df['depth'] = depth
    df['deploy_id'] = deployment

    # calculate the practical salinity of the seawater from the temperature and conductivity measurements
    df['psu'] = SP_from_C(df['conductivity'] * 10.0, df['temperature'], df['pressure'])
    # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(df['psu'], df['pressure'], lng, lat)                 # absolute salinity
    ct = CT_from_t(sa, df['sea_surface_temperature'], df['pressure'])    # conservative temperature
    df['rho'] = rho(sa, ct, df['pressure'])                              # density

    # TODO: If CTD with attached FLORT, add code to convert raw counts to scientific units

    # Setup the global attributes for the NetCDF file and create a timeseries object
    global_attributes = {
        'title': 'CTD Data Records',
        'summary': (
            'Records the CTD data, plus any attached sensors for the Mooring NSIF and MFN platforms'
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
        longitude=lng,
        station_name=platform,
        global_attributes=global_attributes,
        times=df.time.values.astype(np.int64) * 10**-9,
        verticals=df.depth.values,
        output_filename=outfile,
        vertical_positive='down')

    # add the data from the data frame and set the attributes
    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'latitude', 'longitude', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c in ['dcl_date_time_string', 'ctd_date_time_string']:
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(CTDBP[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(CTDBP[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=CTDBP[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
