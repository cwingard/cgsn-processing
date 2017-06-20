#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_spkir
@file cgsn_processing/process/proc_cspp_spkir.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP SPKIR data from JSON formatted source data
"""
import numpy as np
import os
import re

from netCDF4 import Dataset
from pocean.utils import dict_update
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTP
from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_spkir import Calibrations
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_SPKIR
from pyseas.data.opt_functions import opt_ocr507_irradiance


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

    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('SPKIR', df.serial_number[0], (df.time.values.astype('int64') * 10**-9)[0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            raise Exception('A source for the SPKIR calibration coefficients could not be found')

    # pop the raw_channels array out of the dataframe (will put it back in later)
    channels = np.array(np.vstack(df.pop('raw_channels')), dtype='uint32')
    # Convert spectral irradiance values from counts to uE/m^2/s
    wavelengths = [412, 444, 490, 510, 555, 620, 683]
    Ed = opt_ocr507_irradiance(channels, dev.coeffs['offset'], dev.coeffs['scale'], dev.coeffs['immersion_factor'])

    # convert voltages and temperature to engineering units
    df['input_voltage'].apply(lambda x: x * 0.03)
    df['analog_rail_voltage'].apply(lambda x: x * 0.03)
    df['internal_temperature'].apply(lambda x: -50 + x * 0.5)

    # setup some further parameters for use with the OMTP class
    df['deploy_id'] = deployment
    df['site_depth'] = site_depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['z'] = -1 * z_from_p(df['depth'], lat)               # uses CTD pressure record interpolated into SPKIR record
    df['t'] = (df.time.values.astype('int64') * 10 ** -9)[0]  # set profile time to time of first data record
    df['precise_time'] = np.int64(df.pop('time')) * 10 ** -9  # rename time record
    df['station'] = 0

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    spkir_attr = CSPP

    spkir_attr['global'] = dict_update(spkir_attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    spkir_attr = dict_update(spkir_attr, CSPP_SPKIR)

    nc = OMTP.from_dataframe(df, outfile, attributes=spkir_attr)
    nc.close()

    # re-open the netcdf file and add the raw channels, the downwelling irradiance and the wavelengths with the
    # additional dimension of the measurement wavelengths.
    nc = Dataset(outfile, 'a')
    nc.createDimension('wavelengths', 7)

    d = nc.createVariable('wavelengths', 'i', ('wavelengths',))
    d.setncatts(spkir_attr['wavelengths'])
    d[:] = wavelengths

    d = nc.createVariable('raw_channels', 'u4', ('time', 'z', 'station', 'wavelengths',))
    d.setncatts(spkir_attr['raw_channels'])
    d[:] = channels

    d = nc.createVariable('irradiance', 'f', ('time', 'z', 'station', 'wavelengths',))
    d.setncatts(spkir_attr['irradiance'])
    d[:] = Ed

    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
