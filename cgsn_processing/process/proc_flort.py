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
import pandas as pd
import re

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import Coefficients, inputs, json2df
from cgsn_processing.process.configs.attr_flort import FLORT

from pyseas.data.flo_functions import flo_scale_and_offset


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
    # load  the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lng = args.longitude
    depth = args.depth

    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    elif args.csvurl:
        # load from the CI hosted CSV files
        csv_url = args.csvurl
        dev.read_csv(csv_url)
        dev.save_coeffs()
    else:
        raise Exception('A source for the FLORT calibration coefficients could not be found')

    # load the json data file and return a panda data frame
    df = json2df(infile)
    df['depth'] = depth
    df['deploy_id'] = deployment

    # Apply the scale and offset correction factors from the factory calibration coefficients
    df['estimated_chlorophyll'] = flo_scale_and_offset(df['raw_signal_chl'], dev.coeffs['dark_chla'], dev.coeffs['scale_chla'])
    df['fluorometric_cdom'] = flo_scale_and_offset(df['raw_signal_cdom'], dev.coeffs['dark_cdom'], dev.coeffs['scale_cdom'])
    df['beta_700'] = flo_scale_and_offset(df['raw_signal_beta'], dev.coeffs['dark_beta'], dev.coeffs['scale_beta'])

    # TODO: Add the calculation of total optical backscatter here. Requires co-located CTD data

    # Setup the global attributes for the NetCDF file and create the NetCDF timeseries object
    global_attributes = {
        'title': 'WET Labs ECO Triplet Chlorophyll and CDOM Fluorescence and Optical Backscatter',
        'summary': (
            'Records bursts of ECO Triplet data measuring chlorophyll and CDOM fluorescence and optical backscatter.'
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
            longitude=lng,
            station_name=platform,
            global_attributes=global_attributes,
            times=df.time.values.astype(np.float) * 10**-9,
            verticals=df.depth.values,
            output_filename=outfile,
            vertical_positive='down')

    # add the data from the data frame and set the attributes
    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'latitude', 'longitude', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(FLORT[c])
            d[:] = df[c].values
        elif c == 'flort_date_time_string':
            d = nc.createVariable(c, 'S17', ('time',))
            d.setncatts(FLORT[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(FLORT[c])
            d[:] = df[c].values
        else:
            # use the TimeSeries object to add the variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=FLORT[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
