#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_adcp
@file cgsn_processing/process/proc_adcp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for ADCP from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, dict_update, dt64_epoch, epoch_time, json2obj, \
    json_obj2df, colocated_ctd, update_dataset
from cgsn_processing.process.configs.attr_adcp import ADCP, PD0, PD8, DERIVED
from gsw import z_from_p
from pyseas.data.generic_functions import magnetic_declination
from pyseas.data.adcp_functions import magnetic_correction, adcp_bin_depths


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

    # optional/default arguments for calculating the bin_depths
    bin_size = args.bin_size
    blanking_distance = args.blanking_distance
    ctd_name = args.devfile  # name of co-located CTD
    depth_m = depth
    depth_flag = False  # singleton depth value

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

    # check for data from a co-located CTD and test to see if it covers our time range of interest, will use this
    # data if the ADCP does not have a pressure sensor (majority of the OOI sensors)
    ctd = colocated_ctd(infile, ctd_name)
    if not ctd.empty:
        # set the CTD time to the same units as the ADCP time
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this ADCP file
        coverage = ctd_time.min() <= time.min() and ctd_time.max() >= time.max()

        # reset initial estimate of deployment depth based if we have full coverage
        if coverage:
            dbar = np.interp(time, ctd_time, ctd.pressure.values)
            depth_m = -1 * z_from_p(dbar, lat)
            depth_flag = True   # full time-based array of depth values

    # determine the magnetic declination for later use in correcting the eastward and northward velocity components
    theta = magnetic_declination(lat, lon, time)

    # Process PD0 formatted data
    if adcp_type.lower() == 'pd0':

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

        # calculate the bin_depths so we can plot our data in geo-spatial coordinates, pulling required data from the
        # data file (pressure is a special case, need to find the optimal source)
        blanking_distance = fx.bin_1_distance.values[0]
        bin_size = fx.depth_cell_length.values[0]
        orientation = fx.sysconfig_vertical_orientation.values[0]

        # determine best source for the pressure measurement: best = ADCP pressure sensor, good = co-located CTD, OK =
        # deployment depth (from inputs to the function).
        ptest = vbl.pressure == 0
        if not ptest.all():  # the ADCP has a pressure sensor, using that data instead of values set above
            # use the ADCP pressure sensor, convert the daPa values to dbar and then meters
            depth_m = -1 * z_from_p(vbl.pressure.values / 1000., lat)
            depth_flag = True  # full time-based array of depth values

        # calculate the bin_depths
        bin_depths = adcp_bin_depths(blanking_distance, bin_size, bin_number, orientation, depth_m)

        # remap the bin_depths to a 2D array to correspond to the time and bin_number coordinate axes.
        if not depth_flag:
            bin_depths = bin_depths.repeat(time.size, axis=0)

        # create the bin depths date set
        bd = xr.Dataset({
            'bin_depths': (['time', 'bin_number'], bin_depths)
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')), 'bin_number': bin_number})

        # correct the eastward and northward velocity components for magnetic declination
        u_cor, v_cor = magnetic_correction(theta, np.array(data['velocity']['eastward']),
                                           np.array(data['velocity']['northward']))

        # create the 2D velocity, correlation magnitude, echo intensity and percent good data sets
        vel = xr.Dataset({
            'eastward_seawater_velocity_est': (['time', 'bin_number'],
                                               np.array(data['velocity']['eastward']).astype(np.int32)),
            'eastward_seawater_velocity': (['time', 'bin_number'], u_cor / 1000.),
            'northward_seawater_velocity_est': (['time', 'bin_number'],
                                                np.array(data['velocity']['northward']).astype(np.int32)),
            'northward_seawater_velocity': (['time', 'bin_number'], v_cor / 1000.),
            'vertical_seawater_velocity': (['time', 'bin_number'],
                                           np.array(data['velocity']['vertical']).astype(np.int32)),
            'error_velocity': (['time', 'bin_number'], np.array(data['velocity']['error']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        cor = xr.Dataset({
            'correlation_magnitude_beam1': (['time', 'bin_number'],
                                            np.array(data['correlation']['magnitude_beam1']).astype(np.int32)),
            'correlation_magnitude_beam2': (['time', 'bin_number'],
                                            np.array(data['correlation']['magnitude_beam2']).astype(np.int32)),
            'correlation_magnitude_beam3': (['time', 'bin_number'],
                                            np.array(data['correlation']['magnitude_beam3']).astype(np.int32)),
            'correlation_magnitude_beam4': (['time', 'bin_number'],
                                            np.array(data['correlation']['magnitude_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        echo = xr.Dataset({
            'echo_intensity_beam1': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam1']).astype(np.int32)),
            'echo_intensity_beam2': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam2']).astype(np.int32)),
            'echo_intensity_beam3': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam3']).astype(np.int32)),
            'echo_intensity_beam4': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam4']).astype(np.int32))
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
            'percent_good_3beam': (['time', 'bin_number'],
                                   np.array(data['percent']['good_3beam']).astype(np.int32)),
            'percent_transforms_reject': (['time', 'bin_number'],
                                          np.array(data['percent']['transforms_reject']).astype(np.int32)),
            'percent_bad_beams': (['time', 'bin_number'], np.array(data['percent']['bad_beams']).astype(np.int32)),
            'percent_good_4beam': (['time', 'bin_number'], np.array(data['percent']['good_4beam']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        # combine it all into one data set
        adcp = xr.merge([glbl, fx, bd, vbl, rtc, vel, cor, echo, back, per])
        adcp['time'] = dt64_epoch(adcp.time)  # Convert from a datetime64 object to seconds since 1970
        adcp_attrs = PD0    # use the PD0 attributes

    elif adcp_type.lower() == 'pd8':
        # load the subset of variable header data included with a PD8 dataset
        df = json_obj2df(data, 'variable')
        vbl = xr.Dataset.from_dataframe(df)

        # pull the bin number out of the velocity data set
        bin_number = np.array(data['velocity']['bin_number'][0]).astype(np.int32)

        # calculate the bin_depths
        bin_depths = adcp_bin_depths(blanking_distance, bin_size, bin_number, 1, depth_m)

        # remap the bin_depths to a 2D array to correspond to the time and bin_number coordinate axes.
        if not depth_flag:
            bin_depths = bin_depths.repeat(time.size, axis=0)

        # create the bin depths date set
        bd = xr.Dataset({
            'bin_depths': (['time', 'bin_number'], bin_depths)
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')), 'bin_number': bin_number})

        # correct the eastward and northward velocity components for magnetic declination
        u_cor, v_cor = magnetic_correction(np.array(data['velocity']['eastward']),
                                           np.array(data['velocity']['northward']),
                                           theta)

        # create the 2D velocity and echo intensity data sets
        vel = xr.Dataset({
            'seawater_velocity_direction_est': (['time', 'bin_number'],
                                                np.array(data['velocity']['direction']).astype(np.float)),
            'seawater_velocity_magnitude_est': (['time', 'bin_number'],
                                                np.array(data['velocity']['magnitude']).astype(np.float)),
            'eastward_seawater_velocity_est': (['time', 'bin_number'],
                                               np.array(data['velocity']['eastward']).astype(np.int32)),
            'eastward_seawater_velocity': (['time', 'bin_number'], u_cor),
            'northward_seawater_velocity_est': (['time', 'bin_number'],
                                                np.array(data['velocity']['northward']).astype(np.int32)),
            'northward_seawater_velocity': (['time', 'bin_number'], v_cor),
            'vertical_seawater_velocity': (['time', 'bin_number'],
                                           np.array(data['velocity']['vertical']).astype(np.int32)),
            'error_velocity': (['time', 'bin_number'], np.array(data['velocity']['error']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        echo = xr.Dataset({
            'echo_intensity_beam1': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam1']).astype(np.int32)),
            'echo_intensity_beam2': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam2']).astype(np.int32)),
            'echo_intensity_beam3': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam3']).astype(np.int32)),
            'echo_intensity_beam4': (['time', 'bin_number'],
                                     np.array(data['echo']['intensity_beam4']).astype(np.int32))
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
        adcp = xr.merge([glbl, vbl, bd, vel, echo, back])
        adcp['time'] = dt64_epoch(adcp.time)  # Convert from a datetime64 object to seconds since 1970
        adcp_attrs = PD8    # use the PD8 attributes
    else:
        # Unknown ADCP type, exiting function
        return None

    # Compute the vertical extent of the data for the global metadata attributes
    vmax = adcp.bin_depths.max().values
    vmin = adcp.bin_depths.min().values

    # add to the global attributes for the ADCP
    attrs = dict_update(ADCP, adcp_attrs)   # merge default and PD0 attribute dictionaries into a single dictionary
    attrs = dict_update(attrs, DERIVED)     # add the derived attributes
    adcp = update_dataset(adcp, platform, deployment, lat, lon, [depth, vmin, vmax], attrs)

    # save the file
    adcp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
