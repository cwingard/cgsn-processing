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

from cgsn_processing.process.common import Coefficients, inputs, json2obj, colocated_ctd
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_nutnr import ISUS, SUNA
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.nit_functions import ts_corrected_nitrate
from gsw import SP_from_C, p_from_z


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

    def read_csv(self, csv_url):
        """
        Reads the values from a NUTNR calibration file already parsed and
        stored on Github as a CSV files. Note, the formatting of those files
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

    :kwargs ctd_name: Name of directory with data from a co-located CTD. This
           data will be used to calculate the optical backscatter, which
           requires the temperature and salinity data from the CTD. Otherwise
           the optical backscatter is filled with NaN's
    :kwargs burst: Boolean flag to indicate whether or not to apply burst
           averaging to the data. Default is to not apply burst averaging.

    :return nutnr: An xarray dataset with the processed nutnr data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')
    burst = kwargs.get('burst')

    # load the json data file as a dictionary object for further processing
    data = json2obj(infile)
    if data.empty:
        # json data file was empty, exiting
        return None

    # setup the instrument calibration data object
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

    # clean-up and re-organize the timing variables
    ds = pd.to_datetime(data['date_string'], format='%Y%j', utc=True)
    td = pd.to_timedelta(data['decimal_hours'], 'h')
    data['internal_timestamp'] = ds + td
    data.drop(columns=['date_time_string', 'date_string', 'decimal_hours'], inplace=True)

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
    if measurement_type == 'NLC':
        instrument_type = 'suna'        # SUNA Full Frames

    # pop the raw_channels array out of the dataframe (we will put it back in later)
    if instrument_type in ['isus', 'suna']:
        channels = np.array(np.vstack(data.pop('channel_measurements')))

    # create the time coordinate array and setup a base data frame
    nutnr_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(nutnr_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # setup and load the 1D parsed data
    empty_data = np.atleast_1d(data['serial_number']).astype(int) * np.nan
    # raw data parsed from the data file
    for v in data.columns:
        if v not in ['time', 'measurement_type']:
            df[v] = np.atleast_1d(data[v])

    if instrument_type == 'condensed':
        # add the 1D variables for the ISUS using a fill value
        df['temperature_internal'] = empty_data
        df['temperature_spectrometer'] = empty_data
        df['temperature_lamp'] = empty_data
        df['lamp_on_time'] = empty_data
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

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    df['ctd_pressure'] = empty_data
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data

    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if not ctd.empty:
        # set the CTD and NUTNR time to the same units of seconds since 1970-01-01
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this optaa file
        td = timedelta(hours=1).total_seconds()
        coverage = ctd_time.min() <= min(nutnr_time) and ctd_time.max() + td >= max(nutnr_time)

        # reset initial estimates of in-situ temperature and salinity if we have full coverage
        if coverage:
            pressure = np.mean(np.interp(nutnr_time, ctd_time, ctd.pressure))
            df['ctd_pressure'] = pressure

            temperature = np.mean(np.interp(nutnr_time, ctd_time, ctd.temperature))
            df['ctd_temperature'] = temperature

            salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
            salinity = np.mean(np.interp(nutnr_time, ctd_time, salinity))
            df['ctd_salinity'] = salinity

    # Calculate the corrected nitrate concentration (uM) accounting for temperature and salinity and the pure
    # water calibration values.
    if instrument_type != 'condensed':
        df['corrected_nitrate'] = ts_corrected_nitrate(dev.coeffs['cal_temp'], dev.coeffs['wl'], dev.coeffs['eno3'],
                                                       dev.coeffs['eswa'], dev.coeffs['di'], df['dark_value'],
                                                       df['temperature'], df['salinity'], channels,
                                                       measurement_type, dev.coeffs['wllower'],
                                                       dev.coeffs['wlupper'])

    # convert the 1D data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the 2D arrays for the raw channel measurements
    wavelengths = dev.coeffs['wl']
    num_wavelengths = wavelengths.shape

    channels = xr.Dataset({
        # raw data parsed from the data file
        'channel_measurements': (['time', 'wavelengths'], channels),
    }, coords={'time': (['time'], pd.to_datetime(nutnr_time, unit='s')),
               'wavelengths': wavelengths})

    # combine the 1D and 2D datasets into a single xarray dataset
    optaa = xr.merge([ds, ac])

    # convert the dataframe to a format suitable for the pocean OMTs, adding the deployment name
    df['deploy_id'] = deployment


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

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    if args.switch == 1:    # dataset includes the full spectral output
        # check for the source of calibration coeffs and load accordingly
        coeff_file = os.path.abspath(args.coeff_file)
        dev = Calibrations(coeff_file)  # initialize calibration class
        if os.path.isfile(coeff_file):
            # we always want to use this file if it exists
            dev.load_coeffs()
        else:
            # load from the CI hosted CSV files
            csv_url = find_calibration('NUTNR', str(df.serial_number[0]), (df.time.values.astype('int64') / 1e9)[0])
            if csv_url:
                dev.read_csv(csv_url)
                dev.save_coeffs()
            else:
                print('A source for the NUTNR calibration coefficients for {} could not be found'.format(infile))
                return None

        # Merge the co-located CTD temperature and salinity data and calculate the corrected nitrate concentration
        nutnr_path, nutnr_file = os.path.split(infile)
        ctd_file = re.sub('nutnr[\w]*', ctd_name, nutnr_file)
        ctd_path = re.sub('nutnr', re.sub('[\d]*', '', ctd_name), nutnr_path)
        ctd = json2df(os.path.join(ctd_path, ctd_file))
        if not ctd.empty and len(ctd.index) >= 3:
            # The Global moorings may use the data from the METBK-CT for the NUTNR mounted on the buoy subsurface plate.
            # We'll rename the data columns from the METBK to match other CTDs and process accordingly.
            if re.match('metbk', ctd_name):
                # rename temperature and salinity
                ctd = ctd.rename(columns={
                    'sea_surface_temperature': 'temperature',
                    'sea_surface_conductivity': 'conductivity'
                })
                # set the depth in dbar from the measured depth in m below the water line.
                if re.match('metbk1', ctd_name):
                    ctd['pressure'] = p_from_z(-1.3661, lat)
                elif re.match('metbk2', ctd_name):
                    ctd['pressure'] = p_from_z(-1.2328, lat)
                else:  # default of 1.00 m
                    ctd['pressure'] = p_from_z(-1.0000, lat)

            # calculate the practical salinity of the seawater from the temperature, conductivity and pressure
            # measurements
            ctd['psu'] = SP_from_C(ctd['conductivity'].values * 10.0, ctd['temperature'].values, ctd['pressure'].values)

            # interpolate temperature and salinity data from the CTD into the FLORT record for calculations
            degC = interp1d(ctd.time.values.astype('int64'), ctd.temperature.values, bounds_error=False)
            df['temperature'] = degC(df.time.values.astype('int64'))

            psu = interp1d(ctd.time.values.astype('int64'), ctd.psu, bounds_error=False)
            df['salinity'] = psu(df.time.values.astype('int64'))

            # Calculate the corrected nitrate concentration (uM) accounting for temperature and salinity and the pure
            # water calibration values.
            df['corrected_nitrate'] = ts_corrected_nitrate(dev.coeffs['cal_temp'], dev.coeffs['wl'], dev.coeffs['eno3'],
                                                           dev.coeffs['eswa'], dev.coeffs['di'], df['seawater_dark'],
                                                           df['temperature'], df['salinity'], channels,
                                                           df['measurement_type'], dev.coeffs['wllower'],
                                                           dev.coeffs['wlupper'])
        else:
            df['temperature'] = -9999.9
            df['salinity'] = -9999.9
            df['corrected_nitrate'] = -9999.9

    else:   # dataset does not include the full spectral array. Pad out with fill values to keep datasets consistent
        channels = np.ones([df.shape[0], 256]) * -999999999
        wavelengths = np.ones(256) * np.nan
        df['temperature'] = np.nan
        df['salinity'] = np.nan
        df['corrected_nitrate'] = np.nan

    # convert the dataframe to a format suitable for the pocean OMTs, adding the deployment name
    df['deploy_id'] = deployment
    df = df2omtdf(df, lat, lon, depth)

    # add to the global attributes for the NUTNR
    attrs = ISUS
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    })

    nc = OMTs.from_dataframe(df, outfile, attributes=attrs)
    nc.close()

    # re-open the netcdf file and add the raw channel measurements and the wavelengths with the additional dimension
    # of the measurement wavelengths.
    nc = Dataset(outfile, 'a')
    nc.createDimension('wavelengths', len(wavelengths))

    d = nc.createVariable('wavelengths', 'f', ('wavelengths',))
    d.setncatts(attrs['wavelengths'])
    d[:] = wavelengths

    d = nc.createVariable('channel_measurements', 'i', ('station', 't', 'wavelengths',))
    d.setncatts(attrs['channel_measurements'])
    d[:] = channels

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()


if __name__ == '__main__':
    main()
