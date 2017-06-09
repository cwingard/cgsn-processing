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
from pyaxiom.netcdf.sensors import TimeSeries
from pytz import timezone

from cgsn_processing.process.common import Coefficients, inputs, json2df
from cgsn_processing.process.configs.attr_pco2w import PCO2W

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
    elif args.csvurl:
        # load from the CI hosted CSV files
        cal.read_csv(args.csvurl)
        cal.save_coeffs()
    else:
        raise Exception('A source for the PCO2W calibration coefficients could not be found')

    # initialize the pCO2 blanks class
    blank_file = os.path.abspath(args.devfile)
    blank = Blanks(blank_file, 0, 0)

    # check for the source of pCO2 blanks and load accordingly
    if os.path.isfile(blank_file):
        # we always want to use this file if it exists
        blank.load_blanks()
    else:
        # Create one using defaults of 0
        blank.save_blanks()

    # set the depth and deployment variables
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
    blank_434 = []
    blank_620 = []

    for i in range(len(df['record_type'])):
        if df['record_type'][i] == 4:
            # this is a light measurement, calculate the pCO2
            pCO2.append(pco2_pco2wat(df['record_type'][i], df['light_measurements'][i], df['thermistor'][i],
                                     ea434, eb434, ea620, eb620,
                                     cal.coeffs['calt'], cal.coeffs['cala'], cal.coeffs['calb'], cal.coeffs['calc'],
                                     blank.blank_434, blank.blank_620)[0])

            # record the blanks used
            blank_434.append(blank.blank_434)
            blank_620.append(blank.blank_620)

        if df['record_type'][i] == 5:
            # this is a dark measurement, update and save the new blanks
            blank.blank_434 = pco2_blank(df['light_measurements'][i][6])
            blank.blank_620 = pco2_blank(df['light_measurements'][i][7])
            blank.save_blanks()

            blank_434.append(blank.blank_434)
            blank_620.append(blank.blank_620)

    # add the resulting data to the dataframe
    df['pCO2'] = pCO2
    df['blank_434'] = blank_434
    df['blank_620'] = blank_620

    # Setup the global attributes for the NetCDF file and create the NetCDF TimeSeries object
    global_attributes = {
        'title': 'Seawater pCO2 from PCO2W',
        'summary': (
            'Measures the seawater pCO2 from the Sunburst Sensors SAMI2-pCO2 Instrument).'
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

    # create a new dimension for the 14 light measurements
    nc.createDimension('measurements', size=14)
    d = nc.createVariable('measurements', 'i', ('measurements',))
    d.setncatts(PCO2W['measurements'])
    d[:] = np.arange(0, 14).tolist()

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time and deploy_id strings
        if c in ['collect_date_time', 'process_date_time']:
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(PCO2W[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(PCO2W[c])
            d[:] = df[c].values
        # create the netCDF.Variable object for the measurement array
        elif c in ['light_measurements']:
            d = nc.createVariable(c, 'i', ('time', 'measurements',))
            d.setncatts(PCO2W[c])
            d[:] = np.array(np.vstack(df[c].values), dtype='int32')
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=PCO2W[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
