#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_parsers.process.proc_pco2w
@file cgsn_parsers/process/proc_pco2w.py
@author Christopher Wingard
@brief Calculate the pCO2 of water from the SAMI-pCO2 (PCO2W) instrument
"""
import json
import numpy as np
import os
import pandas as pd
import warnings

from datetime import datetime, timedelta
from pytz import timezone

from cgsn_processing.process.common import Coefficients, NumpyEncoder, ENCODING, inputs, dict_update, json2df, \
    update_dataset
from cgsn_processing.process.configs.attr_pco2w import PCO2W
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.co2_functions import co2_blank, co2_thermistor, co2_pco2wat
from pyseas.data.ph_functions import ph_battery


class Blanks(object):
    """
    JSON object used to store the PCO2W absorbance blanks used in the
    calculations of the pCO2 of seawater from a Sunburst Sensors, SAMI-pCO2
    """
    def __init__(self, blnkfile, k434, k620):
        # initialize the information needed to define the file and pure water blanks
        self.blnkfile = blnkfile
        self.k434 = k434
        self.k620 = k620

    def load_blanks(self):
        # load the blanks
        with open(self.blnkfile, 'r') as f:
            blanks = json.load(f)

        # assign the blanks
        self.k434 = blanks['k434']
        self.k620 = blanks['k620']

    def save_blanks(self):
        # create the blanks dictionary
        blanks = {
            'k434': self.k434,
            'k620': self.k620
        }

        # save the blanks to a JSON file (remove the file, if it exists, before writing the new data)
        try:
            os.remove(self.blnkfile)
        except OSError:
            pass

        # now write the blanks to the file
        with open(self.blnkfile, 'w') as f:
            jdata = json.dumps(blanks, cls=NumpyEncoder)
            f.write(jdata)

            
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
            if row[1] == 'CC_cala':
                coeffs['cala'] = float(row[2])
            if row[1] == 'CC_calb':
                coeffs['calb'] = float(row[2])
            if row[1] == 'CC_calc':
                coeffs['calc'] = float(row[2])
            if row[1] == 'CC_calt':
                coeffs['calt'] = float(row[2])
            if row[1] == 'CC_sami_bits':
                coeffs['sami_bits'] = float(row[2])
            if row[1] == 'CC_cal_range':
                coeffs['cal_range'] = np.array(json.loads(row[2]))

        # serial number, stripping off all but the numbers
        coeffs['serial_number'] = data.serial[0]

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_pco2w(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the Sunburst Sensors SAMI-pCO2 sensor. Loads the
    JSON formatted parsed data and applies appropriate calibration coefficients
    to convert the raw parsed data into engineering units. If no calibration
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
    :kwargs serial_number: The serial number of the SAMI-pCO2
    :return pco2w: An xarray dataset with the processed PHSEN data
    """
    # process the variable length keyword arguments
    serial_number = kwargs.get('serial_number')

    # load the json data file as a panda dataframe for further processing
    data = json2df(infile)
    if data.empty:
        # json data file was empty, exiting
        return None

    # set the deployment id as a variable
    data['deploy_id'] = deployment

    # initialize the calibrations data class
    coeff_file = os.path.join(os.path.dirname(infile), 'pco2w.calibration_coeffs.json')
    cal = Calibrations(coeff_file)
    proc_flag = False

    # check for the source of calibration coefficients and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        cal.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('PCO2W', serial_number, (data.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            cal.read_csv(csv_url)
            cal.save_coeffs()
            proc_flag = True
        else:
            warnings.warn('Required calibrations coefficients could not be found.')

    # initialize the pCO2 blanks class
    blank_file = os.path.join(os.path.dirname(infile), 'pco2w.blank_coeffs.json')
    blanks = Blanks(blank_file, np.nan, np.nan)

    # check for the source of pCO2 blanks and load accordingly
    if os.path.isfile(blank_file):
        # we always want to use this file if it exists
        blanks.load_blanks()
    else:
        # Create one using NaN's for the default blanks
        blanks.save_blanks()

    # convert the raw battery voltage and thermistor values from counts to V and degC, respectively
    data.rename(columns={'voltage_raw': 'raw_battery_voltage',
                         'thermistor_raw': 'raw_thermistor'}, inplace=True)
    if proc_flag:
        data['thermistor_temperature'] = co2_thermistor(data['raw_thermistor'], cal.coeffs['sami_bits'])
        data['battery_voltage'] = ph_battery(data['raw_battery_voltage'], cal.coeffs['sami_bits'])
    else:
        data['thermistor_temperature'] = data['raw_thermistor'] * np.nan
        data['battery_voltage'] = data['raw_battery_voltage'] * np.nan

    # reset the data type and units for the record time to make sure the value is correctly represented and can be
    # calculated against. the PCO2W uses the OSX date format of seconds since 1904-01-01. here we convert to seconds
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
        if 'process_date_time' in data.columns:
            offset.append((rec - data['time'][i]).total_seconds() - 300)    # with correction for processing time

    data['record_time'] = record_time   # replace the instrument time stamp
    if offset:
        data['time_offset'] = offset    # add the estimated instrument clock offset

    # calculate pCO2
    pco2 = []
    k434 = []
    k620 = []

    for i in range(len(data)):
        if data['record_type'][i] == 4:
            # this is a light measurement, calculate the pCO2 concentration
            if not proc_flag or (np.isnan(blanks.k434) and np.isnan(blanks.k620)):
                # We don't have a blank to use in the calculation, or the calibration coefficients are missing
                pco2.append(np.nan)
            else:
                p = co2_pco2wat(data['ratio_434'][i], data['ratio_620'][i], data['thermistor_temperature'][i],
                                cal.coeffs['calt'], cal.coeffs['cala'], cal.coeffs['calb'], cal.coeffs['calc'],
                                blanks.k434, blanks.k620)
                pco2.append(p.item())

            # record the blanks used
            k434.append(blanks.k434)
            k620.append(blanks.k620)

        if data['record_type'][i] == 5:
            # this is a pure water blank measurement, update and save the new blanks
            blanks.k434 = co2_blank(data['ratio_434'][i])
            blanks.k620 = co2_blank(data['ratio_620'][i])
            blanks.save_blanks()

            pco2.append(np.nan)
            k434.append(blanks.k434)
            k620.append(blanks.k620)

    # add the resulting data to the data frame and convert to an xarray data set
    data['pCO2'] = pco2
    data['k434'] = k434
    data['k620'] = k620
    pco2w = data.to_xarray()

    # update the metadata and set up the data for export to NetCDF
    attrs = dict_update(PCO2W, SHARED)  # merge shared and PCO2W attribute dictionaries into a single dictionary
    pco2w = update_dataset(pco2w, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    if proc_flag:
        pco2w.attrs['processing_level'] = 'processed'
    else:
        pco2w.attrs['processing_level'] = 'parsed'

    return pco2w


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

    # process the PCO2W data and save the results to disk
    pco2w = proc_pco2w(infile, platform, deployment, lat, lon, depth, serial_number=serial_number)
    if pco2w:
        pco2w.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
