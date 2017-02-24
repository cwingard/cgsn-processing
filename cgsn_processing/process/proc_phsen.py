#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_phsen
@file cgsn_processing/process/proc_phsen.py
@author Christopher Wingard
@brief Calculates the pH for the PHSEN and saves the data to NetCDF
"""
import numpy as np
import os
import re

from datetime import datetime, timedelta
from pyaxiom.netcdf.sensors import TimeSeries
from pytz import timezone

from cgsn_processing.process.common import inputs, json2df
from cgsn_processing.process.configs.attr_phsen import PHSEN

from ion_functions.data.ph_functions import ph_battery, ph_thermistor, ph_calc_phwater


def main():
    # load  the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lng = args.longitude
    depth = args.switch.astype(np.float)    # utilize the switch option to set the deployment depth

    # load the json data file and return a panda data frame
    df = json2df(infile)
    if not df:
        # there was no data in this file, ending early
        return None

    # set the depth
    df['depth'] = depth

    # convert the raw battery voltage and thermistor values from counts
    # to V and degC, respectively
    df['thermistor_start'] = ph_thermistor(df['thermistor_start'])
    therm = ph_thermistor(df['thermistor_end'])
    df['thermistor_end'] = therm
    df['voltage_battery'] = ph_battery(df['voltage_battery'])

    # compare the instrument clock to the GPS based DCL time stamp
    # --> PHSEN uses the OSX date format of seconds since 1904-01-01
    mac = datetime.strptime("01-01-1904", "%m-%d-%Y")
    offset = []
    for i in range(len(df['time'])):
        rec = mac + timedelta(seconds=df['record_time'][i].astype(np.float64))
        rec.replace(tzinfo=timezone('UTC'))
        offset.append((rec - df['time'][i]).total_seconds())

    df['time_offset'] = offset

    # set default calibration values (could later roll this into a coefficients file)
    nrec = len(df['time'])
    ea434 = np.ones(nrec) * 17533.
    eb434 = np.ones(nrec) * 2229.
    ea578 = np.ones(nrec) * 101.
    eb578 = np.ones(nrec) * 38502.
    slope = np.ones(nrec) * 0.9698
    offset = np.ones(nrec) * 0.2484
    salinity = np.ones(nrec) * 33.0

    # calculate the pH (with some cursing and grumbling about the Object dtype pandas use for arrays)
    refnc = np.vstack(df['reference_measurements'].values).astype(np.int)
    light = np.vstack(df['light_measurements'].values).astype(np.int)
    df['pH'] = ph_calc_phwater(refnc, light, therm, ea434, eb434, ea578, eb578, slope, offset, salinity)

    # Setup the global attributes for the NetCDF file and create the NetCDF TimeSeries object
    global_attributes = {
        'title': 'Seawater pH from PHSEN',
        'summary': (
            'Measures the seawater pH from the Sunburst Sensors SAMI2-pH Instrument).'
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

    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # add the deployment index (dimensionless)
    d = nc.createVariable('deployment', 'i2')
    d.setncatts(PHSEN['deployment'])
    d[:] = int(re.sub('\D', '', deployment))

    # create new dimensions for the light and reference arrays
    nc.createDimension('light', size=92)
    nc.createDimension('refnc', size=16)

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(PHSEN[c])
            d[:] = df[c].values
        elif c == 'light_measurements':
            d = nc.createVariable(c, 'i', ('time', 'light',))
            d.setncatts(PHSEN[c])
            d[:] = light
        elif c == 'reference_measurements':
            d = nc.createVariable(c, 'i', ('time', 'refnc',))
            d.setncatts(PHSEN[c])
            d[:] = refnc
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=PHSEN[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
