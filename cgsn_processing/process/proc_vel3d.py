#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_vel3d
@file cgsn_processing/process/proc_vel3d.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Nortek Vector Velocimeter (VEL3D) data
"""
import os
import numpy as np
import xarray as xr

from gsw import z_from_p
from pyseas.data.generic_functions import magnetic_declination, magnetic_correction

from cgsn_processing.process.common import ENCODING, FILL_INT, inputs, json2obj, json_obj2df, dt64_epoch, update_dataset
from cgsn_processing.process.configs.attr_vel3d import VEL3D


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

    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # pull out the noise measurements collected at the start of a measurement cycle
    if data['header']:
        noise_amplitudes = np.array(data['header']['noise_amplitudes']).astype(np.int32)
        noise_correlations = np.array(data['header']['noise_correlations']).astype(np.int32)
    else:
        noise_amplitudes = np.ones * FILL_INT
        noise_correlations = np.ones * FILL_INT

    # create the system data set
    df = json_obj2df(data, 'system')
    system = xr.Dataset.from_dataframe(df)
    system = system.drop_vars(['date_time_array'])

    # create the velocity
    df = json_obj2df(data, 'velocity')
    df.drop(columns=['ensemble_counter', 'amplitudes', 'correlations'], inplace=True)
    amplitudes = np.array(data['velocity']['amplitudes']).astype(np.int32)      # grab the amplitudes array
    correlations = np.array(data['velocity']['correlations']).astype(np.int32)  # grab the correlations array

    # convert the amplitudes array to individually named variables
    df['amplitude_beam1'] = amplitudes[:, 0]
    df['amplitude_beam2'] = amplitudes[:, 1]
    df['amplitude_beam3'] = amplitudes[:, 2]

    # merge by replication the ambient noise amplitudes measured at the start of a burst
    df['noise_amplitude_beam1'] = noise_amplitudes[0, 0]
    df['noise_amplitude_beam2'] = noise_amplitudes[0, 1]
    df['noise_amplitude_beam3'] = noise_amplitudes[0, 2]

    # convert the correlations array to individually named variables
    df['correlation_beam1'] = correlations[:, 0]
    df['correlation_beam2'] = correlations[:, 1]
    df['correlation_beam3'] = correlations[:, 2]

    # merge by replication the ambient noise correlations measured at the start of a burst
    df['noise_correlation_beam1'] = noise_correlations[0, 0]
    df['noise_correlation_beam2'] = noise_correlations[0, 1]
    df['noise_correlation_beam3'] = noise_correlations[0, 2]

    # add the deployment number and create the data set
    df['deploy_id'] = deployment
    velocity = xr.Dataset.from_dataframe(df)

    # merge the 1 Hz system data into the 8 Hz velocity data
    system = system.reindex_like(velocity, method='nearest')
    vel3d = velocity.merge(system)

    # convert the error and status code variable data types
    vel3d['error_code'] = (vel3d['error_code']).astype(np.uint8)
    vel3d['status_code'] = (vel3d['status_code']).astype(np.uint8)

    # convert the pressure record to depth and calculate mean, min and max depths
    z = z_from_p(vel3d.pressure.values, lat)
    vmin = np.min(z)
    vmax = np.max(z)
    z = np.mean(z)

    # apply magnetic declination correction to the eastward and northward velocity
    # components and scale from mm/s to m/s
    theta = magnetic_declination(lat, lon, dt64_epoch(vel3d['time']), depth)
    magvar = np.vectorize(magnetic_correction)
    east, north = magvar(theta, vel3d.velocity_east / 1000., vel3d.velocity_north / 1000.)

    # add the corrected data back into the data set
    vel3d['velocity_east_corrected'] = (['time'], east)
    vel3d['velocity_north_corrected'] = (['time'], north)

    # update the data set with appropriate metadata
    vel3d = update_dataset(vel3d, platform, deployment, lat, lon, [z, vmin, vmax], VEL3D)

    # save the file
    vel3d.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)

if __name__ == '__main__':
    main()
