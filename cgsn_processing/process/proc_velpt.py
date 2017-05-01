#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_velpt
@file cgsn_processing/process/proc_velpt.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the buoy 3D accelerometer data 
"""
import numpy as np
import os
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json_sub2df
from cgsn_processing.process.configs.attr_velpt import VELPT


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = np.float(args.switch)  # utilize the switch option to set the deployment depth

    # load the json data file and return a panda dataframe
    df = json_sub2df(infile, 'velocity')
    df['depth'] = depth
    df['deploy_id'] = deployment

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Point Velocity Measurements from the Nortek Aquadopp',
        'summary': (
            'Records 3 minute ensemble averages every 15 minutes of point velocity from various points in the mooring'
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

        if c == 'date_time_array':
            #TODO: Add this parameter to the dataset
            # print("Skipping the '{}' for now".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(VELPT[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=VELPT[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
