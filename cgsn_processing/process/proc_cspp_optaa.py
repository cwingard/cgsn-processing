#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_optaa
@file cgsn_processing/process/proc_cspp_optaa.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP OPTAA data from JSON formatted source data
"""
import numpy as np
import os
import re

from netCDF4 import Dataset
from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs
from scipy.interpolate import interp1d

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_optaa import Calibrations, apply_dev, apply_scatcorr, apply_tscorr
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_OPTAA


def main(argv=None):
    # load the input arguments
    args = inputs(argv)
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

    # check for the source of calibration coeffs and load accordingly
    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('OPTAA', str(df.serial_number[0]), (df.time.values.astype('int64') * 10**-9)[0])
        if csv_url:
            # load from the CI hosted CSV files
            tca_url = re.sub('.csv', '__CC_taarray.ext', csv_url)
            tcc_url = re.sub('.csv', '__CC_tcarray.ext', csv_url)
            dev.read_devurls(csv_url, tca_url, tcc_url)
            dev.save_coeffs()
        else:
            print('A source for the OPTAA calibration coefficients for {} could not be found'.format(infile))
            return None

    # Merge the co-located CTD temperature and salinity data and calculate the temperature and salinity corrections
    ctd_file = re.sub('optaa', 'ctdpf', infile)
    ctd_file = re.sub('ACS_ACS', 'PPB_CTD', ctd_file)
    ctd = json2df(ctd_file)
    if not ctd.empty:
        # interpolate temperature, pressure and salinity data from the CTD into the OPTAA record for calculations
        degC = interp1d(ctd.time.values.astype('int64'), ctd.temperature.values, bounds_error=False)
        df['temperature'] = degC(df.time.values.astype('int64'))

        psu = interp1d(ctd.time.values.astype('int64'), ctd.salinity, bounds_error=False)
        df['salinity'] = psu(df.time.values.astype('int64'))

        dbar = interp1d(ctd.time.values.astype('int64'), ctd.pressure, bounds_error=False)
        df['depth'] = dbar(df.time.values.astype('int64'))
    else:
        # there was no CTD data, and thus no pressure record or temperature and salinity available, ending early
        return None

    # apply the device file conversions from counts to m^-1
    df.drop(df[df.num_wavelengths != dev.coeffs['num_wavelengths']].index, inplace=True)
    df = apply_dev(df, dev.coeffs)
    # apply the temperature and salinity corrections
    df = apply_tscorr(df, dev.coeffs, df['temperature'], df['salinity'])
    # finally apply the scatter corrections
    df = apply_scatcorr(df, dev.coeffs)

    # setup some further parameters for use with the OMTs class
    df['deploy_id'] = deployment
    df['z'] = depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['t'] = df.pop('time')
    df['station'] = 0
    df.rename(columns={'depth': 'ctd_depth'}, inplace=True)

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # Setup and update the attributes for the resulting NetCDF file
    attr = CSPP

    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    attr = dict_update(attr, CSPP_OPTAA)

    # pop arrays out of the dataframe (will put them into the netcdf file later)
    c_ref = np.array(np.vstack(df.pop('c_reference_raw')))
    a_ref = np.array(np.vstack(df.pop('a_reference_raw')))
    c_sig = np.array(np.vstack(df.pop('c_signal_raw')))
    a_sig = np.array(np.vstack(df.pop('a_signal_raw')))
    apd = np.array(np.vstack(df.pop('apd')))
    apd_ts = np.array(np.vstack(df.pop('apd_ts')))
    apd_ts_s = np.array(np.vstack(df.pop('apd_ts_s')))
    cpd = np.array(np.vstack(df.pop('cpd')))
    cpd_ts = np.array(np.vstack(df.pop('cpd_ts')))

    nc = OMTs.from_dataframe(df, outfile, attributes=attr)
    nc.close()

    # re-open the netcdf file and add the raw and calculated measurements and the wavelengths with the additional
    # dimension of the measurement wavelengths.
    nc = Dataset(outfile, 'a')

    # create a new dimension for the wavelength arrays, padded out to a size of 100 to account for the variable number
    # of wavelengths, and then create arrays for the the 'a' and 'c'-channel wavelengths
    nc.createDimension('wavelengths', size=100)
    d = nc.createVariable('wavelengths', 'i', ('wavelengths',))
    d[:] = np.arange(100)
    d.setncatts(attr['wavelengths'])

    pad = 100 - dev.coeffs['num_wavelengths']
    fill_int = (np.ones(pad) * -999999999).astype(np.int32)
    fill_nan = np.ones(pad) * np.nan

    d = nc.createVariable('a_wavelengths', 'f', ('wavelengths',))
    d.setncatts(attr['a_wavelengths'])
    last = dev.coeffs['a_wavelengths'][-1]
    step = np.median(np.diff(dev.coeffs['a_wavelengths']))
    wave_pad = (np.arange(pad) + 1 * step) + last
    d[:] = np.concatenate((dev.coeffs['a_wavelengths'], wave_pad)).tolist()

    d = nc.createVariable('c_wavelengths', 'f', ('wavelengths',))
    d.setncatts(attr['c_wavelengths'])
    last = dev.coeffs['c_wavelengths'][-1]
    step = np.median(np.diff(dev.coeffs['c_wavelengths']))
    wave_pad = (np.arange(pad) + 1 * step) + last
    d[:] = np.concatenate((dev.coeffs['c_wavelengths'], wave_pad)).tolist()

    # now add all the popped arrays back in
    d = nc.createVariable('a_reference_raw', 'i', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['a_reference_raw'])
    d[:] = np.concatenate((a_ref, np.tile(fill_int, (len(df.t), 1))), axis=1).astype(np.int32)

    d = nc.createVariable('a_signal_raw', 'i', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['a_signal_raw'])
    d[:] = np.concatenate((a_sig, np.tile(fill_int, (len(df.t), 1))), axis=1).astype(np.int32)

    d = nc.createVariable('c_reference_raw', 'i', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['c_reference_raw'])
    d[:] = np.concatenate((c_ref, np.tile(fill_int, (len(df.t), 1))), axis=1).astype(np.int32)

    d = nc.createVariable('c_signal_raw', 'i', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['c_signal_raw'])
    d[:] = np.concatenate((c_sig, np.tile(fill_int, (len(df.t), 1))), axis=1).astype(np.int32)

    d = nc.createVariable('apd', 'f', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['apd'])
    d[:] = np.concatenate((apd, np.tile(fill_nan, (len(df.t), 1))), axis=1)

    d = nc.createVariable('apd_ts', 'f', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['apd_ts'])
    d[:] = np.concatenate((apd_ts, np.tile(fill_nan, (len(df.t), 1))), axis=1)

    d = nc.createVariable('apd_ts_s', 'f', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['apd_ts_s'])
    d[:] = np.concatenate((apd_ts_s, np.tile(fill_nan, (len(df.t), 1))), axis=1)

    d = nc.createVariable('cpd', 'f', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['cpd'])
    d[:] = np.concatenate((cpd, np.tile(fill_nan, (len(df.t), 1))), axis=1)

    d = nc.createVariable('cpd_ts', 'f', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['cpd_ts'])
    d[:] = np.concatenate((cpd_ts, np.tile(fill_nan, (len(df.t), 1))), axis=1)

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
