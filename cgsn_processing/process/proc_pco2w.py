#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_parsers.process.proc_pco2w
@file cgsn_parsers/process/proc_pco2w.py
@author Christopher Wingard
@brief Calculate the pCO2 of water from the SAMI2-pCO2 (PCO2W) instrument
"""
import numpy as np
import pandas as pd
import pickle
import os
import re

from datetime import datetime, timedelta
from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs
from pytz import timezone

from cgsn_parsers.parsers.common import dcl_to_epoch
from cgsn_processing.process.common import Coefficients, inputs, json2df, df2omtdf
from cgsn_processing.process.configs.attr_pco2w import PCO2W
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.co2_functions import co2_blank, co2_thermistor, co2_pco2wat
from pyseas.data.ph_functions import ph_battery


class Blanks(object):
    """
    Serialized object used to store the PCO2W absorbance blanks used in the calculations of the pCO2 of seawater from
    a Sunburst Sensors, SAMI2-pCO2
    """
    def __init__(self, blnkfile, k434, k620):
        # initialize the information needed to define the blanks Pickle file
        # and the blanks        
        self.blnkfile = blnkfile
        self.k434 = k434
        self.k620 = k620
    
    def load_blanks(self):
        # load the cPickled blanks dictionary
        with open(self.blnkfile, 'rb') as f:
            blank = pickle.load(f)

        # assign the blanks
        self.k434 = blank['434']
        self.k620 = blank['620']
        
    def save_blanks(self):
        # create the blanks dictionary        
        blank = {
            '434': self.k434,
            '620': self.k620
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

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # This is an empty file, end processing
        return None

    # initialize the calibrations data class
    coeff_file = os.path.abspath(args.coeff_file)
    cal = Calibrations(coeff_file)  # initialize calibration class

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        cal.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('PCO2W', args.serial, (df.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            cal.read_csv(csv_url)
            cal.save_coeffs()
        else:
            print('A source for the PCO2W calibration coefficients for {} could not be found'.format(infile))
            return None

    # initialize the pCO2 blanks class
    blank_file = os.path.abspath(args.devfile)
    blank = Blanks(blank_file, -9999.9, -9999.9)

    # check for the source of pCO2 blanks and load accordingly
    if os.path.isfile(blank_file):
        # we always want to use this file if it exists
        blank.load_blanks()
    else:
        # Create one using defaults of 1
        blank.save_blanks()

    # convert the raw battery voltage and thermistor values from counts
    # to V and degC, respectively
    df['thermistor'] = co2_thermistor(df['thermistor_raw'])
    df['voltage_battery'] = ph_battery(df['voltage_raw'])

    # compare the instrument clock to the GPS based DCL time stamp
    # --> PCO2W uses the OSX date format of seconds since 1904-01-01
    mac = datetime.strptime("01-01-1904", "%m-%d-%Y")
    ept = datetime.strptime("01-01-1970", "%m-%d-%Y")
    offset = []
    for i in range(len(df['time'])):
        proc = ept + timedelta(seconds=dcl_to_epoch(df['process_date_time'][i]))
        proc.replace(tzinfo=timezone('UTC'))                # DCL sample processing time
        rec = mac + timedelta(seconds=df['record_time'][i].astype(np.uint32) * 1.)
        rec.replace(tzinfo=timezone('UTC'))                 # SAMI record time
        offset.append((proc - rec).total_seconds())

    df['time_offset'] = offset

    # calculate pCO2
    pCO2 = []
    k434 = []
    k620 = []

    for i in range(len(df['record_type'])):
        if df['record_type'][i] == 4:
            # this is a light measurement, calculate the pCO2 concentration
            if blank.k434 == -9999.9 and blank.k620 == -9999.9:
                # We don't have a blank to use in the calculation
                pCO2.append(-9999.9)
            else:
                p = co2_pco2wat(df['ratio_434'][i], df['ratio_620'][i], df['thermistor'][i], cal.coeffs['calt'],
                            cal.coeffs['cala'], cal.coeffs['calb'], cal.coeffs['calc'],
                            blank.k434, blank.k620)
                pCO2.append(p.item())

            # record the blanks used
            k434.append(blank.k434)
            k620.append(blank.k620)

        if df['record_type'][i] == 5:
            # this is a dark measurement, no pCO2 measurement, update and save the new blanks
            blank.k434 = co2_blank(df['ratio_434'][i])
            blank.k620 = co2_blank(df['ratio_620'][i])
            blank.save_blanks()

            pCO2.append(-9999.9)
            k434.append(blank.k434)
            k620.append(blank.k620)

    # add the resulting data to the dataframe
    df['pCO2'] = pCO2
    df['k434'] = k434
    df['k620'] = k620

    # convert the dataframe to a format suitable for the pocean OMTs
    df['deploy_id'] = deployment
    df = df2omtdf(df, lat, lon, depth)

    # add to the global attributes for the PCO2W
    attrs = PCO2W
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTs.from_dataframe(df, outfile, attributes=attrs)
    nc.close()


if __name__ == '__main__':
    main()
