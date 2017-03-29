#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_pco2a
@file cgsn_processing/process/proc_pco2a.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the PCO2A from JSON formatted source data
"""
import numpy as np
import os
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_pco2a import PCO2A

from pyseas.data.co2_functions import pco2_ppressure

def main():
    # load  the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lng = args.longitude
    
    # load the json data file and return a panda data frame
    df = json2df(infile)
    df['depth'] = 0.0       # default depth, will update for sensors below
    df['deploy_id'] = deployment

    # rename the co2_source parameter to sample_id for better subsetting, and the CO2 measurement variable
    df.rename(columns={'co2_source': 'sample_id', 'measured_water_co2': 'measured_co2'}, inplace=True)

    # calculate the partial pressure of CO2 in air and water samples
    df['pCO2'] = pco2_ppressure(df['measured_co2'], df['gas_stream_pressure'])

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'Partial Pressure of CO2 in the Air and Water',
        'summary': (
            'Measures partial pressure of CO2 in the air and water, concurrently.'
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
            times=df.time.values.astype(np.float) * 10**-9,
            verticals=df.depth.values,
            output_filename=outfile,
            vertical_positive='down')

    # add the data from the data frame and set the attributes
    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # add the PCO2A inlet depths/altitudes as variables
    # depth of the PCO2A water inlet
    d = nc.createVariable('z_water', 'f4')
    d.setncatts(PCO2A['z_water'])
    d[:] = 1.25
    # altitude of the PCO2A air inlet
    d = nc.createVariable('z_air', 'f4')
    d.setncatts(PCO2A['z_air'])
    d[:] = -2.00

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c in ['dcl_date_time_string', 'co2_date_time_string']:
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(PCO2A[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(PCO2A[c])
            d[:] = df[c].values
        elif c == 'sample_id':
            d = nc.createVariable(c, 'S1', ('time',))
            d.setncatts(PCO2A[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=PCO2A[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
