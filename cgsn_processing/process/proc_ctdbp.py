#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_ctdbp
@file cgsn_processing/process/proc_ctdbp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the CTDBP data from the JSON formatted data
"""
import numpy as np
import os
import xarray as xr

from gsw import SP_from_C, SA_from_SP, CT_from_t, rho

from cgsn_processing.process.common import ENCODING, inputs, dict_update, epoch_time, join_df, \
    json2df, json2obj, json_obj2df, update_dataset
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_ctdbp import GLOBAL, CTDBP

from cgsn_processing.process.proc_dosta import Calibrations as DOSTA_Calibrations
from cgsn_processing.process.proc_flort import Calibrations as FLORT_Calibrations

from pyseas.data.do2_functions import do2_phase_volt_to_degree, do2_therm_volt_to_degc, \
    do2_phase_to_doxy, do2_salinity_correction
from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


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
    ctd_type = args.switch

    if ctd_type in ['solo', 'dosta', 'flort']:
        # load the json data file as a panda data frame for further processing
        ctd = json2df(infile)
        if not ctd:
            # json data file was empty, exiting
            return None

        ctd['sensor_time'] = epoch_time(ctd['ctd_date_time_string'].values[0])
        ctd.drop(columns='ctd_date_time_string', inplace=True)

        # create an xarray data set from the data frame
        ctd = xr.Dataset.from_dataframe(ctd)
        
        if ctd_type == 'flort':
            # grab the calibration coefficients for the FLORT
            flort_coeff = os.path.join(os.path.dirname(infile), 'ctdbp-flort.cal_coeffs.pkl')
            dev = FLORT_Calibrations(flort_coeff)  # initialize calibration class
            if os.path.isfile(flort_coeff):
                # we always want to use this file if it exists
                dev.load_coeffs()
            else:
                # load from the CI hosted CSV files
                csv_url = find_calibration('FLORT', args.flort_serial, (ctd.time.values.astype('int64') * 10 ** -9)[0])
                if csv_url:
                    dev.read_csv(csv_url)
                    dev.save_coeffs()
                else:
                    print('A source for the FLORT calibration coefficients for {} could not be found, ' +
                          'filling calibration coefficients with NaN'.format(infile))
                    dev.coeffs['dark_cdom'] = np.nan
                    dev.coeffs['scale_cdom'] = np.nan
                    dev.coeffs['dark_chla'] = np.nan
                    dev.coeffs['scale_chla'] = np.nan
                    dev.coeffs['dark_beta'] = np.nan
                    dev.coeffs['scale_beta'] = np.nan
                    dev.coeffs['chi_factor'] = np.nan
                    dev.coeffs['wavelength'] = np.nan
                    dev.coeffs['scatter_angle'] = np.nan
                    dev.save_coeffs()

            ctd['estimated_chlorophyll'] = flo_scale_and_offset(ctd['raw_chlorophyll'], dev.coeffs['dark_chla'],
                                                                dev.coeffs['scale_chla'])
            ctd['fluorometric_cdom'] = flo_scale_and_offset(ctd['raw_cdom'], dev.coeffs['dark_cdom'],
                                                            dev.coeffs['scale_cdom'])
            ctd['beta_700'] = flo_scale_and_offset(ctd['raw_backscatter'], dev.coeffs['dark_beta'],
                                                   dev.coeffs['scale_beta'])

    elif ctd_type == 'imm':
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
                               'memory_free': 'sample_slots_free'},
                      inplace=True)

        # create a data frame with the CTD, DOSTA and FLORD data
        ctd = json_obj2df(data, 'ctd')
        ctd['sensor_time'] = epoch_time(status['date_time_string'].values[0])
        ctd.drop(columns='date_time_string', inplace=True)
        ctd.rename(columns={'raw_oxy_calphase': 'raw_oxygen_phase',
                            'raw_oxy_temp': 'raw_oxygen_thermistor'},
                   inplace=True)

        # join the status and ctd data together into a single data frame, keeping track of data types and fill values
        joined = join_df(ctd, status)

        # create a final data set with the raw and derived CTD data and merged status data
        ctd = xr.Dataset.from_dataframe(joined)

        # grab the calibration coefficients for the two sensors: FLORD
        flort_coeff = os.path.join(os.path.dirname(infile), 'ctdmo-flord.cal_coeffs.pkl')
        dev = FLORT_Calibrations(flort_coeff)  # initialize calibration class
        if os.path.isfile(flort_coeff):
            # we always want to use this file if it exists
            dev.load_coeffs()
        else:
            # load from the CI hosted CSV files
            csv_url = find_calibration('FLORD', args.flort_serial, (ctd.time.values.astype('int64') * 10 ** -9)[0])
            if csv_url:
                dev.read_csv(csv_url)
                dev.save_coeffs()
            else:
                print('A source for the FLORD calibration coefficients for {} could not be found, ' +
                      'filling calibration coefficients with NaN'.format(infile))
                dev.coeffs['dark_chla'] = np.nan
                dev.coeffs['scale_chla'] = np.nan
                dev.coeffs['dark_beta'] = np.nan
                dev.coeffs['scale_beta'] = np.nan
                dev.coeffs['chi_factor'] = np.nan
                dev.coeffs['wavelength'] = np.nan
                dev.coeffs['scatter_angle'] = np.nan
                dev.save_coeffs()

        # grab the calibration coefficients for the two sensors: DOSTA
        dosta_coeff = os.path.join(os.path.dirname(infile), 'ctdmo-dosta.cal_coeffs.pkl')
        dev = DOSTA_Calibrations(dosta_coeff)  # initialize calibration class
        if os.path.isfile(dosta_coeff):
            # we always want to use this file if it exists
            dev.load_coeffs()
        else:
            # load from the CI hosted CSV files
            csv_url = find_calibration('DOSTA', args.dosta_serial, (ctd.time.values.astype('int64') * 10 ** -9)[0])
            if csv_url:
                dev.read_csv(csv_url)
                dev.save_coeffs()
            else:
                print('A source for the DOSTA calibration coefficients for {} could not be found, ' +
                      'filling calibration coefficients with NaN'.format(infile))
                dev.coeffs['two_point_coeffs'] = np.ones(2) * np.nan
                dev.coeffs['svu_cal_coeffs'] = np.ones(5) * np.nan
                dev.save_coeffs()

        # compute the L0 to L1 conversions
        ctd['oxygen_phase'] = do2_phase_volt_to_degree(ctd['raw_oxygen_phase'])
        ctd['oxygen_thermistor'] = do2_therm_volt_to_degc(ctd['raw_oxygen_thermistor'])
        ctd['dissolved_oxygen'] = do2_phase_to_doxy(ctd['oxygen_phase'], ctd['oxygen_thermistor'],
                                                    dev.coeffs['svu_cal_coeffs'], dev.coeffs['two_point_coeffs'])
        ctd['estimated_chlorophyll'] = flo_scale_and_offset(ctd['raw_chlorophyll'], dev.coeffs['dark_chla'],
                                                            dev.coeffs['scale_chla'])
        ctd['beta_700'] = flo_scale_and_offset(ctd['raw_backscatter'], dev.coeffs['dark_beta'],
                                               dev.coeffs['scale_beta'])
    else:
        pass

    # add the deployment id, used to subset data sets
    ctd['deploy_id'] = deployment

    # calculate the practical salinity of the seawater from the temperature and conductivity measurements
    ctd['salinity'] = SP_from_C(ctd['conductivity'] * 10.0, ctd['temperature'], ctd['pressure'])

    # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(ctd['psu'], ctd['pressure'], lon, lat)      # absolute salinity
    ct = CT_from_t(sa, ctd['temperature'], ctd['pressure'])     # conservative temperature
    ctd['density'] = rho(sa, ct, ctd['pressure'])               # density

    if ctd_type in ['dosta', 'imm']:
        # apply temperature, salinity and pressure corrections to dissolved oxygen measurement
        ctd['corrected_dissolved_oxygen'] = do2_salinity_correction(ctd['dissolved_oxygen'], ctd['pressure'],
                                                                    ctd['temperature'], ctd['salinity'], lat, lon)

    if ctd_type in ['flort', 'imm']:
        # calculate the total optical backscatter, corrected for in-situ salinity, from the volume scattering
        # coefficient (Beta) at 700 nm.
        ctd['bback'] = flo_bback_total(ctd['beta_700'], ctd['temperature'], ctd['salinity'],
                                       dev.coeffs['scatter_angle'], dev.coeffs['wavelength'], dev.coeffs['chi_factor'])

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    attrs = dict_update(GLOBAL, CTDBP)
    ctd = update_dataset(ctd, platform, deployment, lat, lon, [depth, depth, depth], attrs)

    # save the data
    ctd.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
