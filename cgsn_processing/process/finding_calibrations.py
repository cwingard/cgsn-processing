#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.finding_calibrations
@file cgsn_processing/process/finding_calibrations.py
@author Christopher Wingard
@brief Find the most applicable calibration file for an instrument
"""
import datetime
import pandas as pd
import re
import requests

from bs4 import BeautifulSoup
from calendar import timegm
from pytz import timezone

# set the base URL for the OOI asset management listing of calibration files and a regex for the CSV files
GIT = 'https://github.com'
CSV = re.compile('.*\.csv')


def list_links(url, tag=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    pattern = re.compile(str(tag))
    return [node.get('href') for node in soup.find_all('a', text=pattern)]


def find_calibration(inst_class, inst_serial, sampling_date):
    # find the links for the instrument class we are after
    links = list_links('{}/ooi-integration/asset-management/tree/master/calibration/'.format(GIT), inst_class)
    tdiff = []
    flist = []

    # if successful, start to zero in on our instrument
    if links:
        for link in links:
            instrmts = list_links('{}/{}/'.format(GIT, link), '-{}__'.format(inst_serial.rjust(5, '0')))
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
            csv = '{}{}'.format('https://raw.githubusercontent.com', flist[tdiff.index(m)])
            csv = re.sub('/blob', '', csv)
    else:
        csv = None

    return csv
