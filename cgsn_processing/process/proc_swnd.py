#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_swnd
@file cgsn_processing/process/proc_swnd.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the dissolved oxygen from the JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING
from cgsn_processing.process.configs.attr_swnd import SWND


def wind_binning(tbin):
    """
    Function to bin the 5-second wind data into 1-minute averages. The wind
    speed and vector-averaged wind direction are calculated for each 1-minute
    bin. The maximum wind speed observed in the 1-minute bin is also recorded.
    The wind components are then re-calculated using the average wind speed and
    direction.

    :param tbin: xarray dataset with the 5-second wind data
    :return avg: xarray dataset with the 1-minute averaged wind data
    """
    # calculate the 1-minute averages
    avg = tbin.mean(dim='time')

    # replace the averaged heading with a circular mean
    x = np.mean(np.sin(np.radians(tbin['heading'])))
    y = np.mean(np.cos(np.radians(tbin['heading'])))
    avg['heading'] = np.mod(np.degrees(np.arctan2(x, y)), 360)

    # record the max wind speed observed in the 1-minute bin
    avg['wind_speed_max'] = tbin['wind_speed'].max(dim='time')

    # calculate wind direction from the vector average of the eastward and northward wind components
    avg['wind_direction'] = np.mod(np.degrees(np.arctan2(avg['eastward_wind_asimet'], avg['northward_wind_asimet'])), 360)

    # use the average wind speed and direction to re-calculate the eastward and northward wind components
    avg['eastward_wind_ndbc'] = avg['wind_speed'] * np.sin(np.radians(avg['wind_direction']))
    avg['northward_wind_ndbc'] = avg['wind_speed'] * np.cos(np.radians(avg['wind_direction']))
    return avg


def proc_swnd(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main ASIMET Sonic Wind (SWND) module processing function. Loads the JSON
    formatted parsed data and calculates different wind products to compare
    to the METBK reported eastward and northward wind components. In the
    later case, the METBK wind components are too low at higher wind speeds.
    This data should provide a better estimate of the wind speed and direction
    at higher wind speeds and should allow for a determination of why the
    METBK reported values are biased low.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform relative to the sea surface.
    :return swnd: xarray dataset with the processed SWND data
    """
    # load the json data file as a dictionary object for further processing
    swnd = json2df(infile)
    if swnd.empty:
        # json data file was empty, exiting
        return None

    # drop the DCL date and time string, we no longer need it
    swnd = swnd.drop(columns=['dcl_date_time_string'])

    # convert the Gill wind components to the oceanographic convention (relative to the east and north axis
    # of the instrument, rather than the U and V axis of the instrument).
    swnd['eastward_wind_relative'] = -1 * swnd['v_axis_wind_speed']  # rename and convert v-axis wind speed to eastward
    swnd['northward_wind_relative'] = swnd['u_axis_wind_speed']      # convert u-axis wind speed to positive northward
    swnd = swnd.drop(columns=['u_axis_wind_speed', 'v_axis_wind_speed'])

    # calculate the wind speed and relative wind direction
    swnd['wind_speed'] = np.sqrt(swnd['eastward_wind_relative']**2 + swnd['northward_wind_relative']**2)
    reldir = np.degrees(np.arctan2(swnd['eastward_wind_relative'], swnd['northward_wind_relative'])) + 180

    # for any wind speed less than 0.05 m/s, use a forward fill to use the last good wind direction
    m = swnd['wind_speed'] < 0.05  # per the vendor, the wind direction is not reliable at low wind speeds
    reldir[m] = np.nan
    reldir = reldir.ffill()

    # calculate the wind direction relative to magnetic north from the compass heading and the relative wind direction
    wnddir = np.mod(reldir + swnd['heading'], 360)

    # calculate the eastward and northward wind components using the wind speed and wind direction
    swnd['eastward_wind_asimet'] = -1 * swnd['wind_speed'] * np.sin(np.radians(wnddir))
    swnd['northward_wind_asimet'] = -1 * swnd['wind_speed'] * np.cos(np.radians(wnddir))

    # create an xarray data set from the data frame
    swnd = xr.Dataset.from_dataframe(swnd)

    # resample the data to 1-minute averages using the wind_binning function defined above
    swnd = swnd.resample(time='1Min', closed='right', label='right').map(wind_binning)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    swnd['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(swnd.time)).astype(str))
    swnd = update_dataset(swnd, platform, deployment, lat, lon, [depth, depth, depth], SWND)
    return swnd


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

    # process the CTDBP data and save the results to disk
    swnd = proc_swnd(infile, platform, deployment, lat, lon, depth)
    if swnd:
        swnd.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
