#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_spkir
@file cgsn_processing/process/proc_spkir.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for SPKIR from JSON formatted source data
"""
import json
import numpy as np
import os
import pandas as pd
import re

from netCDF4 import Dataset
from pocean.utils import dict_update
from pocean.dsg.timeseries.om import OrthogonalMultidimensionalTimeseries as OMTs

from cgsn_processing.process.common import Coefficients, inputs, json2df, df2omtdf
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_spkir import SPKIR
from pyseas.data.opt_functions import opt_ocr507_irradiance


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the SPKIR factory calibration coefficients for a unit. Values come from either a serialized object
        created per instrument and deployment (calibration coefficients do not change in the middle of a deployment),
        or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from a SPKIR calibration file already parsed and stored on Github as a CSV files. Note, 
        the formatting of those files puts some constraints on this process. If someone has a cleaner method, 
        I'm all in favor... 
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # immersion, scale and offset correction factors
            if row[1] == 'CC_immersion_factor':
                coeffs['immersion_factor'] = np.array(json.loads(row[2]))
            if row[1] == 'CC_offset':
                coeffs['offset'] = np.array(json.loads(row[2]))
            if row[1] == 'CC_scale':
                coeffs['scale'] = np.array(json.loads(row[2]))

        # save the resulting dictionary
        self.coeffs = coeffs


def main(argv=None):
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # load the json data file and return a panda dataframe, adding a default depth and the deployment ID
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
        csv_url = find_calibration('SPKIR', str(df.serial_number[0]), (df.time.values.astype('int64') * 10**-9)[0])
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
        else:
            print('A source for the SPKIR calibration coefficients for {} could not be found'.format(infile))
            return None

    # pop the raw_channels array out of the dataframe (will put it back in later)
    channels = np.array(np.vstack(df.pop('raw_channels')), dtype='uint32')
    # Convert spectral irradiance values from counts to uE/m^2/s
    wavelengths = [412, 444, 490, 510, 555, 620, 683]
    Ed = opt_ocr507_irradiance(channels, dev.coeffs['offset'], dev.coeffs['scale'], dev.coeffs['immersion_factor'])

    # convert voltages and temperature to engineering units
    df['input_voltage'].apply(lambda x: x * 0.03)
    df['analog_rail_voltage'].apply(lambda x: x * 0.03)
    df['internal_temperature'].apply(lambda x: -50 + x * 0.5)

    # convert the dataframe to a format suitable for the pocean OMTs
    df['deploy_id'] = deployment
    df = df2omtdf(df, lat, lon, depth)

    # add to the global attributes for the SPKIR
    attrs = SPKIR
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTs.from_dataframe(df, outfile, attributes=attrs)
    nc.close()

    # re-open the netcdf file and add the raw channels, the downwelling irradiance and the wavelengths with the
    # additional dimension of the measurement wavelengths.
    nc = Dataset(outfile, 'a')
    nc.createDimension('wavelengths', 7)

    d = nc.createVariable('wavelengths', 'i', ('wavelengths',))
    d.setncatts(attrs['wavelengths'])
    d[:] = wavelengths

    d = nc.createVariable('raw_channels', 'u4', ('station', 'time', 'wavelengths',))
    d.setncatts(attrs['raw_channels'])
    d[:] = channels

    d = nc.createVariable('irradiance', 'f', ('station', 'time', 'wavelengths',))
    d.setncatts(attrs['irradiance'])
    d[:] = Ed

    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
