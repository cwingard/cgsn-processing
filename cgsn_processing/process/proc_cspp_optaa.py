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
import xarray as xr

from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, json2obj, update_dataset, ENCODING, FILL_INT
from cgsn_processing.process.configs.attr_optaa import OPTAA
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_optaa import Calibrations, apply_dev, apply_tscorr, apply_scatcorr, \
    calculate_ratios, estimate_chl_poc


def proc_cspp_optaa(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for a CSPP-mounted OPTA. Loads the JSON formatted
    parsed data and applies appropriate calibration coefficients to convert the
    raw parsed data into engineering units. If no calibration coefficients are
    available, filled variables are returned and the dataset processing level
    attribute is set to "parsed". If the calibration coefficients are available,
    then the dataset processing level attribute is set to "processed".

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed
    **ctd_name: Name of directory with data from a co-located CTD. This
        data will be used to apply salinity and density corrections to the
        data. Otherwise, the salinity corrected oxygen concentration is
        filled with NaN's

    :return optaa: xarray dataset with the processed CSPP OPTAA data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')

    # load the instrument calibration data
    coeff_file = os.path.join(os.path.dirname(infile), 'optaa.cal_coeffs.json')
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # load the json data file as a dictionary object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

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

    # create the time coordinate array and set up a base data frame
    optaa_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(optaa_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # set up and load the 1D parsed data
    empty_data = np.atleast_1d(data['serial_number']).astype(int) * np.nan
    # raw data parsed from the data file
    df['serial_number'] = np.atleast_1d(data['serial_number']).astype(int)
    df['elapsed_run_time'] = np.atleast_1d(data['elapsed_run_time']).astype(int)
    df['internal_temp_raw'] = np.atleast_1d(data['internal_temp_raw']).astype(int)
    df['external_temp_raw'] = np.atleast_1d(data['external_temp_raw']).astype(int)
    df['pressure_raw'] = np.atleast_1d(data['pressure_raw']).astype(int)
    df['a_signal_dark'] = np.atleast_1d(data['a_signal_dark']).astype(int)
    df['a_reference_dark'] = np.atleast_1d(data['a_reference_dark']).astype(int)
    df['c_signal_dark'] = np.atleast_1d(data['c_signal_dark']).astype(int)
    df['c_reference_dark'] = np.atleast_1d(data['c_reference_dark']).astype(int)
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

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    ctd = pd.DataFrame()
    if ctd_name:
        ctd_file = re.sub('ACS_ACS', 'PPB_CTD', os.path.basename(infile))
        ctd_dir = re.sub('optaa', 'ctdpf', os.path.dirname(infile))

        if os.path.isfile(os.path.join(ctd_dir, ctd_file)):
            ctd = json2df(os.path.join(ctd_dir, ctd_file))

    if not ctd.empty:
        # interpolate the CTD data into the profile
        pressure = np.interp(optaa_time, ctd['time'], ctd['pressure'])
        df['ctd_pressure'] = pressure

        temperature = np.interp(optaa_time, ctd['time'], ctd['temperature'])
        df['ctd_temperature'] = temperature

        salinity = np.interp(optaa_time, ctd['time'], ctd['salinity'])
        df['ctd_salinity'] = salinity
    else:
        raise Exception('Corresponding CTD data file is empty or cannot be located.')

    # convert the 1D data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the 2D arrays from the raw a and c channel measurements using the number of wavelengths
    # padded to 100 as the dimensional array.
    wavelength_number = np.arange(100).astype(int)  # used as a dimensional variable
    num_wavelengths = np.array(data['a_signal_raw']).shape[1]
    pad = 100 - num_wavelengths
    fill_nan = np.ones(pad) * np.nan
    fill_int = (np.ones(pad) * FILL_INT).astype(int)
    a_wavelengths = np.concatenate([dev.coeffs['a_wavelengths'], fill_nan])
    c_wavelengths = np.concatenate([dev.coeffs['c_wavelengths'], fill_nan])
    empty_data = np.concatenate([np.array(data['a_signal_raw']).astype(int),
                                 np.tile(fill_nan, (len(optaa_time), 1))], axis=1) * np.nan
    ac = xr.Dataset({
        # raw data parsed from the data file
        'a_wavelengths': (['time', 'wavelength_number'], np.tile(a_wavelengths, (len(optaa_time), 1))),
        'a_signal_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['a_signal_raw']).astype(int),
                         np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'a_reference_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['a_reference_raw']).astype(int),
                            np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'c_wavelengths': (['time', 'wavelength_number'], np.tile(c_wavelengths, (len(optaa_time), 1))),
        'c_signal_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['c_signal_raw']).astype(int),
                         np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'c_reference_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['c_reference_raw']).astype(int),
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
    optaa = xr.merge([ds, ac])

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    optaa['deploy_id'] = xr.Variable('time', np.tile(deployment, len(optaa.time)).astype(str))
    optaa['profile_id'] = xr.Variable('time', np.tile(profile_id, len(optaa.time)).astype(str))

    # calculate the depth range for the NetCDF global attributes: deployment depth and the profile min/max range
    z = -1 * z_from_p(df['ctd_pressure'], lat)
    depth_range = [depth, z.min(), z.max()]

    # set the processed attribute to parsed
    optaa.attrs['processing_level'] = 'parsed'

    # if there is calibration data, apply it now
    if proc_flag:
        # apply the device file and the temperature, salinity and scatter corrections
        optaa = apply_dev(optaa, dev.coeffs)
        optaa = apply_tscorr(optaa, dev.coeffs, temperature, salinity)
        optaa = apply_scatcorr(optaa, dev.coeffs)

        # estimate chlorophyll-a and POC concentrations from the absorption and attenuation data, respectively.
        optaa = estimate_chl_poc(optaa, dev.coeffs)

        # calculate pigment and CDOM ratios to provide variables useful in characterizing the community structure and
        # the status of the sensor itself (e.g. estimating bio-fouling).
        optaa = calculate_ratios(optaa, dev.coeffs)

        # set the processed attribute to processed
        optaa.attrs['processing_level'] = 'processed'

    # update the data set with the appropriate attributes
    optaa = update_dataset(optaa, platform, deployment, lat, lon, depth_range, OPTAA)
    optaa['wavelength_number'].attrs['actual_wavelengths'] = data['num_wavelengths'][0]

    # return the final processed dataset
    return optaa


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
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lon = args.longitude
    depth = args.depth

    # process the OPTAA data and save the results to disk
    optaa = proc_cspp_optaa(infile, platform, deployment, lat, lon, depth)
    if optaa:
        optaa.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
