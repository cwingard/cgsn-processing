#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_dosta
@file cgsn_processing/process/proc_cspp_dosta.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP DOSTA data from JSON formatted source data
"""
import numpy as np
import os
import re
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update, dt64_epoch
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_NUTNR
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_nutnr import Calibrations

from pyseas.data.nit_functions import ts_corrected_nitrate
from gsw import z_from_p


def proc_cspp_nutnr(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main NUTNR processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    along with data from the co-located CTD, the nitrate concentration is
    recalculated from the raw absorbance measurements with temperature and
    salinity corrections applied. Otherwise, filled variables are returned and
    the dataset processing level attribute is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed
    **suna_serial: serial number of the SUNA instrument
    **ctd_name: Name of directory with data from a co-located CTD. This
        data will be used to apply salinity and density corrections to the
        data. Otherwise, the salinity corrected oxygen concentration is
        filled with NaN's

    :return nutnr: xarray dataset with the processed DOSTA data
    """
    # process the variable length keyword arguments
    serial_number = kwargs.get('suna_serial')
    ctd_name = kwargs.get('ctd_name')

    # load the json data file as a dictionary object for further processing
    data = json2df(infile)
    if data.empty:
        # json data file was empty, exiting
        return None

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'nutnr.cal_coeffs.json')
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # check for the source of the calibration coefficients and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it already exists
        dev.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        sampling_time = data['time'][0].value / 10.0 ** 9
        csv_url = find_calibration('NUTNR', serial_number, sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True
        else:
            print('A source for the NUTNR calibration coefficients for {} could not be found'.format(infile))

    # set the sensor time from the date string and decimal hours
    ds = pd.to_datetime(str(data['year']) + str(data['day_of_year']), format='%Y%j', utc=True)
    td = pd.to_timedelta(data['decimal_hours'], 'h')
    data['sensor_time'] = dt64_epoch(ds + td)

    # only keep the light frame measurements
    data = data[data['measurement_type'] == 'SLB']

    # remove the variables we will no longer use and rename select remaining variables for consistency
    data.drop(columns=['suspect_timestamp', 'year', 'day_of_year', 'decimal_hours'], inplace=True)
    data.rename(columns={'fit_rmse': 'rms_error',
                         'dark_value': 'seawater_dark'}, inplace=True)
    if 'absorbance_250' in data.columns:
        # check to see if this data frame has an older, incorrectly named variable
        data.rename(columns={'absorbance_250': 'absorbance_350'}, inplace=True)

    # create the time coordinate array and set up a base data frame
    nutnr_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(nutnr_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # pop the raw channels array out of data (we will put it back in later)
    channels = np.array(np.vstack(data.pop('channel_measurements')))

    # set up and load the 1D parsed data into the data frame
    for v in data.columns:
        if v not in ['time']:
            df[v] = np.atleast_1d(data[v])

    # create a missing data array for processed variables and pre-set them to NaN
    empty_data = np.atleast_1d(data['serial_number']).astype(int) * np.nan

    # processed 1D variables to be created if a device file is available
    df['depth'] = empty_data
    df['ctd_pressure'] = empty_data
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data
    df['corrected_nitrate'] = empty_data
    df['corrected_nitrogen_in_nitrate'] = empty_data

    # default wavelength array if we are missing calibration coefficients
    wavelengths = np.linspace(start=190, stop=395, num=256)

    ctd = pd.DataFrame()
    if ctd_name:
        ctd_file = re.sub('SNA_SNA', 'PPB_CTD', os.path.basename(infile))
        ctd_dir = re.sub('nutnr', 'ctdpf', os.path.dirname(infile))

        if os.path.isfile(os.path.join(ctd_dir, ctd_file)):
            ctd = json2df(os.path.join(ctd_dir, ctd_file))

    if not ctd.empty:
        # interpolate the CTD data into the profile
        pressure = np.interp(data['time'], ctd['time'], ctd['pressure'])
        df['ctd_pressure'] = pressure

        temperature = np.interp(data['time'], ctd['time'], ctd['temperature'])
        df['ctd_temperature'] = temperature

        salinity = np.interp(data['time'], ctd['time'], ctd['salinity'])
        df['ctd_salinity'] = salinity

    if proc_flag and not ctd.empty:
        # create the wavelengths array
        wavelengths = (dev.coeffs['wl']).astype(float)

        # Calculate the corrected nitrate concentration (uM) accounting for temperature and salinity and the pure
        # water calibration values.
        df['corrected_nitrate'] = ts_corrected_nitrate(dev.coeffs['cal_temp'], wavelengths, dev.coeffs['eno3'],
                                                       dev.coeffs['eswa'], dev.coeffs['di'], df['seawater_dark'],
                                                       df['ctd_temperature'], df['ctd_salinity'], channels,
                                                       df['measurement_type'])

        df['corrected_nitrogen_in_nitrate'] = df['corrected_nitrate'] / 1000 * 14.0067

    # now that we no longer need it, get rid of the measurement type
    df.drop(columns=['measurement_type'], inplace=True)

    # convert the 1D data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the 2D arrays for the raw channel measurements
    ch = xr.Dataset({
        'channel_measurements': (['time', 'wavelengths'], channels),
    }, coords={'time': (['time'], pd.to_datetime(nutnr_time, unit='s')),
               'wavelengths': wavelengths})

    # combine the 1D and 2D datasets into a single xarray dataset
    nutnr = xr.merge([ds, ch])

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    nutnr['deploy_id'] = xr.Variable('time', np.tile(deployment, len(nutnr.time)).astype(str))
    nutnr['profile_id'] = xr.Variable('time', np.tile(profile_id, len(nutnr.time)).astype(str))

    # calculate the depth range for the NetCDF global attributes: deployment depth and the profile min/max range
    nutnr['depth'] = -1 * z_from_p(nutnr['ctd_pressure'], lat)
    depth_range = [depth, nutnr['depth'].min().values, df['depth'].max().values]

    attrs = dict_update(CSPP_NUTNR, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    nutnr = update_dataset(nutnr, platform, deployment, lat, lon, depth_range, attrs)
    if proc_flag:
        nutnr.attrs['processing_level'] = 'processed'
    else:
        nutnr.attrs['processing_level'] = 'parsed'

    return nutnr


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
    serial = args.serial  # serial number of the SUNA instrument
    ctd_name = args.devfile  # name of co-located CTD

    # process the NUTNR data and save the results to disk
    nutnr = proc_cspp_nutnr(infile, platform, deployment, lat, lon, depth, suna_serial=serial, ctd_name=ctd_name)
    if nutnr:
        nutnr.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
