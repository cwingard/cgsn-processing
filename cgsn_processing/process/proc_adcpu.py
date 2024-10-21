#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_adcpu (derived from proc_adcp.py)
@file cgsn_processing/process/proc_adcpu.py
@author Paul Whelan
@brief Creates a NetCDF dataset for the Nortek Aquadopp 2 data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import ENCODING, inputs, dict_update, json2obj, update_dataset
from cgsn_processing.process.configs.attr_adcpu import ADCPU
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.generic_functions import magnetic_declination
from pyseas.data.adcp_functions import magnetic_correction


def proc_adcpu(infile, platform, deployment, lat, lon, depth):
    """
    Main ADCPU processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. Deployment details are used to determine the
    magnetic declination prior to converting the current vectors from magnetic
    north to true north.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return adcpu: An xarray dataset with the processed ADCPU data
    """
    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # create the time coordinate array and set up a data frame with the global values
    time = np.array(data['time'])
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(time, unit='s')
    df.set_index('time', drop=True, inplace=True)
    df['deploy_id'] = deployment
    glbl_ds = xr.Dataset.from_dataframe(df)

    # create the cell number coordinate array
    cell_number = np.arange(1, data['config']['number_cells'][0] + 1).astype(int)

    df = pd.DataFrame()
    df['cell_number'] = cell_number
    df.set_index('cell_number', drop=True, inplace=True)
    cell_ds = xr.Dataset.from_dataframe(df)

    # determine the magnetic declination for later use in correcting the eastward and northward velocity components
    theta = magnetic_declination(lat, lon, time)

    # load the config data 
    cfg_ds = xr.Dataset({'instrument_type': (['time'], np.array(data['config']['instrument_type']).astype(int)),
                         'instrument_name': (['time'], np.array(data['config']['instrument_name'])),
                         'number_beams': (['time'], np.array(data['config']['number_beams']).astype(int)),
                         'number_cells': (['time'], np.array(data['config']['number_cells']).astype(int)),
                         'blanking': (['time'], np.array(data['config']['blanking']).astype(float)),
                         'cell_size': (['time'], np.array(data['config']['cell_size']).astype(float)),
                         'coordinate_system': (['time'], np.array(data['config']['coord_system']).astype(int))
                         })

    # load the sensor data
    sen_ds = xr.Dataset({'error_code': (['time'], np.array(data['sensor']['error_code'])),
                         'status_code': (['time'], np.array(data['sensor']['status_code'])),
                         'battery_voltage': (['time'], np.array(data['sensor']['battery_voltage']).astype(float)),
                         'sound_speed': (['time'], np.array(data['sensor']['sound_speed']).astype(float)),
                         'heading': (['time'], np.array(data['sensor']['heading']).astype(float)),
                         'pitch': (['time'], np.array(data['sensor']['pitch']).astype(float)),
                         'roll': (['time'], np.array(data['sensor']['roll']).astype(int)),
                         'pressure': (['time'], np.array(data['sensor']['pressure']).astype(float)),
                         'temperature': (['time'], np.array(data['sensor']['temperature']).astype(float)),
                         'analog_in_1': (['time'], np.array(data['sensor']['analog_in_1']).astype(int)),
                         'analog_in_2': (['time'], np.array(data['sensor']['analog_in_2']).astype(int))
                         })

    # load the variable current data packets (the current dataset is 2 dimensions [time, cell])
    len_time = len(time)
    len_cell = len(cell_number)

    # correct the eastward and northward velocity components for magnetic declination
    v_east = np.array(data['current']['velocity_beam_1'])
    v_north = np.array(data['current']['velocity_beam_2'])

    # re-dimension to [time][cells] for using magnetic_correction function
    v_east = np.resize(v_east, (len_time, len_cell))
    v_north = np.resize(v_north, (len_time, len_cell))
    u_cor, v_cor = magnetic_correction(theta, v_east, v_north)

    # everything else also has to be made into a np.array and re-dimensioned
    vb1 = np.array(data['current']['velocity_beam_1']).astype(float)
    vb1 = np.resize(vb1, (len_time, len_cell))
    vb2 = np.array(data['current']['velocity_beam_2']).astype(float)
    vb2 = np.resize(vb2, (len_time, len_cell))
    vb3 = np.array(data['current']['velocity_beam_3']).astype(float)
    vb3 = np.resize(vb3, (len_time, len_cell))
    spd = np.array(data['current']['speed']).astype(float)
    spd = np.resize(spd, (len_time, len_cell))
    dir = np.array(data['current']['direction']).astype(float)
    dir = np.resize(dir, (len_time, len_cell))
    am1 = np.array(data['current']['amplitude_beam_1']).astype(int)
    am1 = np.resize(am1, (len_time, len_cell))
    am2 = np.array(data['current']['amplitude_beam_2']).astype(int)
    am2 = np.resize(am2, (len_time, len_cell))
    am3 = np.array(data['current']['amplitude_beam_3']).astype(int)
    am3 = np.resize(am3, (len_time, len_cell))
    co1 = np.array(data['current']['correlation_beam_1']).astype(int)
    co1 = np.resize(co1, (len_time, len_cell))
    co2 = np.array(data['current']['correlation_beam_2']).astype(int)
    co2 = np.resize(co2, (len_time, len_cell))
    co3 = np.array(data['current']['correlation_beam_3']).astype(int)
    co3 = np.resize(co3, (len_time, len_cell))

    cur_ds = xr.Dataset({'velocity_beam_1': (['time', 'cell_number'], vb1),
                         'velocity_beam_2': (['time', 'cell_number'],  vb2),
                         'velocity_beam_3': (['time', 'cell_number'],  vb3),
                         'velocity_east_corrected': (['time', 'cell_number'], u_cor),
                         'velocity_north_corrected': (['time', 'cell_number'], v_cor),
                         'velocity_vertical': (['time', 'cell_number'], vb3),
                         'speed': (['time', 'cell_number'], spd),
                         'direction': (['time', 'cell_number'], dir),
                         'amplitude_beam_1': (['time', 'cell_number'], am1),
                         'amplitude_beam_2': (['time', 'cell_number'], am2),
                         'amplitude_beam_3': (['time', 'cell_number'], am3),
                         'correlation_beam_1': (['time', 'cell_number'], co1),
                         'correlation_beam_2': (['time', 'cell_number'], co2),
                         'correlation_beam_3': (['time', 'cell_number'], co3)
                         }, coords={'time': (['time'], pd.to_datetime(time, unit='s')), 'cell_number': cell_number})

    adcpu = xr.merge([glbl_ds, cell_ds, cfg_ds, sen_ds, cur_ds])

    # Add in attributes
    attrs = dict_update(ADCPU, SHARED)
    adcpu = update_dataset(adcpu, platform, deployment, lat, lon, [depth, 0.0, depth], attrs)
    adcpu.attrs['processing_level'] = 'processed'

    return adcpu


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

    # process the ADCP data and save the results to disk
    adcpu = proc_adcpu(infile, platform, deployment, lat, lon, depth)
    if adcpu:
        adcpu.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()