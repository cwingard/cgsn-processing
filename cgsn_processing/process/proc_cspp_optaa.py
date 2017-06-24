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

from gsw import z_from_p
from netCDF4 import Dataset
from pocean.utils import dict_update
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTp
from scipy.interpolate import interp1d

from cgsn_processing.process.common import inputs, json2df, reset_long
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_optaa import Calibrations, apply_dev, apply_scatcorr, apply_tscorr
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_OPTAA


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

    # check for the source of calibration coeffs and load accordingly
    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('OPTAA', df.serial_number[0], (df.time.values.astype('int64') * 10**-9)[0])
        if csv_url:
            # load from the CI hosted CSV files
            tca_url = re.sub('.csv', '__CC_taarray.ext', csv_url)
            tcc_url = re.sub('.csv', '__CC_tcarray.ext', csv_url)
            dev.read_devurls(csv_url, tca_url, tcc_url)
            dev.save_coeffs()
        else:
            raise Exception('A source for the OPTAA calibration coefficients could not be found')

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
        df = df[np.isnan(df.depth.values) != 1]  # remove rows with NaN for depth
    else:
        # there was no CTD data, and thus no pressure record or temperature and salinity available, ending early
        return None

    # apply the device file conversions from counts to m^-1
    df = apply_dev(df, dev.coeffs)
    # apply the temperature and salinity corrections
    df = apply_tscorr(df, dev.coeffs, df['temperature'], df['salinity'])
    # finally apply the scatter corrections
    df = apply_scatcorr(df, dev.coeffs)

    # setup some further parameters for use with the OMTp class
    df['deploy_id'] = deployment
    df['site_depth'] = site_depth
    profile_id = re.sub('\D+', '', fname)
    df['profile_id'] = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])
    df['x'] = lon
    df['y'] = lat
    df['z'] = -1 * z_from_p(df['depth'], lat)               # uses CTD pressure record interpolated into OPTAA record
    df['t'] = df.pop('time')[0]                             # set profile time to time of first data record
    df['precise_time'] = df.t.values.astype('int64') / 1e9  # create a precise time record
    df['station'] = 0

    # make sure all ints are represented as int32 instead of int64
    df = reset_long(df)

    # clean-up duplicate depth values
    df.drop_duplicates(subset='depth', keep='first', inplace=True)

    # Setup and update the attributes for the resulting NetCDF file
    optaa_attr = CSPP

    optaa_attr['global'] = dict_update(optaa_attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    optaa_attr = dict_update(optaa_attr, CSPP_OPTAA)

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

    nc = OMTp.from_dataframe(df, outfile, attributes=optaa_attr)
    nc.close()

    # re-open the netcdf file and add the raw and calculated measurements and the wavelengths with the additional
    # dimension of the measurement wavelengths.
    nc = Dataset(outfile, 'a')

    # create a new dimension for the wavelength array, padded out to a size of 100 to account for the variable number
    # of wavelengths, and then create arrays for the the 'a' and 'c'-channel wavelengths
    nc.createDimension('a_wavelengths', size=100)
    nc.createDimension('c_wavelengths', size=100)
    pad = 100 - dev.coeffs['num_wavelengths']
    fill = np.ones(pad) * -999999999.

    d = nc.createVariable('a_wavelengths', 'f', ('a_wavelengths',))
    d.setncatts(optaa_attr['a_wavelengths'])
    d[:] = np.concatenate((dev.coeffs['a_wavelengths'], fill)).tolist()

    d = nc.createVariable('c_wavelengths', 'f', ('c_wavelengths',))
    d.setncatts(optaa_attr['c_wavelengths'])
    d[:] = np.concatenate((dev.coeffs['c_wavelengths'], fill)).tolist()

    # now add all the popped arrays back in
    d = nc.createVariable('a_reference_raw', 'i', ('time', 'z', 'station', 'a_wavelengths',))
    d.setncatts(optaa_attr['a_reference_raw'])
    d[:] = np.concatenate((a_ref, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('a_signal_raw', 'i', ('time', 'z', 'station', 'a_wavelengths',))
    d.setncatts(optaa_attr['a_signal_raw'])
    d[:] = np.concatenate((a_sig, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('c_reference_raw', 'i', ('time', 'z', 'station', 'c_wavelengths',))
    d.setncatts(optaa_attr['c_reference_raw'])
    d[:] = np.concatenate((c_ref, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('c_signal_raw', 'i', ('time', 'z', 'station', 'c_wavelengths',))
    d.setncatts(optaa_attr['c_signal_raw'])
    d[:] = np.concatenate((c_sig, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('apd', 'f', ('time', 'z', 'station', 'a_wavelengths',))
    d.setncatts(optaa_attr['apd'])
    d[:] = np.concatenate((apd, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('apd_ts', 'f', ('time', 'z', 'station', 'a_wavelengths',))
    d.setncatts(optaa_attr['apd_ts'])
    d[:] = np.concatenate((apd_ts, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('apd_ts_s', 'f', ('time', 'z', 'station', 'a_wavelengths',))
    d.setncatts(optaa_attr['apd_ts_s'])
    d[:] = np.concatenate((apd_ts_s, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('cpd', 'f', ('time', 'z', 'station', 'c_wavelengths',))
    d.setncatts(optaa_attr['cpd'])
    d[:] = np.concatenate((cpd, np.tile(fill, (len(df.t), 1))), axis=1)

    d = nc.createVariable('cpd_ts', 'f', ('time', 'z', 'station', 'c_wavelengths',))
    d.setncatts(optaa_attr['cpd_ts'])
    d[:] = np.concatenate((cpd_ts, np.tile(fill, (len(df.t), 1))), axis=1)

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
