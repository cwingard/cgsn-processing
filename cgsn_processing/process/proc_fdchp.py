#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_fdchp
@file cgsn_processing/process/proc_fdchp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the FDCHP from JSON formatted source data
"""
import numpy as np
import os
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.error_flags import derive_multi_flags
from cgsn_processing.process.configs.attr_fdchp import FDCHP


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

    df['depth'] = -4.81       # default altitude
    df['deploy_id'] = deployment

    # TODO: FDCHP produces a status flag. Need to find out what those values mean and calculate status variables
    # df = derive_multi_flags(FDCHPStatusFlag, 'status', df)

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Summarized Flux Direct Covariance Sensor Measurements',
        'summary': (
            'Records the hourly summarized flux direct covariance measurements from the FDCHP.'
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
            times=df.time.values.astype(float) * 10**-9,
            verticals=df.depth.values,
            output_filename=outfile,
            vertical_positive='down')

    # add the data from the data frame and set the attributes
    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(FDCHP[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(FDCHP[c])
            d[:] = df[c].values
        elif c == 'status':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(FDCHP[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=FDCHP[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
