#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_pwrsys
@file cgsn_processing/process/proc_pwrsys.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the PWRSYS from JSON formatted source data
"""
import numpy as np
import os
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import hex2int, inputs, json2df
from cgsn_processing.process.error_flags import PwrsysOverrideFlag, PwrsysErrorFlag1, PwrsysErrorFlag2, \
    PwrsysErrorFlag3, derive_multi_flags
from cgsn_processing.process.configs.attr_pwrsys import PWRSYS


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

    # set an empty error flag variable
    ef = []
    # iterate through the rows
    for row in df.itertuples():
        ef.append(derive_multi_flags(PwrsysErrorFlag1, int(row.error_flag1, 16)))
    # assign the error flags
    df[name] = ef

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Mooring Power System Controller (PSC) Status Data',
        'summary': (
            'Measures the status of the mooring power system controller, encompassing the '
            'batteries, recharging sources (wind and solar), and outputs.'
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
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(PWRSYS[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(PWRSYS[c])
            d[:] = df[c].values
        elif c in ['override_flag', 'error_flag1', 'error_flag2', 'error_flag3']:
            d = nc.createVariable(c, 'i8', ('time',))
            d.setncatts(PWRSYS[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=PWRSYS[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
