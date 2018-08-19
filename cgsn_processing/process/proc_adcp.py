#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_adcp
@file cgsn_processing/process/proc_adcp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for ADCP from JSON formatted source data
"""
import json
import numpy as np
import os
import pandas as pd
import xarray as xr
import re

from cgsn_processing.process.common import dict_update, inputs
from cgsn_processing.process.configs.attr_adcp import ADCP, ADCP_PD0


def json_sub2df(data, sub):
    """
    Take a JSON formatted data object, read in as a dict, pull out the subarray of interest, and return the results as
    a panda data frame.
    """
    df = pd.DataFrame(data[sub])
    if df.empty:
        return df

    df['time'] = pd.to_datetime(data['time'], unit='s')
    df.set_index('time', drop=True, inplace=True)

    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

    return df


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
    adcp_type = args.switch

    # load the json data file
    with open(infile) as jf:
        data = json.load(jf)

    # load the fixed and variable leader data packets
    df = json_sub2df(data, 'fixed')
    fx = xr.Dataset.from_dataframe(df)

    df = json_sub2df(data, 'variable')
    vbl = xr.Dataset.from_dataframe(df)

    # create the time and bin_number coordinate arrays
    time = np.array(data['time'])
    bin_number = np.arange(data['fixed']['num_cells'][0] - 1)

    # drop real-time clock arrays 1 and 2, rewriting the data as an ISO 8601 combined date and time string and converting
    # to an Epoch time value.
    rtc_string = ["{:2d}{:02d}{:02d}{:02d}T{:02d}{:02d}{:02d}.{:03d}Z".format(rtc[0], rtc[1], rtc[2], rtc[3],
                                                                              rtc[4], rtc[5], rtc[6], rtc[7])
                  for rtc in vbl['real_time_clock2'].values]
    rtc = xr.Dataset({'real_time_clock': (['time'], pd.to_datetime(rtc_string, unit='s'))},
                     coords={'time': (['time'], pd.to_datetime(time, unit='s'))})
    vbl = vbl.drop(['real_time_clock1', 'real_time_clock2'])

    # use the ensemble number and increment variables (ensemble number rolls over at 65535) to calculate the
    # sequential ensemble number
    vbl['ensemble_number'] = vbl['ensemble_number'] + (vbl['ensemble_number_increment'] * 65535)
    vbl = vbl.drop(['ensemble_number_increment'])

    # create the 2D velocity, correlation magnitude, echo intensity and percent good data sets
    vel = xr.Dataset({
        'eastward': (['time', 'bin_number'], np.array(data['velocity']['eastward'])),
        'northward': (['time', 'bin_number'], np.array(data['velocity']['northward'])),
        'vertical': (['time', 'bin_number'], np.array(data['velocity']['vertical'])),
        'error': (['time', 'bin_number'], np.array(data['velocity']['error']))
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
               'bin_number': (['bin_number'], bin_number)})

    cor = xr.Dataset({
        'magnitude_beam1': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam1'])),
        'magnitude_beam2': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam2'])),
        'magnitude_beam3': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam3'])),
        'magnitude_beam4': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam4']))
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
               'bin_number': (['bin_number'], bin_number)})

    echo = xr.Dataset({
        'intensity_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1'])),
        'intensity_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2'])),
        'intensity_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3'])),
        'intensity_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']))
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
               'bin_number': (['bin_number'], bin_number)})

    per = xr.Dataset({
        'good_3beam': (['time', 'bin_number'], np.array(data['percent']['good_3beam'])),
        'transforms_reject': (['time', 'bin_number'], np.array(data['percent']['transforms_reject'])),
        'bad_beams': (['time', 'bin_number'], np.array(data['percent']['bad_beams'])),
        'good_4beam': (['time', 'bin_number'], np.array(data['percent']['good_4beam']))
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
               'bin_number': (['bin_number'], bin_number)})

    # combine it all into one data set
    adcp = xr.merge([fx, vbl, rtc, vel, cor, echo, per])

    # add to the global attributes for the ADCP
    attrs = dict_update(ADCP, ADCP_PD0)    # merge default and ADCP type attribute dictionaries into a single dictionary

    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })


if __name__ == '__main__':
    main()
