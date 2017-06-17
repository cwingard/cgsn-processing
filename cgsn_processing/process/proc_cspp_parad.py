#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_flort
@file cgsn_processing/process/proc_cspp_flort.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP FLORT data from JSON formatted source data
"""
import os
import re

from pocean.utils import dict_update
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTP
from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.proc_flort import Calibrations
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_FLORT

from pyseas.data.flo_functions import flo_scale_and_offset

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

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # Apply the scale and offset correction factors from the factory calibration coefficients
    df['estimated_chlorophyll'] = flo_scale_and_offset(df['raw_signal_chl'], dev.coeffs['dark_chla'], dev.coeffs['scale_chla'])
    df['fluorometric_cdom'] = flo_scale_and_offset(df['raw_signal_cdom'], dev.coeffs['dark_cdom'], dev.coeffs['scale_cdom'])
    df['beta_700'] = flo_scale_and_offset(df['raw_signal_beta'], dev.coeffs['dark_beta'], dev.coeffs['scale_beta'])

    # TODO: Add the calculation of total optical backscatter here. Requires co-located CTD data

    # setup some further parameters for use with the OMTP class
    df['deploy_id'] = deployment
    df['site_depth'] = site_depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['z'] = -1 * z_from_p(df['depth'], lat)    # uses CTD pressure record interpolated into FLORT record
    df['t'] = df.pop('time')    # renames time to t, OMTP class will convert it back
    df['station'] = 0

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    flort_attr = CSPP

    flort_attr['global'] = dict_update(flort_attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    flort_attr = dict_update(flort_attr, CSPP_FLORT)

    nc = OMTP.from_dataframe(df, outfile, attributes=flort_attr)
    nc.close()

if __name__ == '__main__':
    main()
