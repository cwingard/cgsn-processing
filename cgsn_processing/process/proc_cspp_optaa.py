#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_optaa
@file cgsn_processing/process/proc_cspp_optaa.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP OPTAA data from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import re
import warnings
import xarray as xr

from gsw import z_from_p
from scipy.interpolate import interp1d

from cgsn_processing.process.common import inputs, json2obj, update_dataset, ENCODING, FILL_INT, FILL_NAN
from cgsn_processing.process.configs.attr_optaa import OPTAA
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_optaa import Calibrations, apply_dev, apply_tscorr, apply_scatcorr, \
    calculate_ratios, estimate_chl_poc


def proc_cspp_optaa(infile, coeff_file, platform, deployment, lat, lon, depth):
    """
    Processing function for a CSPP-mounted OPTA. Loads the JSON formatted
    parsed data and applies appropriate calibration coefficients to convert the
    raw parsed data into engineering units. If no calibration coefficients are
    available, filled variables are returned and the dataset processing level
    attribute is set to "parsed". If the calibration coefficients are available,
    the the dataset processing level attribute is set to "processed".

    :param infile: JSON formatted parsed data file
    :param coeff_file: JSON formatted data file with the factory calibration
        coefficients. Will attempt to download the calibration coefficients
         and create this file if it does not exist.
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longittude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return optaa: An xarray dataset with the processed CSPP OPTAA data
    """
    # load the json data file as a dictionary object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub('\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # load the instrument calibration data
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it already exists
        dev.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('OPTAA', str(data['serial_number'][0]), data['time'][0])
        if csv_url:
            tca_url = re.sub('.csv', '__CC_taarray.ext', csv_url)
            tcc_url = re.sub('.csv', '__CC_tcarray.ext', csv_url)
            dev.read_devurls(csv_url, tca_url, tcc_url)
            dev.save_coeffs()
            proc_flag = True

    # check the device file coefficients against the data file contents
    if dev.coeffs['serial_number'] != data['serial_number'][0]:
        raise Exception('Serial Number mismatch between ac-s data and the device file.')
    if dev.coeffs['num_wavelengths'] != data['num_wavelengths'][0]:
        raise Exception('Number of wavelengths mismatch between ac-s data and the device file.')

    # create the time coordinate array and setup a base data frame
    optaa_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(optaa_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # setup and load the 1D parsed data
    df['z'] = depth
    empty_data = np.atleast_1d(data['serial_number']).astype(np.int32) * np.nan
    # raw data parsed from the data file
    df['serial_number'] = np.atleast_1d(data['serial_number']).astype(np.int32)
    df['elapsed_run_time'] = np.atleast_1d(data['elapsed_run_time']).astype(np.int32)
    df['internal_temp_raw'] = np.atleast_1d(data['internal_temp_raw']).astype(np.int32)
    df['external_temp_raw'] = np.atleast_1d(data['external_temp_raw']).astype(np.int32)
    df['pressure_raw'] = np.atleast_1d(data['pressure_raw']).astype(np.int32)
    df['a_signal_dark'] = np.atleast_1d(data['a_signal_dark']).astype(np.int32)
    df['a_reference_dark'] = np.atleast_1d(data['a_reference_dark']).astype(np.int32)
    df['c_signal_dark'] = np.atleast_1d(data['c_signal_dark']).astype(np.int32)
    df['c_reference_dark'] = np.atleast_1d(data['c_reference_dark']).astype(np.int32)
    # processed variables to be created if a device file is available
    df['internal_temp'] = empty_data
    df['external_temp'] = empty_data
    df['pressure'] = empty_data
    df['estimated_chlorophyll'] = empty_data
    df['estimated_poc'] = empty_data
    df['ratio_cdom'] = empty_data
    df['ratio_carotenoids'] = empty_data
    df['ratio_phycobilins'] = empty_data
    df['ratio_qband'] = empty_data

    # check for data from the required co-located CTD for this profile
    ctd_file = re.sub('optaa', 'ctdpf', infile)
    ctd_file = re.sub('ACS_ACS', 'PPB_CTD', ctd_file)
    ctd = json2obj(ctd_file)
    if not ctd.empty:
        # interpolate the CTD data into the profile
        dbar = interp1d(ctd['time'], ctd['pressure'], bounds_error=False)
        df['ctd_depth'] = z_from_p(dbar(optaa_time), lat)

        degc = interp1d(ctd['time'], ctd['temperature'], bounds_error=False)
        df['ctd_temperature'] = degc(optaa_time)
        temperature = df['ctd_temperature'].values

        psu = interp1d(ctd['time'], ctd['salinity'], bounds_error=False)
        df['ctd_salinity'] = psu(optaa_time)
        salinity = df['ctd_salinity'].values
    else:
        raise Exception('Corresponding CTD data file is empty or cannot be located.')

    # convert the data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the 2D arrays from the raw a and c channel measurements using the number of wavelengths
    # padded to 100 as the dimensional array.
    wavelength_number = np.arange(100).astype(np.int32)  # used as a dimensional variable
    num_wavelengths = np.array(data['a_signal_raw']).shape[1]
    pad = 100 - num_wavelengths
    fill_nan = np.ones(pad) * FILL_NAN
    fill_int = (np.ones(pad) * FILL_INT).astype(np.int32)
    a_wavelengths = np.concatenate([dev.coeffs['a_wavelengths'], fill_nan])
    c_wavelengths = np.concatenate([dev.coeffs['c_wavelengths'], fill_nan])
    empty_data = np.concatenate([np.array(data['a_signal_raw']).astype(np.int32),
                                 np.tile(fill_nan, (len(optaa_time), 1))], axis=1) * np.nan
    ac = xr.Dataset({
        # raw data parsed from the data file
        'a_wavelengths': (['time', 'wavelength_number'], np.tile(a_wavelengths, (len(optaa_time), 1))),
        'a_signal_raw': (['time', 'wavelength_number'],
                         np.concatenate([np.array(data['a_signal_raw']).astype(np.int32),
                                         np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'a_reference_raw': (['time', 'wavelength_number'],
                            np.concatenate([np.array(data['a_reference_raw']).astype(np.int32),
                                            np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'c_wavelengths': (['time', 'wavelength_number'], np.tile(c_wavelengths, (len(optaa_time), 1))),
        'c_signal_raw': (['time', 'wavelength_number'],
                         np.concatenate([np.array(data['c_signal_raw']).astype(np.int32),
                                         np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'c_reference_raw': (['time', 'wavelength_number'],
                            np.concatenate([np.array(data['c_reference_raw']).astype(np.int32),
                                            np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        # processed variables to be created if a device file is available
        'apd': (['time', 'wavelength_number'], empty_data),
        'apd_ts': (['time', 'wavelength_number'], empty_data),
        'apd_ts_s': (['time', 'wavelength_number'], empty_data),
        'cpd': (['time', 'wavelength_number'], empty_data),
        'cpd_ts': (['time', 'wavelength_number'], empty_data)
    }, coords={'time': (['time'], pd.to_datetime(optaa_time, unit='s')),
               'wavelength_number': wavelength_number})

    # combine the 1D and 2D datasets into a single xarray dataset
    raw = xr.merge([ds, ac])

    # add the deployment and profile IDs to the dataset
    raw['deploy_id'] = xr.Variable('time', np.tile(deployment, len(raw.time)).astype(np.str))
    raw['profile_id'] = xr.Variable('time', np.tile(profile_id, len(raw.time)).astype(np.str))

    # calculate the depth range for the NetCDF global attributes: deployment depth and min/max range
    depth_range = [depth, df['ctd_depth'].min(), df['ctd_depth'].max()]

    # if no calibration file was found, save the dataset as-is
    if not proc_flag:  # no device file is available
        # updating the data set with the appropriate attributes
        raw = update_dataset(raw, platform, deployment, lat, lon, depth_range, OPTAA)
        raw['wavelength_number'].attrs['actual_wavelengths'] = data['num_wavelengths'][0]
        raw.attrs['processing_level'] = 'parsed'

        # return the final dataset, with processed data filled since the calibration data is missing
        warnings.warn('Calibration data is missing. Processed data is filled with either a NaN or -9999999.')
        return raw

    # apply the device file and the temperature, salinity and scatter corrections
    proc = apply_dev(raw, dev.coeffs)
    proc = apply_tscorr(proc, dev.coeffs, temperature, salinity)
    proc = apply_scatcorr(proc, dev.coeffs)

    # estimate chlorophyll-a and POC concentrations from the absorption and attenuation data, respectively.
    proc = estimate_chl_poc(proc, dev.coeffs)

    # calculate pigment and CDOM ratios to provide variables useful in characterizing the community structure and
    # the status of the sensor itself (biofouling tracking).
    proc = calculate_ratios(proc, dev.coeffs)

    # update the data set with the appropriate attributes
    proc = update_dataset(proc, platform, deployment, lat, lon, depth_range, OPTAA)
    proc['wavelength_number'].attrs['actual_wavelengths'] = data['num_wavelengths'][0]
    proc.attrs['processing_level'] = 'processed'

    # return the final processed dataset
    return proc


def main(argv=None):
    """
    Command line function to process the OPTAA data using the proc_cspp_optaa
    function. Command line arguments are parsed and passed to the function.

    :param argv: List of command line arguments
    """
    # load the input arguments
    args = inputs(argv)
    infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    coeff_file = os.path.abspath(args.coeff_file)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # process the OPTAA data and save the results to disk
    optaa = proc_cspp_optaa(infile, coeff_file, platform, deployment, lat, lon, depth)
    if optaa:
        optaa.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
