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

from pyseas.data.ph_functions import ph_battery, ph_thermistor, ph_calc_phwater


def main(argv=None):
    # load  the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth    # utilize the switch option to set the deployment depth

    # load the json data file and return a panda data frame
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # set the depth and deployment id
    df['depth'] = depth
    df['deploy_id'] = deployment

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
    refnc = np.array(np.vstack(df['reference_measurements'].values), dtype='int32')
    light = np.array(np.vstack(df['light_measurements'].values), dtype='int32')

    df['pH'] = ph_calc_phwater(refnc, light, therm, ea434, eb434, ea578, eb578, slope, offset, salinity)

    # now we need to reset the light and reference arrays to variables that are more meaningful and useful
    refnc = np.atleast_3d(refnc)      # 4 sets of 4 seawater plus DI measurements (blanks)
    refnc = np.reshape(refnc, (nrec, 4, 4))
    fill = np.ones((nrec, 19)) * -999999999
    df['blank_refrnc_434'] = np.concatenate((refnc[:, :, 0], fill), axis=1).tolist()  # DI blank reference, 434 nm
    df['blank_signal_434'] = np.concatenate((refnc[:, :, 1], fill), axis=1).tolist()  # DI blank signal, 434 nm
    df['blank_refrnc_578'] = np.concatenate((refnc[:, :, 2], fill), axis=1).tolist()  # DI blank reference, 578 nm
    df['blank_signal_578'] = np.concatenate((refnc[:, :, 3], fill), axis=1).tolist()  # DI blank signal, 578 nm

    light = np.atleast_3d(light)
    light = np.reshape(light, (nrec, 23, 4))
    df['reference_434'] = light[:, :, 0].tolist()   # reference signal, 434 nm
    df['signal_434'] = light[:, :, 1].tolist()   # signal intensity, 434 nm (PH434SI_L0)
    df['reference_578'] = light[:, :, 2].tolist()   # reference signal, 578 nm
    df['signal_578'] = light[:, :, 3].tolist()   # signal intensity, 578 nm (PH578SI_L0)

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
        longitude=lon,
        station_name=platform,
        global_attributes=global_attributes,
        times=df.time.values.astype(np.int64) * 10**-9,
        verticals=df.depth.values,
        output_filename=outfile,
        vertical_positive='down')

    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # create a new dimension for the 23 measurements in the 4 light arrays (will use fill values to pad out the
    # reference arrays to have a single common dimension
    nc.createDimension('measurements', size=23)
    d = nc.createVariable('measurements', 'i', ('measurements',))
    d.setncatts(PHSEN['measurements'])
    d[:] = np.arange(0, 23).tolist()

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        if c in ['light_measurements', 'reference_measurements']:
            # print("Skipping '{}' (will be represented by more meaningful variables)".format(c))
            continue

        # create the netCDF.Variable object for the date/time and deploy_id strings
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(PHSEN[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(PHSEN[c])
            d[:] = df[c].values
        # create the netCDF.Variable object for the blank and measurement arrays
        elif c in ['blank_refrnc_434', 'blank_signal_434', 'blank_refrnc_578', 'blank_signal_578',
                   'reference_434', 'signal_434', 'reference_578', 'signal_578']:
            d = nc.createVariable(c, 'i', ('time', 'measurements',))
            d.setncatts(PHSEN[c])
            d[:] = np.array(np.vstack(df[c].values), dtype='int32')
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=PHSEN[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()


if __name__ == '__main__':
    main()
