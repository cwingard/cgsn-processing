#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_superv_stc
@file cgsn_processing/process/proc_superv_stc.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the STC Supervisor from JSON formatted source data
"""
import numpy as np
import os
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df
#from cgsn_processing.process.error_flags import SupervErrorFlagSTC, derive_multi_flags
from cgsn_processing.process.configs.attr_superv_stc import SUPERV


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
    df['depth'] = 0.0
    df['deploy_id'] = deployment

    # convert the error flag strings to named variables.
    # TODO: Need to find where these values are defined.
    #df = derive_multi_flags(SupervErrorFlagSTC, 'error_flags1', df)
    #df = derive_multi_flags(SupervErrorFlagSTC, 'error_flags2', df)

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Mooring STC Supervisor Data',
        'summary': (
            'Measures the status of the STC, encompassing voltages, current draws, leak detects and the state of'
            'attached communication and logging devices.'
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
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'stc_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(SUPERV[c])
            d[:] = df[c].values
        elif c in ['error_flags1', 'error_flags2']:
                d = nc.createVariable(c, 'S23', ('time',))
                d.setncatts(SUPERV[c])
                d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(SUPERV[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=SUPERV[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
