#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_dosta
@file cgsn_processing/process/proc_dosta.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the dissolved oxygen from the JSON formatted source data
"""
import json
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import Coefficients, inputs, json2df, dict_update, colocated_ctd, update_dataset, \
    ENCODING, FILL_INT, FILL_NAN
from cgsn_processing.process.configs.attr_dosta import GLOBAL, DOSTA
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.do2_functions import do2_phase_to_doxy, do2_salinity_correction
from gsw import SP_from_C

class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the DOSTA factory and secondary 2-point calibration coefficients. Values come from either a serialized
        object created per instrument and deployment (calibration coefficients do not change in the middle of a
        deployment), or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url
        self.coeffs = {}

    def read_csv(self, csv_url):
        """
        Reads the values from a DOSTA calibration file already parsed and stored on Github as a CSV file. Note,
        the formatting of those files puts some constraints on this process. If someone has a cleaner method,
        I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # scale and offset correction factors from a two-point calibration
            if row[1] == 'CC_conc_coef':
                coeffs['two_point_coeffs'] = np.array(json.loads(row[2]))

            # Stern-Volmer-Uchida calibration coefficients from a multipoint factory calibration
            if row[1] == 'CC_csv':
                coeffs['svu_cal_coeffs'] = np.array(json.loads(row[2]))

        # save the resulting dictionary
        self.coeffs = coeffs

def proc_dosta(infile, platform, deployment, lat, lon, depth, ctd_name=None):
    """

    :param infile:
    :param platform:
    :param deployment:
    :param lat:
    :param lon:
    :param depth:
    :return:
    """
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    df['z'] = depth
    df['deploy_id'] = deployment
    empty_data = np.atleast_1d(df['serial_number']).astype(np.int32) * FILL_NAN

    # clean up and rename the variables
    df.drop(columns=['dcl_date_time_string'], inplace=True)

    # create empty variables for the derived values and the co-located CTD data
    df['temperature'] = empty_data
    df['pressure'] = empty_data
    df['salinity'] = empty_data
    df['svu_oxygen_concentration'] = empty_data
    df['corrected_oxygen_concentratio'] = empty_data

    # create an xarray data set from the data frame
    raw = xr.Dataset.from_dataframe(df)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    attrs = dict_update(GLOBAL, DOSTA)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    raw = update_dataset(raw, platform, deployment, lat, lon, [depth, depth, depth], attrs)

    # load the instrument calibration data
    dosta_coeff = os.path.join(os.path.dirname(infile), 'dosta.cal_coeffs.json')
    dev = Calibrations(dosta_coeff)  # initialize calibration class

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(dosta_coeff):
        # we always want to use this file if it already exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('DOSTA', str(df['serial_number'][0]), df['time'][0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            # If we cannot find the calibration coefficients we are done, do not attempt to create a processed file
            print('A source for the calibration coefficients for {} could not be found.', str(df['serial_number'][0]))
            raw.attrs['processing_level'] = 'parsed'
            return raw

    # recompute the oxygen concentration from the calibrated phase, optode thermistor temperature and the calibration
    # coefficients
    df['svu_oxygen_concentration'] = do2_phase_to_doxy(df['calibrated_phase'], df['optode_thermistor'],
                                                       dev.coeffs['svu_cal_coeffs'], dev.coeffs['two_point_coeffs'])

    # pull in the co-located CTD data
    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if not ctd.empty:
        # set the CTD and pH time to the same units of seconds since 1970-01-01
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this DOSTA file
        coverage = ctd_time.min() <= min(df['time']) and ctd_time.max() >= max(df['time'])

        # interpolate the temperature, pressure and salinity data into the DOSTA record
        if coverage:
            temperature = np.mean(np.interp(df['time'], ctd_time, ctd.temperature))
            df['temperature'] = temperature

            pressure = np.mean(np.interp(df['time'], ctd_time, ctd.pressure))
            df['pressure'] = pressure

            salinity = SP_from_C(ctd.conductivity * 10.0, ctd.temperature, ctd.pressure)
            salinity = np.mean(np.interp(df['time'], ctd_time, salinity))
            df['salinity'] = salinity

            # calculate the pressure and salinity corrected oxygen concentration
            df['corrected_oxygen_concentration'] = do2_salinity_correction(df['svu_oxygen_concentration'],
                                                                           df['pressure'], df['temperature'],
                                                                           df['salinity'], lat, lon)

    # create an xarray data set from the data frame
    proc = xr.Dataset.from_dataframe(df)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    proc = update_dataset(proc, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    proc.attrs['processing_level'] = 'processed'
    return proc

def main(argv=None):
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # process the CTDBP data and save the results to disk
    dosta = proc_dosta(infile, platform, deployment, lat, lon, depth, ctd_name)
    if dosta:
        dosta.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)

if __name__ == '__main__':
    main()
