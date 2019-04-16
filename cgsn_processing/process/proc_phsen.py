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
import xarray as xr

from datetime import datetime, timedelta
from pytz import timezone

from cgsn_processing.process.common import ENCODING, inputs, json2df, dict_update, update_dataset
from cgsn_processing.process.configs.attr_phsen import GLOBAL, PHSEN

from pyseas.data.ph_functions import ph_battery, ph_thermistor, ph_calc_phwater


def main(argv=None):
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # load the json data file as a panda dataframe for further processing
    data = json2df(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # set the deployment id as a variable
    data['deploy_id'] = deployment

    # convert the raw battery voltage and thermistor values from counts to V and degC, respectively
    data.rename(columns={'thermistor_start': 'raw_thermistor_start',
                         'thermistor_end': 'raw_thermistor_end',
                         'voltage_battery': 'raw_battery_voltage'},
                inplace=True)
    data['thermistor_start'] = ph_thermistor(data['raw_thermistor_start'])
    data['thermistor_end'] = ph_thermistor(data['raw_thermistor_end'])
    data['battery_voltage'] = ph_battery(data['raw_battery_voltage'])

    # reset the data type and units for the record time to make sure the value is correctly represented and can be
    # calculated against. the PHSEN uses the OSX date format of seconds since 1904-01-01. here we convert to seconds
    # since 1970-01-01. also, compare the instrument clock to the GPS based DCL time stamp (if present, does not apply
    # if this is an IMM hosted instrument).
    rct = data['record_time'].astype(np.uint32).values * 1.0    # convert to a float
    mac = datetime.strptime("01-01-1904", "%m-%d-%Y")
    ept = datetime.strptime("01-01-1970", "%m-%d-%Y")
    record_time = []
    offset = []
    for i in range(len(data['time'])):
        rec = mac + timedelta(seconds=rct[i])
        rec.replace(tzinfo=timezone('UTC'))
        record_time.append((rec - ept).total_seconds())
        if 'dcl_date_time_string' in data.columns:
            offset.append((rec - data['time'][i]).total_seconds())

    data['record_time'] = record_time   # replace the instrument time stamp
    if offset:
        data['time_offset'] = offset    # add the estimated instrument clock offset

    # extract the reference and light measurement arrays from the data frame
    refnc = np.array(np.vstack(data.pop('reference_measurements').values), dtype='int32')
    light = np.array(np.vstack(data.pop('light_measurements').values), dtype='int32')

    # create an average temperature value to be used in calculating the pH
    therm = data[['thermistor_start', 'thermistor_end']].astype(float).mean(axis=1).values

    # set factory default calibration values
    nrec = len(data['time'])
    ea434 = np.ones(nrec) * 17533.
    eb434 = np.ones(nrec) * 2229.
    ea578 = np.ones(nrec) * 101.
    eb578 = np.ones(nrec) * 38502.
    slope = np.ones(nrec) * 0.9698
    offset = np.ones(nrec) * 0.2484
    salinity = np.ones(nrec) * 34.0

    # calculate the pH
    data['pH'] = ph_calc_phwater(refnc, light, therm, ea434, eb434, ea578, eb578, slope, offset, salinity)

    # now we need to reset the light and reference arrays to named variables that will be more meaningful and useful in
    # the final data files
    refnc = np.atleast_3d(refnc)
    refnc = np.reshape(refnc, (nrec, 4, 4))   # 4 sets of 4 DI water measurements (blanks)
    fill = np.ones((nrec, 19)) * -9999999     # fill value to pad the reference measurements to same shape as light
    blank_refrnc_434 = np.concatenate((refnc[:, :, 0], fill), axis=1)  # DI blank reference, 434 nm
    blank_signal_434 = np.concatenate((refnc[:, :, 1], fill), axis=1)  # DI blank signal, 434 nm
    blank_refrnc_578 = np.concatenate((refnc[:, :, 2], fill), axis=1)  # DI blank reference, 578 nm
    blank_signal_578 = np.concatenate((refnc[:, :, 3], fill), axis=1)  # DI blank signal, 578 nm

    light = np.atleast_3d(light)
    light = np.reshape(light, (nrec, 23, 4))  # 4 sets of 23 seawater measurements
    reference_434 = light[:, :, 0]            # reference signal, 434 nm
    signal_434 = light[:, :, 1]               # signal intensity, 434 nm (PH434SI_L0)
    reference_578 = light[:, :, 2]            # reference signal, 578 nm
    signal_578 = light[:, :, 3]               # signal intensity, 578 nm (PH578SI_L0)

    # create a data set with the reference and light measurements
    ds = xr.Dataset({
        'blank_refrnc_434': (['time', 'measurements'], blank_refrnc_434.astype('int32')),
        'blank_signal_434': (['time', 'measurements'], blank_signal_434.astype('int32')),
        'blank_refrnc_578': (['time', 'measurements'], blank_refrnc_578.astype('int32')),
        'blank_signal_578': (['time', 'measurements'], blank_signal_578.astype('int32')),
        'reference_434': (['time', 'measurements'], reference_434.astype('int32')),
        'signal_434': (['time', 'measurements'], signal_434.astype('int32')),
        'reference_578': (['time', 'measurements'], reference_578.astype('int32')),
        'signal_578': (['time', 'measurements'], signal_578.astype('int32'))
    }, coords={'time': data['time'], 'measurements': np.arange(0, 23).astype('int32')})

    # merge the data sets together and create the final data set with full attributes
    pH = xr.merge([data, ds])
    attrs = dict_update(GLOBAL, PHSEN)      # merge global pH attribute dictionaries into a single dictionary
    pH = update_dataset(pH, platform, deployment, lat, lon, [depth, depth, depth], attrs)

    # save the file
    pH.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
