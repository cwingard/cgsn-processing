#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_parsers.process.proc_pco2w
@file cgsn_parsers/process/proc_pco2w.py
@author Christopher Wingard
@brief Calculate the pCO2 of water from the SAMI2-pCO2 (PCO2W) instrument
"""
import pickle
import numpy as np
import os

from datetime import datetime, timedelta
from pytz import timezone

from cgsn_processing.process.common import Coefficients, inputs, json2df
from pyseas.data.co2_functions import pco2_blank, pco2_pco2wat
from pyseas.data.ph_functions import ph_thermistor, ph_battery


class Blanks(object):
    """
    Serialized object used to store the PCO2W absorbance blanks used in the calculations of the pCO2 of seawater from
    a Sunburst Sensors, SAMI2-pCO2
    """
    def __init__(self, blnkfile, blank_434, blank_620):
        # initialize the information needed to define the blanks Pickle file
        # and the blanks        
        self.blnkfile = blnkfile
        self.blank_434 = blank_434
        self.blank_620 = blank_620
    
    def load_blanks(self):
        # load the cPickled blanks dictionary
        with open(self.blnkfile, 'rb') as f:
            blank = pickle.load(f)

        # assign the blanks
        self.blank_434 = blank['434']
        self.blank_620 = blank['620']
        
    def save_blanks(self):
        # create the blanks dictionary        
        blank = {
            '434': self.blank_434,
            '620': self.blank_620
        }

        # save the cPickled blanks dictionary
        with open(self.blnkfile, 'wb') as f:
            pickle.dump(blank, f)

            
class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        A serialized object created per instrument and deployment (calibration coefficients do not change in the
        middle of a deployment), or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from the CSV file already parsed and stored on Github. Note, the formatting of those files
        puts some constraints on this process. If someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}
        
        # read in the calibration data
        data = pd.read_csv(csv_url, usecols=[0,1,2])
        for idx, row in data.iterrows():
            if row[1] == 'CC_cala':
                coeffs['cala'] = np.float(row[2])
            if row[1] == 'CC_calb':
                coeffs['calb'] = np.float(row[2])
            if row[1] == 'CC_calc':
                coeffs['calc'] = np.float(row[2])
            if row[1] == 'CC_calt':
                coeffs['calt'] = np.float(row[2])

        # serial number, stripping off all but the numbers
        coeffs['serial_number'] = data.serial[0]

        # save the resulting dictionary
        self.coeffs = coeffs


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    coeff_file = os.path.abspath(args.coeff_file)
    cal = Calibrations(coeff_file)  # initialize calibration class

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        cal.load_coeffs()
    elif args.csvurl:
        # load from the CI hosted CSV files
        cal.read_csv(args.csvurl)
        cal.save_coeffs()
    else:
        raise Exception('A source for the PCO2W calibration coefficients could not be found')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # This is an empty file, end processing
        return None

    df['depth'] = depth
    df['deploy_id'] = deployment

    # convert the raw battery voltage and thermistor values from counts
    # to V and degC, respectively
    df['thermistor'] = ph_thermistor(df['thermistor_raw'])
    df['voltage_battery'] = ph_battery(df['voltage_battery'])

    # compare the instrument clock to the GPS based DCL time stamp
    # --> PCO2W uses the OSX date format of seconds since 1904-01-01
    mac = datetime.strptime("01-01-1904", "%m-%d-%Y")
    offset = []
    for i in range(len(df['time'])):
        rec = mac + timedelta(seconds=df['record_time'][i].astype(np.float64))
        rec.replace(tzinfo=timezone('UTC'))
        offset.append((rec - df['time'][i]).total_seconds())

    df['time_offset'] = offset

    # set factory constants for pCO2 calculations
    ea434 = 19706.   # factory constants
    eb434 = 3073.    # factory constants
    ea620 = 34.      # factory constants
    eb620 = 44327.   # factory constants

    # calculate pCO2
    pCO2 = []
    blank434 = []
    blank620 = []

    for i in range(len(df['record_type'])):
        if df['record_type'][i] == 4:
            # this is a light measurement, calculate the pCO2
            pCO2.append(pco2_pco2wat(df['record_type'][i], df['light_measurements'][i], df['thermistor'][i],
                                     ea434, eb434, ea620, eb620,
                                     cal.coeffs['calt'], cal.coeffs['cala'], cal.coeffs['calb'], cal.coeffs['calc'],
                                     blank.blank_434, blank.blank_620)[0])

            # record the blanks used
            blank434.append(blank.blank_434)
            blank620.append(blank.blank_620)

        if pco2w.record_type[i] == 5:
            # this is a dark measurement, update and save the new blanks
            blank.blank_434 = pco2_blank(pco2w.light_measurements[i][6])
            blank.blank_620 = pco2_blank(pco2w.light_measurements[i][7])
            blank.save_blanks()

            blank434.append(blank.blank_434)
            blank620.append(blank.blank_620)

    # save the resulting data to a json formatted file
    pco2w.pCO2 = pCO2
    pco2w.blank434 = blank434
    pco2w.blank620 = blank620

    with open(outfile, 'w') as f:
        f.write(pco2w.toJSON())

if __name__ == '__main__':
    main()
