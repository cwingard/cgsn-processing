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

# constant used by the ASIMET SWND v4.11 firmware processing
PI2 = 6.283185


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

    # add the min and max wind speeds for the bin
    avg['wind_speed_min'] = tbin['wind_speed'].min(dim='time')
    avg['wind_speed_max'] = tbin['wind_speed'].max(dim='time')

    # replace the averaged heading and relative wind directions with the last valid value
    avg['heading'] = tbin['heading'][-1]
    avg['relative_direction'] = tbin['relative_direction'][-1]

    # use the scalar-averaged wind speed and the wind direction calculated from vector averages to re-calculate the
    # eastward and northward wind components per directions provided by the NDBC (https://www.ndbc.noaa.gov/wndav.shtml)
    wind_direction = np.arctan2(avg['eastward_wind_asimet'], avg['northward_wind_asimet'])  # reported in radians
    wind_direction = np.where(wind_direction < 0, wind_direction + PI2, wind_direction)  # 0 to 360 degrees, in radians
    avg['eastward_wind_ndbc'] = avg['wind_speed'] * np.sin(wind_direction)
    avg['northward_wind_ndbc'] = avg['wind_speed'] * np.cos(wind_direction)

    # replace the averaged wind direction with one derived from the vector averages (convert radians to degrees)
    avg['wind_direction'] = wind_direction * 57.29578  # convert to degrees (rad * (360 / 2 * pi))

    return avg


def proc_swnd(infile, platform, deployment, lat, lon, depth):
    """
    Main ASIMET Sonic Wind (SWND) module processing function. Loads the JSON
    formatted parsed data and calculates different wind products to compare
    to the METBK reported eastward and northward wind components. In the
    later case, the METBK wind components are too low at higher wind speeds.
    This data should provide a better estimate of the wind speed and direction
    at higher wind speeds and should allow for a determination of why the
    METBK reported values are biased low. Note, this processing follows the
    steps outlined in the v4.11 firmware processing, but with some minor
    modifications, while the METBK data set is using the v4.20 firmware.

    For more information on the ASIMET system and the SWND module, see the
    ASIMET website:

        "https://www.whoi.edu/what-we-do/explore/instruments/\
            instruments-sensors-samplers/\
            air-sea-interaction-meteorology-the-asimet-system/"

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

    # drop the original wind components
    swnd = swnd.drop(columns=['u_axis_wind_speed', 'v_axis_wind_speed'])

    # convert the compass heading to radians
    heading = swnd['heading'] * 0.0174533  # convert to radians (deg * (2 * pi / 360))

    # calculate the wind speed
    swnd['wind_speed'] = np.sqrt(swnd['eastward_wind_relative']**2 + swnd['northward_wind_relative']**2)

    # calculate the relative wind direction, first correcting the northward wind component to avoid
    # divide by zero errors
    swnd['northward_wind_relative'] = np.where(swnd['northward_wind_relative'] == 0, 0.00001,
                                               swnd['northward_wind_relative'])
    direction = np.arctan2(swnd['eastward_wind_relative'], swnd['northward_wind_relative'])

    # convert to 0 to 360 degrees, but leave in radians for further calculations
    direction = np.where(direction < 0, direction + PI2, direction)

    # if the wind speed is less than 0.05 m/s, set the relative wind direction to a NaN and then forward
    # fill the NaNs with the last valid value (per the Gill WindMasterII manual) -- this differs from the
    # v4.11 processing, which does not make this adjustment
    direction = np.where(swnd['wind_speed'] < 0.05, np.nan, direction)

    # calculate the wind direction relative to magnetic north (using the compass heading and relative wind direction)
    wind_direction = direction + heading
    wind_direction = np.where(wind_direction > PI2, wind_direction - PI2, wind_direction)

    # now compute the eastward and northward wind components
    swnd['eastward_wind_asimet'] = swnd['wind_speed'] * np.sin(wind_direction)
    swnd['northward_wind_asimet'] = swnd['wind_speed'] * np.cos(wind_direction)

    # add the wind direction and relative wind direction (converted to degrees) to the data frame
    swnd['wind_direction'] = wind_direction * 57.29578  # convert to degrees (rad * (360 / 2 * pi))
    swnd['relative_direction'] = direction * 57.29578   # convert to degrees (rad * (360 / 2 * pi))

    # create an xarray data set from the data frame
    swnd = xr.Dataset.from_dataframe(swnd)

    # shift the time so subsequent resampling bins center the data in the middle of the 1-minute bin
    swnd['time'] = swnd.time + np.timedelta64(30, 's')

    # resample the data to 1-minute bins using the wind_binning function defined above
    swnd = swnd.resample(time='1Min', label='left', skipna=True).map(wind_binning)

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
