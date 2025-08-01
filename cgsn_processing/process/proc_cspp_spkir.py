#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_spkir
@file cgsn_processing/process/proc_cspp_spkir.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP SPKIR data from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import re
import xarray as xr

from gsw import z_from_p

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_SPKIR
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.proc_spkir import Calibrations

from pyseas.data.opt_functions import opt_ocr507_irradiance


def proc_cspp_spkir(infile, platform, deployment, lat, lon, depth):
    """
    Main SPKIR processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the processing level attribute is set to "processed". Otherwise, filled
    variables are returned and the dataset processing level attribute is set
    to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed

    :return spkir: xarray dataset with the processed SPKIR data
    """
    # load the json data file as a dataframe for further processing
    data = json2df(infile)
    if data.empty:
        # json data file was empty, exiting
        return None

    # clean up dataframe and rename selected variables
    data.drop(columns=['suspect_timestamp'], inplace=True)  # not even the vendor knows what this is

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'spkir.cal_coeffs.json')
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it already exists
        dev.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        sampling_time = data['time'][0].value / 10.0 ** 9
        csv_url = find_calibration('SPKIR', str(data['serial_number'][0]), sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True

    # create the time coordinate array and set up a base data frame
    spkir_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(spkir_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # pop the raw_channels array out of the dataframe, will add them back in as individual, named variables
    channels = np.array(np.vstack(data.pop('raw_channels')), dtype='uint32')

    # set up and load the 1D parsed data into the data frame
    for v in data.columns:
        if v not in ['time']:
            df[v] = np.atleast_1d(data[v])

    # convert raw voltages and the instrument temperature to engineering units
    df['input_voltage'].apply(lambda x: x * 0.03)
    df['analog_rail_voltage'].apply(lambda x: x * 0.03)
    df['internal_temperature'].apply(lambda x: -50 + x * 0.5)

    # add the raw, downwelling spectral irradiance measurements to the dataframe per wavelength
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

    # rename the depth to ctd_pressure and then calculate the depth range for the NetCDF global attributes:
    # deployment depth and the profile min/max range
    df['ctd_pressure'] = df['depth']
    df['depth'] = -1 * z_from_p(df['ctd_pressure'], lat)
    depth_range = [depth, df['depth'].min(), df['depth'].max()]

    # convert the now 1D dataframe into an xarray data set
    spkir = xr.Dataset.from_dataframe(df)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    spkir['deploy_id'] = xr.Variable('time', np.tile(deployment, len(spkir.time)).astype(str))
    spkir['profile_id'] = xr.Variable('time', np.tile(profile_id, len(spkir.time)).astype(str))

    attrs = dict_update(CSPP_SPKIR, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    spkir = update_dataset(spkir, platform, deployment, lat, lon, depth_range, attrs)
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

    # process the SPKIR data and save the results to disk
    spkir = proc_cspp_spkir(infile, platform, deployment, lat, lon, depth)
    if spkir:
        spkir.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
