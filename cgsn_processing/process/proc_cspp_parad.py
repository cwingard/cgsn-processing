#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_parad
@file cgsn_processing/process/proc_cspp_parad.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP PARAD data from JSON formatted source data
"""
import os
import pandas as pd
import re

from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs

from cgsn_processing.process.common import Coefficients, inputs, json2df, reset_long
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_PARAD

from pyseas.data.opt_functions import opt_par_satlantic


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the PARAD factory calibration coefficients for a unit. Values come from either a serialized object
        created per instrument and deployment (calibration coefficients do not change in the middle of a deployment),
        or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from an Satlantic PAR sensor (aka PARAD) device file already parsed and stored on
        Github as a CSV files. Note, the formatting of these files puts some constraints on this process.
        If someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # immersion, scale and offset correction factors
            if row[1] == 'CC_a0':
                coeffs['a0'] = row[2]
            if row[1] == 'CC_a1':
                coeffs['a1'] = row[2]
            if row[1] == 'CC_Im':
                coeffs['Im'] = row[2]

        # save the resulting dictionary
        self.coeffs = coeffs


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    _, fname = os.path.split(outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # remove the PARAD date/time string from the dataset
    _ = df.pop('parad_date_time_string')

    # check for the source of calibration coeffs and load accordingly
    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('PARAD', args.serial, (df.time.values.astype('int64') / 1e9)[0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            raise Exception('A source for the PARAD calibration coefficients could not be found')

    # Apply the scale, offset and immersion correction factors from the factory calibration coefficients
    df['irradiance'] = opt_par_satlantic(df['raw_par'], dev.coeffs['a0'], dev.coeffs['a1'], dev.coeffs['Im'])

    # setup some further parameters for use with the OMTs class
    df['deploy_id'] = deployment
    df['z'] = depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['t'] = df.pop('time')
    df['station'] = 0

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    attr = CSPP

    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    attr = dict_update(attr, CSPP_PARAD)

    nc = OMTs.from_dataframe(df, outfile, attributes=attr)
    nc.close()

if __name__ == '__main__':
    main()
