#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_nutnr
@file cgsn_processing/process/proc_cspp_nutnr.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP NUTNR data from JSON formatted source data
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
from cgsn_processing.process.proc_nutnr import Calibrations
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_NUTNR

from pyseas.data.nit_functions import ts_corrected_nitrate


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

    # check for the source of calibration coeffs and load accordingly
    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('NUTNR', args.serial, (df.time.values.astype('int64') * 10**-9)[0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            raise Exception('A source for the NUTNR calibration coefficients could not be found')

    # Merge the co-located CTD temperature and salinity data and calculate the corrected nitrate concentration
    ctd_file = re.sub('nutnr', 'ctdpf', infile)
    ctd_file = re.sub('SNA_SNA', 'PPB_CTD', ctd_file)

    ctd = json2df(ctd_file)
    if not ctd.empty:
        # interpolate temperature, pressure and salinity data from the CTD into the NUTNR record for calculations
        degC = interp1d(ctd.time.values.astype('int64'), ctd.temperature.values, bounds_error=False)
        df['temperature'] = degC(df.time.values.astype('int64'))

        psu = interp1d(ctd.time.values.astype('int64'), ctd.salinity, bounds_error=False)
        df['salinity'] = psu(df.time.values.astype('int64'))

        dbar = interp1d(ctd.time.values.astype('int64'), ctd.pressure, bounds_error=False)
        df['depth'] = dbar(df.time.values.astype('int64'))

        # create the wavelengths array and the raw channels
        wavelengths = (dev.coeffs['wl']).astype(np.float)
        raw_channels = np.array(np.vstack(df['channel_measurements'].values))

        # Calculate the corrected nitrate concentration (uM) accounting for temperature and salinity and the pure
        # water calibration values.
        df['corrected_nitrate'] = ts_corrected_nitrate(dev.coeffs['cal_temp'], wavelengths, dev.coeffs['eno3'],
                                                       dev.coeffs['eswa'], dev.coeffs['di'], df['dark_value'],
                                                       df['temperature'], df['salinity'], raw_channels,
                                                       df['measurement_type'])
    else:
        # there was no CTD data, and thus no pressure record or temperature and salinity available, ending early
        return None

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

    # pop the raw_channels array out of the dataframe (will put it back in later)
    raw_channels = np.array(np.vstack(df.pop('channel_measurements')))

    # Setup and update the attributes for the resulting NetCDF file
    attr = CSPP

    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })
    attr = dict_update(attr, CSPP_NUTNR)

    nc = OMTs.from_dataframe(df, outfile, attributes=attr)
    nc.close()

    # re-open the netcdf file and add the raw channel measurements and the wavelengths with the additional dimension
    # of the measurement wavelengths.
    nc = Dataset(outfile, 'a')
    nc.createDimension('wavelengths', len(wavelengths))

    d = nc.createVariable('wavelengths', 'f', ('wavelengths',))
    d.setncatts(attr['wavelengths'])
    d[:] = wavelengths

    d = nc.createVariable('channel_measurements', 'i', ('time', 'station', 'wavelengths',))
    d.setncatts(attr['channel_measurements'])
    d[:] = raw_channels

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
