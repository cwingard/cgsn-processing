#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_zplsc
@file cgsn_processing/process/proc_zplsc.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the ZPLSC data from JSON formatted source data
"""
import json
import numpy as np
import os
import pandas as pd
import re

from datetime import datetime
from netCDF4 import Dataset
from pocean.dsg.timeseriesProfile.om import OrthogonalMultidimensionalTimeseriesProfile as OMTp
from pocean.utils import dict_update
from pytz import timezone

from cgsn_processing.process.common import Coefficients, inputs, json2df, df2omtdf
# from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_zplsc import ZPLSC


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the ZPLSC factory calibration coefficients for a unit. Values come from either a serialized object
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
        # TODO: This is a temporary placeholder while we figure out the needed data and structure required
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # factory calibration values
            if row[1] == 'CC_EL_max':
                coeffs['EL_max'] = np.array(json.loads(row[2]))

        # save the resulting dictionary
        #self.coeffs = coeffs
        self.coeffs = {}


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
    bin_size = args.bin_size

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # TODO: Need to determine the appropriate structure and content of the calibration data. Skip this section for now.
    #coeff_file = os.path.abspath(args.coeff_file)
    #dev = Calibrations(coeff_file)  # initialize calibration class
    #
    ## check for the source of calibration coeffs and load accordingly
    #if os.path.isfile(coeff_file):
    #    # we always want to use this file if it exists
    #    dev.load_coeffs()
    #else:
    #    # load from the CI hosted CSV files
    #    csv_url = find_calibration('SPKIR', str(df.serial_number[0]), (df.time.values.astype('int64') * 10**-9)[0])
    #    if csv_url:
    #        dev.read_csv(csv_url)
    #        dev.save_coeffs()
    #    else:
    #        raise Exception('A source for the SPKIR calibration coefficients could not be found')

    # TODO: Once we have a structure for calibration coefficients, process the data from raw echo intensity to Sv

    # compare the instrument clock (from the transmission_date_string) to the GPS based DCL time stamp
    offset = []
    for i in range(len(df['time'])):
        zplsc = datetime.strptime(df['transmission_date_string'][i], "%Y%m%d%H%M%S")
        zplsc.replace(tzinfo=timezone('UTC'))
        offset.append((zplsc - df['time'][i]).total_seconds())

    df['time_offset'] = offset

    # pop the data arrays out of the dataframe (will put most of them back in later)
    profiles_channel_1 = np.array(np.vstack(df.pop('profiles_freq1')))
    profiles_channel_2 = np.array(np.vstack(df.pop('profiles_freq2')))
    profiles_channel_3 = np.array(np.vstack(df.pop('profiles_freq3')))
    profiles_channel_4 = np.array(np.vstack(df.pop('profiles_freq4')))
    minimum_values = np.array(np.vstack(df.pop('minimum_values')))
    number_bins = np.array(np.vstack(df.pop('number_bins')))
    frequencies = np.array(np.vstack(df.pop('frequencies')))
    _ = df.pop('phase')  # discard phase number, we only use the one.
    _ = df.pop('tilts')  # discard tilts array as unit is at 90 degrees and unusable

    # add the minimum values back into the raw echo intensities
    profiles_channel_1 = profiles_channel_1 + np.atleast_2d(minimum_values[:, 0]).T
    profiles_channel_2 = profiles_channel_2 + np.atleast_2d(minimum_values[:, 1]).T
    profiles_channel_3 = profiles_channel_3 + np.atleast_2d(minimum_values[:, 2]).T
    profiles_channel_4 = profiles_channel_4 + np.atleast_2d(minimum_values[:, 3]).T

    # create an approximate depth axis for the dataset based on the bin size, the maximum number of bins, and the
    # mounting angle of the transducers.
    bins = (np.arange(max(number_bins[0, :])) * bin_size) * np.cos(np.radians(15.0))
    bin_depth = depth - 1.0 - (bins + (bin_size / 2.0))

    # pad the profiles with -999999999, if needed, so we can use a common bin_depth axis
    pad = max(number_bins[0, :]) - number_bins[0, 0]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_1 = np.concatenate((profiles_channel_1, np.tile(fill, (len(df.time), 1))), axis=1)

    pad = max(number_bins[0, :]) - number_bins[0, 1]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_2 = np.concatenate((profiles_channel_2, np.tile(fill, (len(df.time), 1))), axis=1)

    pad = max(number_bins[0, :]) - number_bins[0, 2]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_3 = np.concatenate((profiles_channel_3, np.tile(fill, (len(df.time), 1))), axis=1)

    pad = max(number_bins[0, :]) - number_bins[0, 3]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_4 = np.concatenate((profiles_channel_4, np.tile(fill, (len(df.time), 1))), axis=1)

    # break the frequencies array apart
    df['channel_1_freq'] = frequencies[:, 0]
    df['channel_2_freq'] = frequencies[:, 1]
    df['channel_3_freq'] = frequencies[:, 2]
    df['channel_4_freq'] = frequencies[:, 3]

    # convert the dataframe to a format suitable for the pocean OMTs
    df['deploy_id'] = deployment
    df = df2omtdf(df, lat, lon, depth)

    # Setup and update the attributes for the resulting NetCDF file
    attr = ZPLSC
    attr['global'] = dict_update(attr['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTp.from_dataframe(df, outfile, attributes=attr)
    nc.close()

    # Now reopen the NetCDF file and add the additional multi-dimensioned data
    nc = Dataset(outfile, 'a')

    # Create the bin_depth dimension ...
    nc.createDimension('bin_depth', len(bin_depth))
    d = nc.createVariable('bin_depth', 'f', ('bin_depth',))
    d.setncatts(attr['bin_depth'])
    d[:] = bin_depth

    # ... and add the profiles
    d = nc.createVariable('profiles_channel_1', 'i', ('time', 'z', 'station', 'bin_depth',), fill_value=-999999999)
    d.setncatts(attr['profiles_channel_1'])
    d[:] = profiles_channel_1

    d = nc.createVariable('profiles_channel_2', 'i', ('time', 'z', 'station', 'bin_depth',), fill_value=-999999999)
    d.setncatts(attr['profiles_channel_2'])
    d[:] = profiles_channel_2

    d = nc.createVariable('profiles_channel_3', 'i', ('time', 'z', 'station', 'bin_depth',), fill_value=-999999999)
    d.setncatts(attr['profiles_channel_3'])
    d[:] = profiles_channel_3

    d = nc.createVariable('profiles_channel_4', 'i', ('time', 'z', 'station', 'bin_depth',), fill_value=-999999999)
    d.setncatts(attr['profiles_channel_4'])
    d[:] = profiles_channel_4

    # sync it up and close
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
