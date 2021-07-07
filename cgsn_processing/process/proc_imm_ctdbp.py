#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_imm_ctdbp
@file cgsn_processing/process/proc_imm_ctdbp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the CTDBP data transferred via the IMM from the JSON formatted data
"""
import os
import re

import numpy as np
import xarray as xr

from gsw import SP_from_C, SA_from_SP, CT_from_t, rho

from cgsn_processing.process.common import ENCODING, inputs, dict_update, epoch_time, join_df, \
    json2obj, json_obj2df, update_dataset
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_ctdbp import CTDBP

from cgsn_processing.process.proc_dosta import Calibrations as DOSTA_Calibrations
from cgsn_processing.process.proc_flort import Calibrations as FLORD_Calibrations

from pyseas.data.do2_functions import do2_phase_volt_to_degree, do2_therm_volt_to_degc, \
    do2_phase_to_doxy, do2_salinity_correction
from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


def proc_imm_ctdbp(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for a CTDBP with a DOSTA and FLORD attached to the
    mooring riser line, connected via an inductive modem. Loads the JSON
    formatted parsed data and applies appropriate calibration coefficients to
    convert the raw parsed data into engineering units. If no calibration
    coefficients are available, filled variables are returned and the dataset
    processing level attribute is set to "parsed". If calibration data for
    both the FLORD and the DOSTA is available, then the dataset processing
    level attribute is set to "processed". Otherwise, the dataset processing
    level is set to "partial" and the data for one or the other attached
    instrument (the one missing the calibration data) is filled with NaN's

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwarg dosta_serial: The serial number of the attached DOSTA (optional input)
    :kwarg flord_serial: The serial number of the attached FLORD (optional input)

    :return ctd: An xarray dataset with the processed CTDBP data
    """
    # process the variable length keyword arguments
    dosta_serial = kwargs.get('dosta_serial')
    flord_serial = kwargs.get('flord_serial')

    # load the json data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # create a data frame with the CTD status information
    status = json_obj2df(data, 'status')
    status['status_time'] = epoch_time(status['date_time_string'].values[0])
    status.drop(columns='date_time_string', inplace=True)
    status.rename(columns={'main_battery': 'main_battery_voltage',
                           'lithium_battery': 'lithium_battery_voltage',
                           'memory_free': 'sample_slots_free',
                           'eco_current': 'flr_current'},
                  inplace=True)

    # create a data frame with the CTD, DOSTA and FLORD data
    ctd = json_obj2df(data, 'ctd')
    nrows, _ = ctd.shape
    sensor_time = []
    for i in range(nrows):
        dt = ctd['date_time_string'][i]  # convert date/time string into a usable format
        sensor_time.append(epoch_time(dt[:2] + '-' + dt[2:5] + '-' + dt[5:9] + ' ' + dt[9:]))
    ctd['sensor_time'] = sensor_time
    ctd.drop(columns={'serial_number', 'date_time_string'}, inplace=True)
    ctd.rename(columns={'raw_oxy_calphase': 'raw_calibrated_phase',
                        'raw_oxy_temp': 'raw_oxygen_thermistor'},
               inplace=True)

    # join the status and ctd data together into a single data frame, keeping track of data types and fill values
    ctd = join_df(ctd, status)
    ctd = ctd.assign(time=ctd.index.get_level_values('time'))

    # add the deployment id, used to subset data sets
    ctd['deploy_id'] = deployment

    # calculate the practical salinity of the seawater from the temperature and conductivity measurements
    ctd['salinity'] = SP_from_C(ctd['conductivity'].values * 10.0, ctd['temperature'].values, ctd['pressure'].values)

    # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(ctd['salinity'].values, ctd['pressure'].values, lon, lat)  # absolute salinity
    ct = CT_from_t(sa, ctd['temperature'].values, ctd['pressure'].values)      # conservative temperature
    ctd['density'] = rho(sa, ct, ctd['pressure'].values)                # density

    # create filled variables to be updated if calibration coefficients are available
    empty_data = ctd['sensor_time'] * np.nan
    ctd['calibrated_phase'] = empty_data
    ctd['oxygen_thermistor_temperature'] = empty_data
    ctd['svu_oxygen_concentration'] = empty_data
    ctd['oxygen_concentration_corrected'] = empty_data
    ctd['estimated_chlorophyll'] = empty_data
    ctd['beta_700'] = empty_data
    ctd['total_optical_backscatter'] = empty_data

    # grab the calibration coefficients for the two sensors: DOSTA
    dosta_coeff = os.path.join(os.path.dirname(infile), 'ctdbp-dosta.cal_coeffs.json')
    opt = DOSTA_Calibrations(dosta_coeff)  # initialize calibration class
    proc_dosta = False
    if os.path.isfile(dosta_coeff):
        # we always want to use this file if it exists
        opt.load_coeffs()
        proc_dosta = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('DOSTA', dosta_serial, (ctd.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            opt.read_csv(csv_url)
            opt.save_coeffs()
            proc_dosta = True

    # grab the calibration coefficients for the two sensors: FLORD
    flord_coeff = os.path.join(os.path.dirname(infile), 'ctdbp-flord.cal_coeffs.json')
    flr = FLORD_Calibrations(flord_coeff)  # initialize calibration class
    proc_flord = False
    if os.path.isfile(flord_coeff):
        # we always want to use this file if it exists
        flr.load_coeffs()
        proc_flord = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('FLORD', flord_serial, (ctd.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            flr.read_csv(csv_url)
            flr.save_coeffs()
            proc_flord = True

    # if calibration data is available, process the DOSTA data
    if proc_dosta:
        ctd['calibrated_phase'] = do2_phase_volt_to_degree(ctd['raw_calibrated_phase'])
        ctd['oxygen_thermistor_temperature'] = do2_therm_volt_to_degc(ctd['raw_oxygen_thermistor'])
        ctd['svu_oxygen_concentration'] = do2_phase_to_doxy(ctd['calibrated_phase'], ctd['oxygen_thermistor_temperature'],
                                                            opt.coeffs['svu_cal_coeffs'], opt.coeffs['two_point_coeffs'])
        ctd['oxygen_concentration_corrected'] = do2_salinity_correction(ctd['oxygen_concentration'], ctd['pressure'],
                                                                        ctd['temperature'], ctd['salinity'], lat, lon)

    # if calibration data is available, process the FLORD data
    if proc_flord:
        ctd['estimated_chlorophyll'] = flo_scale_and_offset(ctd['raw_chlorophyll'], flr.coeffs['dark_chla'],
                                                            flr.coeffs['scale_chla'])
        ctd['beta_700'] = flo_scale_and_offset(ctd['raw_backscatter'], flr.coeffs['dark_beta'],
                                               flr.coeffs['scale_beta'])
        ctd['total_optical_backscatter'] = flo_bback_total(ctd['beta_700'], ctd['temperature'], ctd['salinity'],
                                                           flr.coeffs['scatter_angle'], flr.coeffs['wavelength'],
                                                           flr.coeffs['chi_factor'])

    # create an xarray data set from the data frame
    ctd = xr.Dataset.from_dataframe(ctd)

    # determine the processing level (parsed, partial, or processed)
    if (proc_dosta and not proc_flord) or (proc_flord and not proc_dosta):
        ctd.attrs['processing_level'] = 'partial'
    elif proc_dosta and proc_flord:
        ctd.attrs['processing_level'] = 'processed'
    else:
        ctd.attrs['processing_level'] = 'parsed'

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    ctd = update_dataset(ctd, platform, deployment, lat, lon, [depth, depth, depth], CTDBP)

    return ctd


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
    flord_serial = args.flord_serial
    dosta_serial = args.dosta_serial

    # process the CTDBP data and save the results to disk
    ctdbp = proc_imm_ctdbp(infile, platform, deployment, lat, lon, depth,
                           dosta_serial=dosta_serial, flord_serial=flord_serial)
    if ctdbp:
        ctdbp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
