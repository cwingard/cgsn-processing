#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_zplsc
@file cgsn_processing/process/proc_zplsc.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the ZPLSC data from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from datetime import datetime, timezone

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, FILL_INT, dict_update
from cgsn_processing.process.configs.attr_zplsc import ZPLSC
from cgsn_processing.process.configs.attr_common import SHARED


def proc_zplsc(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main ZPLSC processing function. Loads the JSON formatted parsed data and
    rearranges the data to create 2D arrays of the echo intensity data. More
    importantly, creates additional variables to allow for tracking the clock
    drift and the sample timing drift.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwargs bin_size: Size of the bins (in meters) used by the condensed
        profiles (used to contruct the bin_depth dimension).

    :return zplsc: An xarray dataset with the reorganized ZPLSC data
    """
    # process the variable length keyword arguments
    bin_size = kwargs.get('bin_size')

    # load the json data file as a dictionary object for further processing
    data = json2df(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # compare the instrument clock to the GPS based DCL time stamp to track clock and sampling drift
    clock_drift = []
    sampling_drift = []
    for i in range(len(data['time'])):
        trans_time = datetime.strptime(data['transmission_date_string'][i], "%Y%m%d%H%M%S")
        burst_time = datetime.strptime(data['burst_date_string'][i], "%Y%m%d%H%M%S")
        trans_time.replace(tzinfo=timezone.utc)
        burst_time.replace(tzinfo=timezone.utc)
        clock_drift.append((trans_time - data['time'][i]).total_seconds())
        sampling_drift.append((burst_time - data['time'][i]).total_seconds())

    data['clock_drift'] = clock_drift
    data['sampling_drift'] = sampling_drift

    # now that we are done with them, drop the date/time strings
    data.drop(columns=['dcl_date_time_string', 'transmission_date_string', 'burst_date_string'], inplace=True)

    # pop the data arrays out of the dataframe (will put most of them back in later)
    profiles_channel_1 = np.array(np.vstack(data.pop('profiles_freq1')))
    profiles_channel_2 = np.array(np.vstack(data.pop('profiles_freq2')))
    profiles_channel_3 = np.array(np.vstack(data.pop('profiles_freq3')))
    profiles_channel_4 = np.array(np.vstack(data.pop('profiles_freq4')))
    minimum_values = np.array(np.vstack(data.pop('minimum_values')))
    number_bins = np.array(np.vstack(data.pop('number_bins')))
    frequencies = np.array(np.vstack(data.pop('frequencies')))
    _ = data.pop('phase')  # discard phase number, we only use the one.
    _ = data.pop('tilts')  # discard tilts array as unit is at 90 degrees and unusable

    # break the frequencies array apart into named variables
    data['channel_1_freq'] = frequencies[:, 0]
    data['channel_2_freq'] = frequencies[:, 1]
    data['channel_3_freq'] = frequencies[:, 2]
    data['channel_4_freq'] = frequencies[:, 3]

    # add the per burst minimum values back into the raw echo intensities
    profiles_channel_1 = profiles_channel_1 + np.atleast_2d(minimum_values[:, 0]).T
    profiles_channel_2 = profiles_channel_2 + np.atleast_2d(minimum_values[:, 1]).T
    profiles_channel_3 = profiles_channel_3 + np.atleast_2d(minimum_values[:, 2]).T
    profiles_channel_4 = profiles_channel_4 + np.atleast_2d(minimum_values[:, 3]).T

    # create an xarray dataset of the 1D data
    ds = xr.Dataset.from_dataframe(data)
    
    # create an approximate depth axis for the dataset based on the bin size, the maximum number of bins, and the
    # mounting angle of the transducers.
    bins = (np.arange(max(number_bins[0, :])) * bin_size) * np.cos(np.radians(15.0))
    bin_depth = depth - 1.0 - (bins + (bin_size / 2.0))
    
    # pad the profiles with a fill value, if needed, so we can use a common bin_depth axis
    pad = max(number_bins[0, :]) - number_bins[0, 0]
    if pad > 0:
        fill = np.ones(pad) * FILL_INT
        profiles_channel_1 = np.concatenate((profiles_channel_1, np.tile(fill, (len(ds.time), 1))), axis=1)

    pad = max(number_bins[0, :]) - number_bins[0, 1]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_2 = np.concatenate((profiles_channel_2, np.tile(fill, (len(ds.time), 1))), axis=1)

    pad = max(number_bins[0, :]) - number_bins[0, 2]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_3 = np.concatenate((profiles_channel_3, np.tile(fill, (len(ds.time), 1))), axis=1)

    pad = max(number_bins[0, :]) - number_bins[0, 3]
    if pad > 0:
        fill = np.ones(pad) * -999999999
        profiles_channel_4 = np.concatenate((profiles_channel_4, np.tile(fill, (len(ds.time), 1))), axis=1)

    # create the 2D arrays for the raw channel measurements
    profiles = xr.Dataset({
        'profiles_channel_1': (['time', 'bin_depth'], profiles_channel_1),
        'profiles_channel_2': (['time', 'bin_depth'], profiles_channel_2),
        'profiles_channel_3': (['time', 'bin_depth'], profiles_channel_3),
        'profiles_channel_4': (['time', 'bin_depth'], profiles_channel_4),
    }, coords={'time': (['time'], pd.to_datetime(data['time'], unit='s')), 'bin_depth': bin_depth})

    # combine the 1D and 2D data
    zplsc = xr.merge([ds, profiles])
    
    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    zplsc['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(zplsc.time)).astype(str))
    attrs = dict_update(ZPLSC, SHARED)
    zplsc = update_dataset(zplsc, platform, deployment, lat, lon, depth, attrs)
    zplsc.attrs['processing_level'] = 'parsed'

    return zplsc


def main(argv=None):
    """
    Command line function to process the ZPLSC data using the proc_zplsc
    function. Command line arguments are parsed and passed to the function.

    :param argv: List of command line arguments
    """
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

    # process the OPTAA data and save the results to disk
    zplsc = proc_zplsc(infile, platform, deployment, lat, lon, depth, bin_size=bin_size)
    if zplsc:
        zplsc.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
