#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_flort
@file cgsn_processing/process/proc_cspp_flort.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP FLORT data from JSON formatted source data
"""
import numpy as np
import os
import re

from gsw import z_from_p
from pocean.utils import dict_update
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTp
from scipy.interpolate import interp1d

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_flort import Calibrations
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_FLORT

from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


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
    site_depth = args.depth

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
        csv_url = find_calibration('FLORT', args.serial, (df.time.values.astype('int64') * 10**-9)[0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            raise Exception('A source for the FLORT calibration coefficients could not be found')

    # Apply the scale and offset correction factors from the factory calibration coefficients
    df['estimated_chlorophyll'] = flo_scale_and_offset(df['raw_signal_chl'], dev.coeffs['dark_chla'], dev.coeffs['scale_chla'])
    df['fluorometric_cdom'] = flo_scale_and_offset(df['raw_signal_cdom'], dev.coeffs['dark_cdom'], dev.coeffs['scale_cdom'])
    df['beta_700'] = flo_scale_and_offset(df['raw_signal_beta'], dev.coeffs['dark_beta'], dev.coeffs['scale_beta'])

    # Merge the co-located CTD temperature and salinity data and calculate the total optical backscatter
    ctd_file = re.sub('flort', 'ctdpf', infile)
    ctd_file = re.sub('TRIP', 'CTD', ctd_file)
    ctd = json2df(ctd_file)
    if not ctd.empty:
        # interpolate temperature and salinity data from the CTD into the FLORT record for calculations
        degC = interp1d(ctd.time.values.astype('int64'), ctd.temperature.values, bounds_error=False)
        df['temperature'] = degC(df.time.values.astype('int64'))
        psu = interp1d(ctd.time.values.astype('int64'), ctd.salinity, bounds_error=False)
        df['salinity'] = psu(df.time.values.astype('int64'))
        df['bback'] = flo_bback_total(df['beta_700'], df['temperature'], df['salinity'], 124., 700., 1.076)
    else:
        df['temperature'] = np.nan
        df['salinity'] = np.nan
        df['bback'] = np.nan

    # setup some further parameters for use with the OMTp class
    df['deploy_id'] = deployment
    df['site_depth'] = site_depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['z'] = -1 * z_from_p(df['depth'], lat)               # uses CTD pressure record interpolated into FLORT record
    df['t'] = df.pop('time')[0]                             # set profile time to time of first data record
    df['precise_time'] = df.t.values.astype('int64') / 1e9  # create a precise time record
    df['station'] = 0

    # clean-up duplicate depth values
    df.drop_duplicates(subset='z', keep='first', inplace=True)

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    flort_attr = CSPP

    flort_attr['global'] = dict_update(flort_attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    flort_attr = dict_update(flort_attr, CSPP_FLORT)

    nc = OMTp.from_dataframe(df, outfile, attributes=flort_attr)
    nc.close()

if __name__ == '__main__':
    main()
