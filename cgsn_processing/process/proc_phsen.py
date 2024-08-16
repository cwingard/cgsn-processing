#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_phsen
@file cgsn_processing/process/proc_phsen.py
@author Christopher Wingard
@brief Calculates the pH for the PHSEN and saves the data to NetCDF
"""
import warnings

import numpy as np
import os
import pandas as pd
import xarray as xr

from datetime import datetime, timedelta
from pytz import timezone

from cgsn_processing.process.common import ENCODING, Coefficients, colocated_ctd, inputs, json2df, \
    dict_update, update_dataset
from cgsn_processing.process.configs.attr_phsen import PHSEN
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.ph_functions import ph_battery, ph_thermistor, ph_calc_phwater
from gsw import SP_from_C


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        A serialized object created per instrument and deployment (calibration
        coefficients do not change in the middle of a deployment), or from
        parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from the CSV file already parsed and stored on GitHub.
        Note, the formatting of those files puts some constraints on this
        process. If someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        data = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in data.iterrows():
            if row[1] == 'CC_ea434':
                coeffs['ea434'] = float(row[2])
            if row[1] == 'CC_ea578':
                coeffs['ea578'] = float(row[2])
            if row[1] == 'CC_eb434':
                coeffs['eb434'] = float(row[2])
            if row[1] == 'CC_eb578':
                coeffs['eb578'] = float(row[2])
            if row[1] == 'CC_ind_off':
                coeffs['ind_off'] = float(row[2])
            if row[1] == 'CC_ind_slp':
                coeffs['ind_slp'] = float(row[2])
            if row[1] == 'CC_psal':
                coeffs['psal'] = float(row[2])
            if row[1] == 'CC_sami_bits':
                coeffs['sami_bits'] = float(row[2])

        # serial number
        coeffs['serial_number'] = data.serial[0]

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_phsen(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the Sunburst Sensors SAMI-pH sensor. Loads the JSON
    formatted parsed data and applies appropriate calibration coefficients to
    convert the raw parsed data into engineering units. If no calibration
    coefficients are available, filled variables are returned and the dataset
    processing level attribute is set to "parsed". If the calibration,
    coefficients are available then the dataset processing level attribute is
    set to "processed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwarg serial_number: The serial number of the SAMI-pH
    :kwarg ctd_name: Name of the co-located CTD to use for salinity data

    :return phsen: An xarray dataset with the processed PHSEN data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')
    serial_number = kwargs.get('serial_number')

    # load the json data file as a panda data frame for further processing
    df = json2df(infile)
    if df.empty:
        # json data file was empty, exiting
        return None

    # initialize the calibrations data class
    coeff_file = os.path.join(os.path.dirname(infile), 'phsen.calibration_coeffs.json')
    cal = Calibrations(coeff_file)
    proc_flag = False

    # check for the source of calibration coefficients and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        cal.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('PHSEN', serial_number, (df.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            cal.read_csv(csv_url)
            cal.save_coeffs()
            proc_flag = True
        else:
            warnings.warn('Required calibrations coefficients could not be found.')

    # clean up dataframe and create an empty data variable
    df.drop(columns=['dcl_date_time_string'], inplace=True)

    # rename select columns to match the expected names in the final data set
    df.rename(columns={'record_time': 'sensor_time',
                       'thermistor_start': 'raw_thermistor_start',
                       'thermistor_end': 'raw_thermistor_end',
                       'voltage_battery': 'raw_battery_voltage'}, inplace=True)

    # convert the raw battery voltage and thermistor values from counts to V and degC, respectively
    if proc_flag:
        df['thermistor_temperature_start'] = ph_thermistor(df['raw_thermistor_start'], cal.coeffs['sami_bits'])
        df['thermistor_temperature_end'] = ph_thermistor(df['raw_thermistor_end'], cal.coeffs['sami_bits'])
        df['battery_voltage'] = ph_battery(df['raw_battery_voltage'], cal.coeffs['sami_bits'])
    else:
        df['thermistor_temperature_start'] = df['raw_thermistor_start'] * np.nan
        df['thermistor_temperature_end'] = df['raw_thermistor_end'] * np.nan
        df['battery_voltage'] = df['raw_battery_voltage'] * np.nan

    # reset the data type and units for the sensor time to make sure the value is correctly represented and can be
    # calculated against. the PHSEN uses the OSX date format of seconds since 1904-01-01. here we convert to seconds
    # since 1970-01-01.
    rct = df['sensor_time'].astype(np.uint32).values * 1.0    # convert to a float
    mac = datetime.strptime("01-01-1904", "%m-%d-%Y")
    ept = datetime.strptime("01-01-1970", "%m-%d-%Y")
    sensor_time = []
    for i in range(len(df['time'])):
        rec = mac + timedelta(seconds=rct[i])
        rec.replace(tzinfo=timezone('UTC'))
        sensor_time.append((rec - ept).total_seconds())

    df['sensor_time'] = sensor_time   # replace the instrument time stamp

    # extract the reference and light measurement arrays from the data frame
    refnc = np.array(np.vstack(df.pop('reference_measurements').values), dtype='int32')
    light = np.array(np.vstack(df.pop('light_measurements').values), dtype='int32')

    # create an average temperature value to be used in calculating the pH
    therm = df[['thermistor_temperature_start', 'thermistor_temperature_end']].astype(float).mean(axis=1).values

    # setup default values to use if no co-located CTD is available
    nrec = len(df['time'])
    df['ctd_pressure'] = np.ones(nrec) * np.nan
    df['ctd_temperature'] = np.ones(nrec) * np.nan
    df['ctd_salinity'] = np.ones(nrec) * 34.0

    # check for data from a co-located CTD and test to see if it covers our time range of interest. will use the
    # salinity data from the CTD in the pH calculation, if available.
    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if not ctd.empty:
        # set the CTD and pH time to the same units of seconds since 1970-01-01
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9
        ph_time = df.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this pH file
        td = timedelta(hours=1).total_seconds()
        coverage = ctd_time.min() <= ph_time.min() and ctd_time.max() + td >= ph_time.max()

        # reset initial estimate of in-situ salinity if we have full coverage
        if coverage:
            df['ctd_pressure'] = np.interp(df['time'], ctd['time'], ctd.pressure)
            df['ctd_temperature'] = np.interp(df['time'], ctd['time'], ctd.temperature)
            salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
            df['ctd_salinity'] = np.interp(df['time'], ctd['time'], salinity)

    # add the salinity to the data set and calculate the pH
    if proc_flag:
        df['pH'] = ph_calc_phwater(refnc, light, therm, df['ctd_salinity'], cal.coeffs['ea434'], cal.coeffs['eb434'],
                                   cal.coeffs['ea578'], cal.coeffs['eb578'], cal.coeffs['ind_slp'],
                                   cal.coeffs['ind_off'])
    else:
        df['pH'] = np.ones(nrec) * np.nan

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

    # create a data set with the raw reference and light measurements
    raw = xr.Dataset({
        'blank_refrnc_434': (['time', 'measurements'], blank_refrnc_434.astype('int32')),
        'blank_signal_434': (['time', 'measurements'], blank_signal_434.astype('int32')),
        'blank_refrnc_578': (['time', 'measurements'], blank_refrnc_578.astype('int32')),
        'blank_signal_578': (['time', 'measurements'], blank_signal_578.astype('int32')),
        'reference_434': (['time', 'measurements'], reference_434.astype('int32')),
        'signal_434': (['time', 'measurements'], signal_434.astype('int32')),
        'reference_578': (['time', 'measurements'], reference_578.astype('int32')),
        'signal_578': (['time', 'measurements'], signal_578.astype('int32'))
    }, coords={'time': df['time'], 'measurements': np.arange(0, 23).astype('int32')})

    # merge the data sets together
    ds = xr.Dataset.from_dataframe(df)
    phsen = xr.merge([ds, raw])

    # create the final data set with full attributes
    phsen['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(phsen.time)).astype(str))
    attrs = dict_update(PHSEN, SHARED)  # merge global and PHSEN attribute dictionaries into a single dictionary
    phsen = update_dataset(phsen, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    if proc_flag:
        phsen.attrs['processing_level'] = 'processed'
    else:
        phsen.attrs['processing_level'] = 'parsed'

    return phsen


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
    serial_number = args.serial
    ctd_name = args.devfile  # name of co-located CTD

    # process the PHSEN data and save the results to disk
    phsen = proc_phsen(infile, platform, deployment, lat, lon, depth, ctd_name=ctd_name, serial_number=serial_number)
    if phsen:
        phsen.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
