#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_flort
@file cgsn_processing/process/proc_flort.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the FLORT from JSON formatted source data
"""
import numpy as np
import os
import re

from gsw import SP_from_C
from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs
from scipy.interpolate import interp1d

from cgsn_processing.process.common import Coefficients, inputs, json2df, df2omtdf
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_flort import FLORT

from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the FLORT factory calibration coefficients for a unit. Values come from either a serialized object
        created per instrument and deployment (calibration coefficients do not change in the middle of a deployment),
        or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from an ECO Triplet (aka FLORT) device file already parsed and stored on
        Github as a CSV files. Note, the formatting of those files puts some constraints on this process. 
        If someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # scale and offset correction factors
            if row[1] == 'CC_dark_counts_cdom':
                coeffs['dark_cdom'] = row[2]
            if row[1] == 'CC_scale_factor_cdom':
                coeffs['scale_cdom'] = row[2]

            if row[1] == 'CC_dark_counts_chlorophyll_a':
                coeffs['dark_chla'] = row[2]
            if row[1] == 'CC_scale_factor_chlorophyll_a':
                coeffs['scale_chla'] = row[2]

            if row[1] == 'CC_dark_counts_volume_scatter':
                coeffs['dark_beta'] = row[2]
            if row[1] == 'CC_scale_factor_volume_scatter':
                coeffs['scale_beta'] = row[2]

            # optical backscatter correction factors
            if row[1] == 'CC_angular_resolution':
                coeffs['chi_factor'] = row[2]
            if row[1] == 'CC_measurement_wavelength':
                coeffs['wavelength'] = row[2]
            if row[1] == 'CC_scattering_angle':
                coeffs['scatter_angle'] = row[2]

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

    # remove the FLORT date/time string from the dataset
    _ = df.pop('flort_date_time_string')

    # check for the source of calibration coeffs and load accordingly
    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('FLORT', args.serial, (df.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            raise Exception('A source for the FLORT calibration coefficients could not be found')

    # Apply the scale and offset correction factors from the factory calibration coefficients
    df['estimated_chlorophyll'] = flo_scale_and_offset(df['raw_signal_chl'], dev.coeffs['dark_chla'],
                                                       dev.coeffs['scale_chla'])
    df['fluorometric_cdom'] = flo_scale_and_offset(df['raw_signal_cdom'], dev.coeffs['dark_cdom'],
                                                   dev.coeffs['scale_cdom'])
    df['beta_700'] = flo_scale_and_offset(df['raw_signal_beta'], dev.coeffs['dark_beta'], dev.coeffs['scale_beta'])

    # Merge the co-located CTD temperature and salinity data and calculate the total optical backscatter
    ctd_file = re.sub('flort', 'ctdbp', infile)
    ctd = json2df(ctd_file)
    if not ctd.empty:
        # calculate the practical salinity of the seawater from the temperature, conductivity and pressure measurements
        ctd['psu'] = SP_from_C(ctd['conductivity'] * 10.0, ctd['temperature'], ctd['pressure'])

        # interpolate temperature and salinity data from the CTD into the FLORT record for calculations
        degC = interp1d(ctd.time.values.astype('int64'), ctd.temperature.values, bounds_error=False)
        df['temperature'] = degC(df.time.values.astype('int64'))

        psu = interp1d(ctd.time.values.astype('int64'), ctd.psu, bounds_error=False)
        df['salinity'] = psu(df.time.values.astype('int64'))

        df['bback'] = flo_bback_total(df['beta_700'], df['temperature'], df['salinity'], 124., 700., 1.076)
    else:
        df['temperature'] = np.nan
        df['salinity'] = np.nan
        df['bback'] = np.nan

    # convert the dataframe to a format suitable for the pocean OMTs
    df['deploy_id'] = deployment
    df = df2omtdf(df, lat, lon, depth)

    # Setup and update the attributes for the resulting NetCDF file
    attr = FLORT
    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTs.from_dataframe(df, outfile, attributes=attr)
    nc.close()

if __name__ == '__main__':
    main()
