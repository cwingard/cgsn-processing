#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_imm_adcp
@file cgsn_processing/process/proc_imm_adcp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for ADCP data recorded in PD12 format via an inductive modem link
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, dict_update, dt64_epoch, json2obj, update_dataset
from cgsn_processing.process.configs.attr_adcp import ADCP, PD12, DERIVED
from gsw.conversions import z_from_p
from pyseas.data.generic_functions import magnetic_declination
from pyseas.data.adcp_functions import magnetic_correction, adcp_bin_depth


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

    # arguments for calculating the bin_depth
    bin_size = args.bin_size
    blanking_distance = args.blanking_distance

    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # create the time coordinate array and setup a data set with the global values used above
    time = np.array(data['time'])
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(time, unit='s')
    df.set_index('time', drop=True, inplace=True)
    df['deploy_id'] = deployment
    glbl = xr.Dataset.from_dataframe(df)

    # drop real-time clock values (already used to create the time variable) and the unit ID (only used if more
    # than 1 ADCP is installed on the IMM chain).
    for k in ['year', 'month', 'day', 'hour', 'minute', 'second', 'csecond', 'unit_id']:
        del data[k]

    # determine the magnetic declination for later use in correcting the eastward and northward velocity components
    theta = magnetic_declination(lat, lon, time)

    # convert the ADCP pressure record to depth in meters (positive down from surface) from daPa
    depth_m = -1 * z_from_p(np.array(data['pressure']) / 1000., lat)

    # calculate the bin depths
    blanking_distance = blanking_distance * data['start_bin'][0]
    num_bins = data['bins'][0]
    bin_number = np.array(range(0, num_bins)) + 1
    bin_depth = adcp_bin_depth(blanking_distance, bin_size, bin_number, 1, depth_m)

    # create the bin depths data set
    bd = xr.Dataset({
        'bin_depth': (['time', 'bin_number'], bin_depth)
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')), 'bin_number': bin_number})

    # correct the eastward and northward velocity components for magnetic declination
    u_cor, v_cor = magnetic_correction(theta, np.array(data['eastward_velocity']), np.array(data['northward_velocity']))

    # create the 2D velocity and echo intensity data sets
    vel = xr.Dataset({
        'eastward_seawater_velocity_est': (['time', 'bin_number'],
                                           np.array(data['eastward_velocity']).astype(np.int32)),
        'eastward_seawater_velocity': (['time', 'bin_number'], u_cor / 1000.),
        'northward_seawater_velocity_est': (['time', 'bin_number'],
                                            np.array(data['northward_velocity']).astype(np.int32)),
        'northward_seawater_velocity': (['time', 'bin_number'], v_cor / 1000.),
        'vertical_seawater_velocity': (['time', 'bin_number'],
                                       np.array(data['vertical_velocity']).astype(np.int32)),
        'error_velocity': (['time', 'bin_number'], np.array(data['error_velocity']).astype(np.int32))
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
               'bin_number': bin_number})

    # convert the remaining data to a data set
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df.time, unit='s')
    df.index = df['time']
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop_vars(['start_bin', 'bins', 'northward_velocity', 'eastward_velocity', 'vertical_velocity',
                       'error_velocity'])

    # re-combine it all back into one data set
    adcp = xr.merge([glbl, ds, bd, vel])
    adcp['time'] = dt64_epoch(adcp.time)  # Convert from a datetime64 object to seconds since 1970

    # Compute the vertical extent of the data for the global metadata attributes
    vmax = adcp.bin_depth.max().values
    vmin = adcp.bin_depth.min().values

    # add to the global attributes for the ADCP
    attrs = dict_update(ADCP, PD12)   # merge default and PD12
    attrs = dict_update(attrs, DERIVED)     # add the derived attributes
    adcp = update_dataset(adcp, platform, deployment, lat, lon, [depth, vmin, vmax], attrs)

    # save the file
    adcp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
