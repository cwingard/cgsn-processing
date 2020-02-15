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
from cgsn_processing.process.configs.attr_adcp import ADCP, PD12, DERIVED
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

    # arguments for calculating the bin_depths
    bin_size = args.bin_size
    blanking_distance = args.blanking_distance

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

    # determine the magnetic declination for later use in correcting the eastward and northward velocity components
    theta = magnetic_declination(lat, lon, time)

    # convert the pressure record to meters from kPa
    depth = data['pressure']

    # calculate the bin_depths
    num_bins = data['bins'][0]
    bin_depths = adcp_bin_depths(blanking_distance, bin_size, num_bins, 1, depth)

    # remap the bin_depths to a 2D array to correspond to the time and bin_number coordinate axes.
    bin_depths = bin_depths.repeat(time.size, axis=0)

    # create the bin depths data set
    bd = xr.Dataset({
        'bin_depths': (['time', 'bin_number'], bin_depths)
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')), 'bin_number': num_bins})

    # correct the eastward and northward velocity components for magnetic declination
    u_cor, v_cor = magnetic_correction(theta, np.array(data['velocity']['eastward']),
                                       np.array(data['velocity']['northward']))

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

    # Compute the vertical extent of the data for the global metadata attributes
    vmax = adcp.bin_depths.max().values
    vmin = adcp.bin_depths.min().values

    # add to the global attributes for the ADCP
    attrs = dict_update(ADCP, adcp_attrs)   # merge default and PD12
    attrs = dict_update(attrs, DERIVED)     # add the derived attributes
    adcp = update_dataset(adcp, platform, deployment, lat, lon, [depth, vmin, vmax], attrs)

    # save the file
    adcp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
