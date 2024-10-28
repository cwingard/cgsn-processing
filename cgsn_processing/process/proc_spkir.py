#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_spkir
@file cgsn_processing/process/proc_spkir.py
@author Joe Futrelle, Chris Wingard
@brief Creates a NetCDF dataset for SPKIR from JSON formatted source data
"""
import json
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import Coefficients, inputs, json2df, update_dataset, \
    ENCODING, dict_update
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_spkir import SPKIR
from cgsn_processing.process.configs.attr_common import SHARED

from pyseas.data.opt_functions import opt_ocr507_irradiance


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the SPKIR factory calibration coefficients for a unit. Values
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
        Reads the values from a SPKIR calibration file already parsed and
        stored on GitHub as a CSV files. Note, the formatting of those files
        puts some constraints on this process. If someone has a cleaner method,
        I'm all in favor... 
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # immersion, scale and offset correction factors
            if row.iloc[1] == 'CC_immersion_factor':
                coeffs['immersion_factor'] = np.array(json.loads(row.iloc[2]))
            if row.iloc[1] == 'CC_offset':
                coeffs['offset'] = np.array(json.loads(row.iloc[2]))
            if row.iloc[1] == 'CC_scale':
                coeffs['scale'] = np.array(json.loads(row.iloc[2]))

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_spkir(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main SPKIR processing function. Loads the JSON formatted, parsed data and
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

    **kwargs burst: Boolean flag to indicate whether to apply burst averaging
            to the data. Default is to not apply burst averaging.

    :return spkir: An xarray dataset with the processed spkir data
    """
    # process the variable length keyword arguments
    burst = kwargs.get('burst')

    # load the json data file as a dictionary object for further processing
    data = json2df(infile)
    if data.empty:
        # json data file was empty, exiting
        return None

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'spkir.cal_coeffs.json')
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
        csv_url = find_calibration('SPKIR', serial_number, sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True

    # clean up the dataframe, getting rid of variables we don't need
    data.drop(columns=['date_time_string'], inplace=True)

    # create the time coordinate array and set up a base data frame
    spkir_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(spkir_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # pop the raw_channels array out of the dataframe (will put it back in later)
    channels = np.array(np.vstack(data.pop('raw_channels')), dtype='uint32')

    # set up and load the 1D parsed data into the data frame
    for v in data.columns:
        if v not in ['time']:
            df[v] = np.atleast_1d(data[v])

    # convert raw voltages and the instrument temperature to engineering units
    df['input_voltage'].apply(lambda x: x * 0.03)
    df['analog_rail_voltage'].apply(lambda x: x * 0.03)
    df['internal_temperature'].apply(lambda x: -50 + x * 0.5)
    
    # add the raw downwelling spectral irradiance measurements to the dataframe per wavelength
    df['raw_irradiance_412'] = channels[:, 0]
    df['raw_irradiance_444'] = channels[:, 1]
    df['raw_irradiance_490'] = channels[:, 2]
    df['raw_irradiance_510'] = channels[:, 3]
    df['raw_irradiance_555'] = channels[:, 4]
    df['raw_irradiance_620'] = channels[:, 5]
    df['raw_irradiance_683'] = channels[:, 6]

    # Convert raw spectral irradiance values from count to uW cm-2 nm-1
    if proc_flag:
        ed = opt_ocr507_irradiance(channels, dev.coeffs['offset'], dev.coeffs['scale'], dev.coeffs['immersion_factor'])
    else:
        ed = channels.astype(float) * np.nan

    # add the converted downwelling spectral irradiance measurements to the dataframe per wavelength
    df['downwelling_irradiance_412'] = ed[:, 0]
    df['downwelling_irradiance_444'] = ed[:, 1]
    df['downwelling_irradiance_490'] = ed[:, 2]
    df['downwelling_irradiance_510'] = ed[:, 3]
    df['downwelling_irradiance_555'] = ed[:, 4]
    df['downwelling_irradiance_620'] = ed[:, 5]
    df['downwelling_irradiance_683'] = ed[:, 6]

    # convert the now 1D dataframe into an xarray data set
    spkir = xr.Dataset.from_dataframe(df)

    # apply a median average to the burst (if desired)
    if burst:
        # resample to a 15-minute interval and shift the clock to center the averaging window
        spkir['time'] = spkir.time + pd.Timedelta('450s')
        spkir = spkir.resample(time='900s').median(dim='time', keep_attrs=True)

        # resampling will fill in missing time steps with NaNs. Use the serial_number variable
        # as a proxy variable to find cases where data is filled with a NaN, and delete those records.
        spkir = spkir.where(~np.isnan(spkir.serial_number), drop=True)

        # reset original integer values
        int_arrays = ['frame_counter', 'sample_delay', 'serial_number']
        for var in spkir.variables:
            if var in int_arrays:
                spkir[var] = spkir[var].astype(int)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    spkir['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(spkir.time)).astype(str))
    attrs = dict_update(SPKIR, SHARED)
    spkir = update_dataset(spkir, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    if proc_flag:
        spkir.attrs['processing_level'] = 'processed'
    else:
        spkir.attrs['processing_level'] = 'parsed'

    return spkir


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
    burst = args.burst

    # process the SPKIR data and save the results to disk
    spkir = proc_spkir(infile, platform, deployment, lat, lon, depth, burst=burst)
    if spkir:
        spkir.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
