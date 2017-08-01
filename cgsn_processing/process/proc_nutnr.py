#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_nutnr
@file cgsn_processing/process/proc_nutnr.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Nitrate concentration data from the NUTNR
"""
import json
import numpy as np
import os
import pandas as pd
import re

from netCDF4 import Dataset
from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs
from scipy.interpolate import interp1d

from cgsn_processing.process.common import Coefficients, inputs, json2df, df2omtdf
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_nutnr import NUTNR

from pyseas.data.nit_functions import ts_corrected_nitrate


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the NUTNR pure water calibration coefficients for a unit. Values come from either a serialized object
        created per instrument and deployment (calibration coefficients do not change in the middle of a deployment),
        or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from a NUTNR calibration file already parsed and stored on Github as a CSV files. Note, the
        formatting of those files puts some constraints on this process. If someone has a cleaner method, I'm all in
        favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            if row[1] == 'CC_cal_temp':
                coeffs['cal_temp'] = float(row[2])

            if row[1] == 'CC_di':
                coeffs['di'] = np.array(json.loads(row[2]))

            if row[1] == 'CC_eno3':
                coeffs['eno3'] = np.array(json.loads(row[2]))

            if row[1] == 'CC_eswa':
                coeffs['eswa'] = np.array(json.loads(row[2]))

            if row[1] == 'CC_lower_wavelength_limit_for_spectra_fit':
                coeffs['wllower'] = int(row[2])

            if row[1] == 'CC_upper_wavelength_limit_for_spectra_fit':
                coeffs['wlupper'] = int(row[2])

            if row[1] == 'CC_wl':
                coeffs['wl'] = np.array(json.loads(row[2]))

        # save the resulting dictionary
        self.coeffs = coeffs


def main(argv=None):
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.split(args.outfile)
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

    if args.switch == 1:    # dataset includes the full spectral output
        # check for the source of calibration coeffs and load accordingly
        coeff_file = os.path.abspath(args.coeff_file)
        dev = Calibrations(coeff_file)  # initialize calibration class
        if os.path.isfile(coeff_file):
            # we always want to use this file if it exists
            dev.load_coeffs()
        else:
            # load from the CI hosted CSV files
            csv_url = find_calibration('NUTNR', df.serial_number[0], (df.time.values.astype('int64') / 1e9)[0])
            if csv_url:
                dev.read_csv(csv_url)
                dev.save_coeffs()
            else:
                raise Exception('A source for the NUTNR calibration coefficients could not be found')

        # pop the raw_channels array out of the dataframe (will put it back in later)
        channels = np.array(np.vstack(df.pop('channel_measurements')))
        # create the wavelengths array
        wavelengths = dev.coeffs['wl']

        # Merge the co-located CTD temperature and salinity data and calculate the corrected nitrate concentration
        ctd_file = re.sub('nutnr', 'ctdbp', infile)
        ctd = json2df(ctd_file)
        if not ctd.empty:
            # interpolate temperature and salinity data from the CTD into the NUTNR record for calculations
            degC = interp1d(ctd.time.values.astype('int64'), ctd.temperature.values, bounds_error=False)
            df['temperature'] = degC(df.time.values.astype('int64'))
            psu = interp1d(ctd.time.values.astype('int64'), ctd.salinity, bounds_error=False)
            df['salinity'] = psu(df.time.values.astype('int64'))

            # Calculate the corrected nitrate concentration (uM) accounting for temperature and salinity and the pure
            # water calibration values.
            df['corrected_nitrate'] = ts_corrected_nitrate(dev.coeffs['cal_temp'], dev.coeffs['wl'], dev.coeffs['eno3'],
                                                           dev.coeffs['eswa'], dev.coeffs['di'], df['seawater_dark'],
                                                           df['temperature'], df['salinity'], channels,
                                                           df['measurement_type'], dev.coeffs['wllower'],
                                                           dev.coeffs['wlupper'])
        else:
            df['temperature'] = np.nan
            df['salinity'] = np.nan
            df['corrected_nitrate'] = np.nan

    else:   # dataset does not include the full spectral array. Pad out with fill values to keep datasets consistent
        channels = np.ones(256) * -999999999
        wavelengths = np.arange(0, 256) * np.nan
        df['temperature'] = np.nan
        df['salinity'] = np.nan
        df['corrected_nitrate'] = np.nan

    # convert the dataframe to a format suitable for the pocean OMTs, adding the deployment name
    df['deploy_id'] = deployment
    df = df2omtdf(df, lat, lon, depth)

    # add to the global attributes for the NUTNR
    attrs = NUTNR
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTs.from_dataframe(df, outfile, attributes=attrs)
    nc.close()

    # re-open the netcdf file and add the raw channel measurements and the wavelengths with the additional dimension
    # of the measurement wavelengths.
    nc = Dataset(outfile, 'a')
    nc.createDimension('wavelengths', len(wavelengths))

    d = nc.createVariable('wavelengths', 'f', ('wavelengths',))
    d.setncatts(attrs['wavelengths'])
    d[:] = wavelengths

    d = nc.createVariable('channel_measurements', 'i', ('time', 'station', 'wavelengths',))
    d.setncatts(attrs['channel_measurements'])
    d[:] = channels

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
