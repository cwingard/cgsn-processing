#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_nutnr
@file cgsn_processing/process/proc_nutnr.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Nitrate concentration data from the NUTNR
"""
import json
import numpy as np
import os
import pandas as pd
import re
import xarray as xr

from datetime import timedelta

from cgsn_processing.process.common import Coefficients, inputs, json2df, colocated_ctd, dict_update, \
    update_dataset, dt64_epoch, ENCODING, FILL_INT
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_nutnr import NUTNR
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.nit_functions import ts_corrected_nitrate
from gsw import SP_from_C, p_from_z, z_from_p


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the NUTNR pure water calibration coefficients for a unit. Values
        come from either a serialized object created per instrument and
        deployment (calibration coefficients do not change in the middle of a
        deployment), or from parsed CSV files maintained on GitHub by the OOI
        CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url
        self.coeffs = {}

    def read_csv(self, csv_url):
        """
        Reads the values from a NUTNR calibration file already parsed and
        stored on GitHub as a CSV files. Note, the formatting of those files
        puts some constraints on this process. If someone has a cleaner method,
        I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            if row[1] == 'CC_cal_temp':
                coeffs['cal_temp'] = float(row[2])

            if row[1] == 'CC_di':
                coeffs['di'] = np.array(json.loads(row[2]))

            if row[1] == 'CC_eno3':
                coeffs['eno3'] = np.array(json.loads(row[2]))

            if row[1] == 'CC_eswa':
                coeffs['eswa'] = np.array(json.loads(row[2]))

            if row[1] == 'CC_lower_wavelength_limit_for_spectra_fit':
                coeffs['wllower'] = int(row[2])

            if row[1] == 'CC_upper_wavelength_limit_for_spectra_fit':
                coeffs['wlupper'] = int(row[2])

            if row[1] == 'CC_wl':
                coeffs['wl'] = np.array(json.loads(row[2]))

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_nutnr(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main NUTNR processing function. Loads the JSON formatted, parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the dataset processing level attribute is set to "processed". Otherwise,
    filled variables are returned and the dataset processing level attribute
    is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    **kwargs ctd_name: Name of directory with data from a co-located CTD. This
            data will be used to calculate the optical backscatter, which
            requires the temperature and salinity data from the CTD. Otherwise,
            the calculated nitrate concentration is filled with NaN's
    **kwargs burst: Boolean flag to indicate whether to apply burst averaging
            to the data. Default is to not apply burst averaging.

    :return nutnr: An xarray dataset with the processed nutnr data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')
    burst = kwargs.get('burst')

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
        serial_number = str(data.serial_number[0])
        sampling_time = data['time'][0].value / 10.0 ** 9
        csv_url = find_calibration('NUTNR', serial_number, sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True

    # set the sensor time from the date string and decimal hours
    ds = pd.to_datetime(data['date_string'], format='%Y%j', utc=True)
    td = pd.to_timedelta(data['decimal_hours'], 'h')
    data['sensor_time'] = dt64_epoch(ds + td)

    # determine the instrument type and drop all dark frame measurements.
    data = data[(data['measurement_type'] == 'NLC') | (data['measurement_type'] == 'NLF')
                | (data['measurement_type'] == 'SLF')]
    data = data.reset_index(drop=True)
    measurement_type = data['measurement_type'][0]
    instrument_type = None
    if measurement_type == 'NLC':
        instrument_type = 'condensed'   # ISUS Condensed Frames
    if measurement_type == 'NLF':
        instrument_type = 'isus'        # ISUS Full Frames
    if measurement_type == 'SLF':
        instrument_type = 'suna'        # SUNA Full Frames

    # remove the variables we will no longer use
    data.drop(columns=['date_time_string', 'date_string', 'decimal_hours'], inplace=True)

    # rename select variables to better align the datasets
    if instrument_type == 'suna':
        data.rename(columns={'fit_rmse': 'rms_error',
                             'dark_value': 'seawater_dark'}, inplace=True)
        if 'absorbance_250' in data.columns:
            # check to see if this data frame has an older, incorrectly named variable
            data.rename(columns={'absorbance_250': 'absorbance_350'}, inplace=True)
    else:
        data.rename(columns={'auxiliary_fit_1st': 'fit_auxiliary_1',
                             'auxiliary_fit_2nd': 'fit_auxiliary_2',
                             'auxiliary_fit_3rd': 'fit_auxiliary_3'}, inplace=True)

    # create the time coordinate array and set up a base data frame
    nutnr_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(nutnr_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # pop the raw channels array out of data (we will put it back in later)
    if instrument_type in ['isus', 'suna']:
        channels = np.array(np.vstack(data.pop('channel_measurements')))
    else:
        empty_data = dev.coeffs['wl'].astype(int) * 0
        channels = np.tile(empty_data, (len(nutnr_time), 1))

    # set up and load the 1D parsed data into the data frame
    for v in data.columns:
        if v not in ['time']:
            df[v] = np.atleast_1d(data[v])

    # add any missing data
    empty_data = np.atleast_1d(data['serial_number']).astype(int) * np.nan
    if instrument_type == 'condensed':
        # add the 1D variables for the ISUS using a fill value
        df['temperature_internal'] = empty_data
        df['temperature_spectrometer'] = empty_data
        df['temperature_lamp'] = empty_data
        df['lamp_on_time'] = np.atleast_1d(data['serial_number']).astype(int) * 0 + FILL_INT
        df['humidity'] = empty_data
        df['voltage_lamp'] = empty_data
        df['voltage_analog'] = empty_data
        df['voltage_main'] = empty_data
        df['average_reference'] = empty_data
        df['variance_reference'] = empty_data
        df['seawater_dark'] = empty_data
        df['spectral_average'] = empty_data

    # processed 1D variables to be created if a device file is available
    df['corrected_nitrate'] = empty_data
    df['corrected_nitrogen_in_nitrate'] = empty_data

    # use a default depth array for later metadata settings (will update if co-located CTD data is available)
    depth = [depth, depth, depth]

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    df['ctd_pressure'] = empty_data
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data

    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if not ctd.empty:
        # test to see if the CTD covers our time period for this nutnr file
        td = timedelta(hours=1)
        coverage = ctd.time.min() <= min(nutnr_time) and ctd.time.max() + td >= max(nutnr_time)

        # reset initial estimates of in-situ temperature and salinity if we have full coverage
        if coverage:
            # The Global moorings may use the data from the METBK-CT for the NUTNR mounted on the buoy subsurface plate.
            # We'll rename the data columns from the METBK to match other CTDs and process accordingly.
            if re.match('metbk', ctd_name):
                # rename temperature and salinity
                ctd = ctd.rename(columns={
                    'sea_surface_temperature': 'temperature',
                    'sea_surface_conductivity': 'conductivity'
                })
                # set the pressure (dbar) from the approximate depth (m) below the water line.
                ctd['pressure'] = p_from_z(-1.25, lat)

            pressure = np.interp(nutnr_time, ctd.time, ctd.pressure)
            df['ctd_pressure'] = pressure
            depth[0] = z_from_p(np.mean(pressure), lat) * -1
            depth[1] = z_from_p(pressure.min(), lat) * -1
            depth[2] = z_from_p(pressure.max(), lat) * -1

            temperature = np.interp(nutnr_time, ctd.time, ctd.temperature)
            df['ctd_temperature'] = temperature

            salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
            salinity = np.interp(nutnr_time, ctd.time, salinity)
            df['ctd_salinity'] = salinity

    # Calculate the corrected nitrate concentration (uM) accounting for temperature and salinity and the pure
    # water calibration values. Use the corrected nitrate Molar concentration to estimate the nitrogen mass
    # concentration.
    if instrument_type != 'condensed' and proc_flag:
        df['corrected_nitrate'] = ts_corrected_nitrate(dev.coeffs['cal_temp'], dev.coeffs['wl'], dev.coeffs['eno3'],
                                                       dev.coeffs['eswa'], dev.coeffs['di'], df['seawater_dark'],
                                                       df['ctd_temperature'], df['ctd_salinity'], channels,
                                                       df['measurement_type'], dev.coeffs['wllower'],
                                                       dev.coeffs['wlupper'])
        df['corrected_nitrogen_in_nitrate'] = df['corrected_nitrate'] / 1000 * 14.0067

    # now that we no longer need it, get rid of the measurement type
    df.drop_vars(columns=['measurement_type'], inplace=True)

    # convert the 1D data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the 2D arrays for the raw channel measurements
    wavelengths = dev.coeffs['wl']
    ch = xr.Dataset({
        'channel_measurements': (['time', 'wavelengths'], channels),
    }, coords={'time': (['time'], pd.to_datetime(nutnr_time, unit='s')),
               'wavelengths': wavelengths})

    # combine the 1D and 2D datasets into a single xarray dataset
    nutnr = xr.merge([ds, ch])

    # apply a median average to the burst (if desired)
    if burst:
        # resample to a 15-minute interval
        nutnr['time'] = nutnr.time + pd.Timedelta('450s')
        nutnr = nutnr.resample(time='900s').median(dim='time', keep_attrs=True)

        # resampling will fill in missing time steps with NaNs. Use the serial_number variable
        # as a proxy variable to find cases where data is filled with a NaN, and delete those records.
        nutnr = nutnr.where(~np.isnan(nutnr.serial_number), drop=True)

        # reset original integer values
        int_arrays = ['serial_number', 'channel_measurements', 'lamp_on_time', 'spectral_average', 'seawater_dark',
                      'integration_factor', 'main_current']
        for var in nutnr.variables:
            if var in int_arrays:
                nutnr[var] = nutnr[var].astype(int)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    nutnr['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(nutnr.time)).astype(str))
    attrs = dict_update(NUTNR, SHARED)
    nutnr = update_dataset(nutnr, platform, deployment, lat, lon, depth, attrs)
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
    ctd_name = args.devfile  # name of co-located CTD
    burst = args.burst

    # process the NUTNR data and save the results to disk
    nutnr = proc_nutnr(infile, platform, deployment, lat, lon, depth, ctd_name=ctd_name, burst=burst)
    if nutnr:
        nutnr.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
