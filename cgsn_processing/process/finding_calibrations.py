#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.finding_calibrations
@file cgsn_processing/process/finding_calibrations.py
@author Christopher Wingard
@brief Find the most applicable calibration file for an instrument
"""
import datetime
import netrc
import pandas as pd
import re
import requests
import warnings

from calendar import timegm
from pytz import timezone
from cgsn_processing.process.common import Coefficients

# set the base URL for the OOI asset management listing of calibration files and a regex for the CSV files
GIT = 'https://api.github.com/repos'
CSV = re.compile(r'.*\.csv')


# load the GitHub API read-only access token
headers = None  # default token
try:
    nrc = netrc.netrc()
    auth = nrc.authenticators('api.github.com')
    if auth is None:
        warnings.warn('No entry found for the GitHub API token in the users .netrc file, consider adding to improve '
                      'access to calibration coefficients')
    else:
        headers = {'Authentication': 'token ' + auth[2]}
except FileNotFoundError as e:
    warnings.warn('No .netrc file found in the users home directory. Consider creating and adding a GitHub API '
                  'token to improve access to calibration coefficients')


def list_directories(url, tag=''):
    page = requests.get(url, headers=headers).json()
    urls = ['{}/{}'.format(url, item['name']) for item in page if tag in item['name']]
    return urls


def find_calibration(inst_class, inst_serial, sampling_date):
    # find the links for the instrument class we are after
    links = list_directories('{}/oceanobservatories/asset-management/contents/calibration'.format(GIT), inst_class)
    tdiff = []
    flist = []

    # if successful, start to zero in on our instrument
    if links:
        for link in links:
            # get the list of cal CSVs for this instrument
            if inst_serial.isdigit():
                # almost all serial numbers are comprised of digits only, but there are a few exceptions
                instrmts = list_directories(link, '-{}__'.format(inst_serial.rjust(5, '0')))
            else:
                # for the few exceptions (SAMIs), we need to look for the serial number as a string
                instrmts = list_directories(link, '-{}__'.format(inst_serial.upper()))

            # if we have found some calibration files, start to zero in on the one we want
            if instrmts:
                for inst in instrmts:
                    # only look at .csv files
                    if not CSV.match(inst):
                        continue

                    # we are getting close, now we need to pull out the date stamp
                    dstr = re.sub('.csv', '', re.split('__', inst)[1])

                    # convert the date string of the file into a datetime object
                    dt = datetime.datetime.strptime(dstr, '%Y%m%d')
                    utc = dt.replace(tzinfo=timezone('UTC'))

                    # calculate the epoch time as seconds since 1970-01-01 in UTC
                    epts = timegm(utc.timetuple()) + (utc.microsecond / 1e6)

                    # test the type of the sampling_date and convert to match epts if needed
                    if type(sampling_date) is pd.Timestamp:
                        # convert the sampling date to epoch time
                        sampling_date = timegm(sampling_date.timetuple())

                    # now compare that time to the sampling date from the data
                    flist.append(inst)
                    tdiff.append(round((sampling_date - epts) / 60 / 60 / 24))

    if tdiff:
        try:
            # check the resulting list of files and time differences for the closest file that precedes our deployment
            m = min(i for i in tdiff if i >= 0)
        except ValueError:
            print("Calibration file pre-dating the sampling date could not be found, returning empty csv string")
            csv = None
        else:
            # assemble the csv URL, adjusting for the fact we want the raw content
            csv = re.sub('api.github.com/repos', 'raw.githubusercontent.com', flist[tdiff.index(m)])
            csv = re.sub('contents', 'master', csv)
    else:
        csv = None

    return csv

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
            if row.iloc[1] == 'CC_dark_counts_cdom':
                coeffs['dark_cdom'] = row.iloc[2]
            if row.iloc[1] == 'CC_scale_factor_cdom':
                coeffs['scale_cdom'] = row.iloc[2]

            if row.iloc[1] == 'CC_dark_counts_chlorophyll_a':
                coeffs['dark_chla'] = row.iloc[2]
            if row.iloc[1] == 'CC_scale_factor_chlorophyll_a':
                coeffs['scale_chla'] = row.iloc[2]

            if row.iloc[1] == 'CC_dark_counts_volume_scatter':
                coeffs['dark_beta'] = row.iloc[2]
            if row.iloc[1] == 'CC_scale_factor_volume_scatter':
                coeffs['scale_beta'] = row.iloc[2]

            # optical backscatter correction factors
            if row.iloc[1] == 'CC_angular_resolution':
                coeffs['chi_factor'] = row.iloc[2]
            if row.iloc[1] == 'CC_measurement_wavelength':
                coeffs['wavelength'] = row.iloc[2]
            if row.iloc[1] == 'CC_scattering_angle':
                coeffs['scatter_angle'] = row.iloc[2]

            # turbidity calculation factors
            if row.iloc[1] == 'CC_dark_counts_turbd':
                coeffs['dark_turbd'] = int(row.iloc[2])
            if row.iloc[1] == 'CC_scale_factor_turbd':
                coeffs['scale_turbd'] = float(row.iloc[2])

        # save the resulting dictionary
        self.coeffs = coeffs
