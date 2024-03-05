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
    components are then re-calculated using the average wind speed and vector
    averaged wind direction.

    :param tbin: grouped pandas dataframe with ~1-minute of 5-second wind data
    :return avg: dataframe with the averaged wind data
    """
    # calculate the 1-minute simple averages for the bin
    avg = tbin.mean(dim='time')

    # add the max wind speed for the bin
    avg['wind_speed_max'] = tbin['wind_speed'].max(dim='time')

    # replace the averaged heading and relative wind directions with circular means
    x = np.cos(np.radians(tbin['heading']))
    y = np.sin(np.radians(tbin['heading']))
    avg['heading'] = np.mod(np.degrees(np.arctan2(y.mean(), x.mean())), 360)
    x = np.cos(np.radians(tbin['relative_direction']))
    y = np.sin(np.radians(tbin['relative_direction']))
    avg['relative_direction'] = np.mod(np.degrees(np.arctan2(y.mean(), x.mean())), 360)

    # re-calculate the wind direction from the averaged eastward and northward wind components
    avg['wind_direction'] = np.mod(np.degrees(np.arctan2(avg['eastward_wind_asimet'],
                                                         avg['northward_wind_asimet'])), 360)

    # use the scalar-averaged wind speed and the wind direction calculated from vector averages to re-calculate the
    # eastward and northward wind components per directions provided by the NDBC (https://www.ndbc.noaa.gov/wndav.shtml)
    avg['eastward_wind_ndbc'] = avg['wind_speed'] * np.sin(np.radians(avg['wind_direction']))
    avg['northward_wind_ndbc'] = avg['wind_speed'] * np.cos(np.radians(avg['wind_direction']))
    return avg


def proc_swnd(infile, platform, deployment, lat, lon, depth):
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
    swnd['eastward_wind_relative'] = -1 * swnd['v_axis_wind_speed']  # rename and convert v-axis to positive eastward
    swnd['northward_wind_relative'] = swnd['u_axis_wind_speed']      # rename u-axis to northward
    swnd = swnd.drop(columns=['u_axis_wind_speed', 'v_axis_wind_speed'])

    # calculate the wind speed and the relative wind direction from the eastward and northward wind components
    swnd['wind_speed'] = np.sqrt(swnd['eastward_wind_relative']**2 + swnd['northward_wind_relative']**2)
    swnd['relative_direction'] = np.mod(np.degrees(np.arctan2(swnd['eastward_wind_relative'],
                                                              swnd['northward_wind_relative'])), 360)

    # if the wind speed is less than 0.05 m/s, set the wind direction to a NaN and then forward fill the NaNs
    # with the last valid value (per the Gill WindMasterII manual)
    swnd['relative_direction'] = np.where(swnd['wind_speed'] < 0.05, np.nan, swnd['relative_direction'])
    swnd['relative_direction'] = swnd['relative_direction'].ffill()

    # now use the compass heading to convert the instrument relative wind direction to magnetic north and derive
    # the true (magnetic) eastward and northward wind components (these should be comparable to the METBK wind
    # components)
    wind_direction = np.radians(np.mod(swnd['relative_direction'] + swnd['heading'], 360))
    swnd['eastward_wind_asimet'] = swnd['wind_speed'] * np.sin(wind_direction)
    swnd['northward_wind_asimet'] = swnd['wind_speed'] * np.cos(wind_direction)

    # create an xarray data set from the data frame
    swnd = xr.Dataset.from_dataframe(swnd)

    # shift the time so subsequent resampling bins center the data in the middle of the 1-minute bin
    swnd['time'] = swnd.time + np.timedelta64(30, 's')

    # resample the data to 1-minute bins using the wind_binning function defined above
    swnd = swnd.resample(time='1Min', label='left').map(wind_binning)

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
