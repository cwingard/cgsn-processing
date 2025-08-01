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

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update, epoch_time, \
    FILL_INT
from cgsn_processing.process.configs.attr_zplsc import ZPLSC
from cgsn_processing.process.configs.attr_common import SHARED


def sample_drift(df):
    """
    Calculate an estimate of the sample drift (difference between when the unit
    should sample versus when it actually did) over the course of a deployment
    by comparing the burst time to a preset array of sample times (minutes of
    the hour)

    :param df: dataframe with the burst time calculated from the burst
        date/time string
    :return: estimated sample drift in seconds relative to when the instrument
        should have sampled
    """
    schedule = np.array([5, 20, 35, 50])
    minutes = np.atleast_2d([x.minute for x in df['time']]).T
    offsets = np.abs(minutes - schedule)
    idx = np.argmin(offsets, 1)
    drift = []
    for i, t in enumerate(df['time']):
        scheduled = pd.Timestamp(t.year, t.month, t.day, t.hour, schedule[idx[i]], 0)
        drift.append(scheduled.to_datetime64().astype(float) / 10 ** 9 - df['burst_time'][i])

    return drift


def proc_zplsc(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    ASL AZFP bioacoustic sensor raw condensed pings processing function. Loads
    the JSON formatted parsed data and converts data into a NetCDF data file
    using xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return zplsc: xarray dataset with the raw condensed pings data
    """
    # process the variable length keyword arguments
    bin_size = kwargs.get('bin_size')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # compare the instrument clock (from the transmission_date_string) to the GPS based DCL time stamp
    df['transmission_time'] = [epoch_time(x) for x in df['transmission_date_string']]
    df['clock_offset'] = (df['time'].values.astype(float) / 10 ** 9) - df['transmission_time']

    # determine the offset and drift in the sampling time (should run at 5, 20, 35 and 50 minutes each hour)
    df['burst_time'] = [(pd.to_datetime(x, format='%y%m%d%H%M%S%f')).to_datetime64().astype(float) / 10 ** 9
                        for x in df['burst_date_string']]
    df['sampling_offset'] = sample_drift(df)

    # clean up the dataframe, getting rid of the time string variables we no longer need
    df.drop(columns=['dcl_date_time_string', 'transmission_date_string', 'burst_date_string'], inplace=True)

    # pop the 2D data arrays out of the dataframe (will put most of them back in later)
    profiles_channel_1 = np.array(np.vstack(df.pop('profiles_freq1')))
    profiles_channel_2 = np.array(np.vstack(df.pop('profiles_freq2')))
    profiles_channel_3 = np.array(np.vstack(df.pop('profiles_freq3')))
    profiles_channel_4 = np.array(np.vstack(df.pop('profiles_freq4')))
    minimum_values = np.array(np.vstack(df.pop('minimum_values')))
    number_bins = np.array(np.vstack(df.pop('number_bins')))
    frequencies = np.array(np.vstack(df.pop('frequencies')))
    _ = df.pop('phase')  # discard phase number, we only use the one.
    _ = df.pop('tilts')  # discard tilts array as unit is at 90 degrees and the sensor can only measure to +-45 degrees

    # break the frequencies array apart
    df['channel_1_freq'] = frequencies[:, 0]
    df['channel_2_freq'] = frequencies[:, 1]
    df['channel_3_freq'] = frequencies[:, 2]
    df['channel_4_freq'] = frequencies[:, 3]

    # convert the 1D variables to a xarray data set
    ds = xr.Dataset.from_dataframe(df)

    # add the minimum values back into the raw echo intensities
    profiles_channel_1 = profiles_channel_1 + np.atleast_2d(minimum_values[:, 0]).T
    profiles_channel_2 = profiles_channel_2 + np.atleast_2d(minimum_values[:, 1]).T
    profiles_channel_3 = profiles_channel_3 + np.atleast_2d(minimum_values[:, 2]).T
    profiles_channel_4 = profiles_channel_4 + np.atleast_2d(minimum_values[:, 3]).T

    # create an approximate depth axis for the dataset based on the bin size, the maximum number of bins, and the
    # mounting angle of the transducers.
    nbins = max(number_bins[0, :])
    bins = np.arange(nbins)
    bin_depth = depth - 1.0 - ((bins * bin_size) * np.cos(np.radians(15.0)) + (bin_size / 2.0))

    # pad the profiles with a fill value, if needed, so we can use a common bin_depth axis
    pad = nbins - number_bins[0, 0]
    if pad > 0:
        fill_int = (np.ones(pad) * FILL_INT).astype(int)
        profiles_channel_1 = np.concatenate([profiles_channel_1, np.tile(fill_int, (len(df.time), 1))], axis=1)
        profiles_channel_2 = np.concatenate([profiles_channel_2, np.tile(fill_int, (len(df.time), 1))], axis=1)
        profiles_channel_3 = np.concatenate([profiles_channel_3, np.tile(fill_int, (len(df.time), 1))], axis=1)
        profiles_channel_4 = np.concatenate([profiles_channel_4, np.tile(fill_int, (len(df.time), 1))], axis=1)

    bursts = xr.Dataset({
        'profiles_channel_1': (['time', 'bin_depth'], profiles_channel_1),
        'profiles_channel_2': (['time', 'bin_depth'], profiles_channel_2),
        'profiles_channel_3': (['time', 'bin_depth'], profiles_channel_3),
        'profiles_channel_4': (['time', 'bin_depth'], profiles_channel_4),
    }, coords={'time': (['time'], pd.to_datetime(df.time, unit='s')), 'bin_depth': bin_depth})

    # create a xarray data set from the 1D and 2D data
    zplsc = xr.merge([ds, bursts])

    # clean up the dataset and assign attributes
    zplsc['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(zplsc.time)).astype(str))
    attrs = dict_update(ZPLSC, SHARED)  # add the shared attributes
    zplsc = update_dataset(zplsc, platform, deployment, lat, lon, [depth, bin_depth.min(), bin_depth.max()], attrs)
    zplsc.attrs['processing_level'] = 'parsed'

    return zplsc


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

    # process the ASL AZFP data and save the results to disk
    zplsc = proc_zplsc(infile, platform, deployment, lat, lon, depth, bin_size=bin_size)
    if zplsc:
        zplsc.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
