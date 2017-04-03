#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_nutnr
@file cgsn_processing/process/proc_nutnr.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Nitrate concentration data from the NUTNR
"""
import numpy as np
import os
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_nutnr import NUTNR


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lng = args.longitude

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    df['depth'] = 7.0
    df['deploy_id'] = deployment

    # TODO: Add calculations for re-computing the nitrate concentrations from the channel measurements

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Nitrate Concentrations at 7 meters Depth',
        'summary': (
            'Records nitrate concentrations from the Satlantic ISUS Nitrate sensor at 7 meters depth'
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

    # create a new dimension for the channel measurements array
    nc.createDimension('channels', size=256)
    d = nc.createVariable('channels', 'i1', ('channels',))
    d[:] = np.arange(0, 256)

    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'latitude', 'longitude', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(NUTNR[c])
            d[:] = df[c].values
        elif c in ['deploy_id', 'measurement_type']:
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(NUTNR[c])
            d[:] = df[c].values
        elif c == 'channel_measurements':
            d = nc.createVariable(c, 'f', ('time', 'channels',))
            d.setncatts(NUTNR[c])
            d[:] = np.array(np.vstack(df[c].values), dtype='float32')
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=NUTNR[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
