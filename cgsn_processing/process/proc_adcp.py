#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_adcp
@file cgsn_processing/process/proc_adcp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for ADCP from JSON formatted source data
"""
import datetime
import numpy as np
import os
import pandas as pd
import xarray as xr

from geomag import declination

from cgsn_processing.process.common import ENCODING, inputs, dict_update, epoch_time, json2obj, json_obj2df, update_dataset
from cgsn_processing.process.configs.attr_adcp import ADCP, PD0, PD8, DERIVED


def bin_depths(distance_first_bin, cell_length, bin_numbers, sensor_depth, orientation):
    """
    Calculates the center bin depths for PD0, PD8 and PD12 ADCP data. As defined in the Data Product Specification
    for Velocity Profile and Echo Intensity - DCN 1341-00750.

    :param dist_first_bin:
    :param bin_size:
    :param num_bins:
    :param sensor_depth:
    :param orientation:
    :return:
    """
    # Convert from cm to meters
    first_bin = distance_first_bin / 100.0
    bin_size = cell_length / 100.0

    # Following the PD0 convention where
    #     adcp_orientation = 0 is downward looking, bin_depths are added to sensor depth
    #                      = 1 is upward looking, bin_depths are subtracted from sensor depth
    z_sign = 1.0 - 2.0 * orientation

    # Calculate the bin depths
    bin_depths = sensor_depth + z_sign * (first_bin + bin_size * bin_numbers)

    return bin_depths


def magnetic_correction(u, v, theta):
    """
    Determines the magnetic declination for the ADCP based upon the depth, date and location of the ADCP. Then applies
    that correction to the eastward and northward velocity components.

    :param u:
    :param v:
    :param theta:
    :return u_cor, v_cor:
    """
    # create masked arrays to capture the preset fill values
    ma_u = np.ma.masked_equal(u, -32768).mask   # ADCPs report -32768 as their fill value
    ma_v = np.ma.masked_equal(v, -32768).mask   # ADCPs report -32768 as their fill value

    # create the transformation matrix based on the magnetic declination
    cosT = np.cos(theta)
    sinT = np.sin(theta)

    M = np.array([
        [cosT, sinT],
        [-1*sinT, cosT]
    ])

    # roll axes so that the lead index represents data packet #.
    M = np.rollaxis(M, 2)

    # the coordinate system is 2D, so the middle dimension is sized at 2.
    uv = np.zeros((u.shape[0], 2, u.shape[1]))

    # pack the coordinates to be rotated into the appropriate slices
    uv[:, 0, :] = u
    uv[:, 1, :] = v

    # the Einstein summation is here configured to do the matrix multiplication uv_cor(i,k) = M(i,j) * uv(j,k)
    # on each slice h.
    uv_cor = np.einsum('hij,hjk->hik', M, uv)

    # the magnetically corrected u values are (scaled to m/s from mm/s):
    u_cor = uv_cor[:, 0, :] / 1000

    # the magnetically corrected v values are (scaled to m/s from mm/s):
    v_cor = uv_cor[:, 1, :] / 1000

    # use the mask to re-apply the fill values (using NaN now that we have converted to floating points)
    u_cor = np.ma.filled(np.ma.fix_invalid(u_cor, ma_u), np.nan)
    v_cor = np.ma.filled(np.ma.fix_invalid(v_cor, ma_v), np.nan)

    return u_cor, v_cor


def utc2date(utc_dates):
    """

    :param utc_dates:
    :return date:
    """
    date = datetime.datetime.utcfromtimestamp(utc_dates).date()
    return date


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

    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # create the time coordinate array and setup a data frame with the global values used above
    time = np.array(data['time'])
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(time, unit='s')
    df.set_index('time', drop=True, inplace=True)
    df['deploy_id'] = deployment
    glbl = xr.Dataset.from_dataframe(df)

    # determine the magnetic declination, using vectorized functions, for later use in correcting the eastward and
    # northward velocity components
    decln = np.vectorize(declination)
    dates = np.vectorize(utc2date)
    feet = -1 * (depth * 3.281)  # geomag uses altitude in feet for the declination
    theta = np.radians(decln(lat, lon, feet, dates(time)))

    # Process PD0 formatted data
    if adcp_type.lower == 'pd0':

        # create the bin number coordinate array
        bin_number = np.arange(data['fixed']['num_cells'][0] - 1).astype(np.int32)

        # load the fixed header data packets
        df = json_obj2df(data, 'fixed')
        fx = xr.Dataset.from_dataframe(df)

        # combine the time_per_ping_seconds and the time_per_ping_minutes into a single variable, ping_period.
        fx['ping_period'] = fx['time_per_ping_seconds'] + (fx['time_per_ping_minutes'] / 60)
        fx = fx.drop(['time_per_ping_seconds', 'time_per_ping_minutes'])    # drop the sub-components

        # load the variable leader data packets
        df = json_obj2df(data, 'variable')
        vbl = xr.Dataset.from_dataframe(df)

        # drop real-time clock arrays 1 and 2, rewriting the data as an ISO 8601 combined date and time string and
        # convert to a Unix epoch time.
        rtc = []
        for ts in vbl['real_time_clock2'].values:
            rtc_string = "{:2d}{:02d}{:02d}{:02d}T{:02d}{:02d}{:02d}.{:03d}Z".format(ts[0], ts[1], ts[2], ts[3],
                                                                                     ts[4], ts[5], ts[6], ts[7])
            rtc.append(epoch_time(rtc_string))  # convert the date/time string to a Unix epoch time stamp

        rtc = xr.Dataset({'real_time_clock': (['time'], rtc)},
                         coords={'time': (['time'], pd.to_datetime(time, unit='s'))})
        vbl = vbl.drop(['real_time_clock1', 'real_time_clock2'])    # drop the sub-components

        # use the ensemble number and increment variables (ensemble number rolls over at 65535) to calculate the
        # sequential ensemble number
        vbl['ensemble_number'] = vbl['ensemble_number'] + (vbl['ensemble_number_increment'] * 65535)
        vbl = vbl.drop(['ensemble_number_increment'])   # drop the sub-components

        # correct the eastward and northward velocity components for magnetic declination
        u_cor, v_cor = magnetic_correction(np.array(data['velocity']['eastward']),
                                           np.array(data['velocity']['northward']),
                                           theta)

        # create the 2D velocity, correlation magnitude, echo intensity and percent good data sets
        vel = xr.Dataset({
            'eastward_seawater_velocity_est': (['time', 'bin_number'], np.array(data['velocity']['eastward']).astype(np.int32)),
            'eastward_seawater_velocity': (['time', 'bin_number'], u_cor),
            'northward_seawater_velocity_est': (['time', 'bin_number'], np.array(data['velocity']['northward']).astype(np.int32)),
            'northward_seawater_velocity': (['time', 'bin_number'], v_cor),
            'vertical_seawater_velocity': (['time', 'bin_number'], np.array(data['velocity']['vertical']).astype(np.int32)),
            'error_velocity': (['time', 'bin_number'], np.array(data['velocity']['error']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        cor = xr.Dataset({
            'correlation_magnitude_beam1': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam1']).astype(np.int32)),
            'correlation_magnitude_beam2': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam2']).astype(np.int32)),
            'correlation_magnitude_beam3': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam3']).astype(np.int32)),
            'correlation_magnitude_beam4': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        echo = xr.Dataset({
            'echo_intensity_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1']).astype(np.int32)),
            'echo_intensity_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2']).astype(np.int32)),
            'echo_intensity_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3']).astype(np.int32)),
            'echo_intensity_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        back = xr.Dataset({
            'backscatter_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1']) * 0.45),
            'backscatter_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2']) * 0.45),
            'backscatter_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3']) * 0.45),
            'backscatter_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']) * 0.45),
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        per = xr.Dataset({
            'percent_good_3beam': (['time', 'bin_number'], np.array(data['percent']['good_3beam']).astype(np.int32)),
            'percent_transforms_reject': (['time', 'bin_number'], np.array(data['percent']['transforms_reject']).astype(np.int32)),
            'percent_bad_beams': (['time', 'bin_number'], np.array(data['percent']['bad_beams']).astype(np.int32)),
            'percent_good_4beam': (['time', 'bin_number'], np.array(data['percent']['good_4beam']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        # combine it all into one data set
        adcp = xr.merge([glbl, fx, vbl, rtc, vel, cor, echo, back, per])
        adcp['time'] = adcp.time.values.astype(float) / 10.0 ** 9  # Convert from nanoseconds to seconds since 1970
        adcp_attrs = PD0    # use the PD0 attributes

        # Compute the vertical extent of the data for the global metadata attributes
        if adcp.sysconfig_vertical_orientation.values[0]:
            # ADCP is looking upwards, max depth is the deployment depth and the min depth is the surface
            vmax = depth
            vmin = 0.0
        else:
            # ADCP is looking downward, we reverse the logic from above and compute the full range for the max depth
            vmin = depth
            vmax = vmin + adcp.depth_cell_length.values[0] / 100 * max(bin_number)

    elif adcp_type == 'PD8':
        # load the subset of variable header data included with a PD8 dataset
        df = json_obj2df(data, 'variable')
        vbl = xr.Dataset.from_dataframe(df)

        # pull the bin number out of the velocity data set
        bin_number = np.array(data['velocity']['bin_number'][0]).astype(np.int32)

        # correct the eastward and northward velocity components for magnetic declination
        u_cor, v_cor = magnetic_correction(np.array(data['velocity']['eastward']),
                                           np.array(data['velocity']['northward']),
                                           theta)

        # create the 2D velocity and echo intensity data sets
        vel = xr.Dataset({
            'seawater_velocity_direction_est': (['time', 'bin_number'], np.array(data['velocity']['direction']).astype(np.float)),
            'seawater_velocity_magnitude_est': (['time', 'bin_number'], np.array(data['velocity']['magnitude']).astype(np.float)),
            'eastward_seawater_velocity_est': (['time', 'bin_number'], np.array(data['velocity']['eastward']).astype(np.int32)),
            'eastward_seawater_velocity': (['time', 'bin_number'], u_cor),
            'northward_seawater_velocity_est': (['time', 'bin_number'], np.array(data['velocity']['northward']).astype(np.int32)),
            'northward_seawater_velocity': (['time', 'bin_number'], v_cor),
            'vertical_seawater_velocity': (['time', 'bin_number'], np.array(data['velocity']['vertical']).astype(np.int32)),
            'error_velocity': (['time', 'bin_number'], np.array(data['velocity']['error']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        echo = xr.Dataset({
            'echo_intensity_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1']).astype(np.int32)),
            'echo_intensity_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2']).astype(np.int32)),
            'echo_intensity_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3']).astype(np.int32)),
            'echo_intensity_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        back = xr.Dataset({
            'backscatter_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1']) * 0.45),
            'backscatter_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2']) * 0.45),
            'backscatter_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3']) * 0.45),
            'backscatter_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']) * 0.45),
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        # combine it all into one data set
        adcp = xr.merge([glbl, vbl, vel, echo, back])
        adcp['time'] = adcp.time.values.astype(float) / 10.0 ** 9  # Convert from nanoseconds to seconds since 1970
        adcp_attrs = PD8    # use the PD8 attributes

        # Compute the vertical extent of the data for the global metadata attributes. Only Pioneer uses PD8 and all of
        # their units are on MFNs looking upward.
        vmax = depth
        vmin = 0.0

    # add to the global attributes for the ADCP
    attrs = dict_update(ADCP, adcp_attrs)   # merge default and PD0 attribute dictionaries into a single dictionary
    attrs = dict_update(attrs, DERIVED)     # add the derived attributes
    adcp = update_dataset(adcp, platform, deployment, lat, lon, [depth, vmin, vmax], attrs)

    # save the file
    adcp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
