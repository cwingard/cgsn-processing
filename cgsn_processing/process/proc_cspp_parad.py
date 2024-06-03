#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cspp_parad
@file cgsn_processing/process/proc_cspp_parad.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the uCSPP PARAD data from JSON formatted source data
"""
import numpy as np
import os
import re
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_cspp import CSPP, CSPP_PARAD
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.finding_calibrations import find_calibration
from pyseas.data.opt_functions import opt_par_satlantic


class Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the PARAD factory calibration coefficients for a unit. Values come from either a serialized object
        created per instrument and deployment (calibration coefficients do not change in the middle of a deployment),
        or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from an Satlantic PAR sensor (aka PARAD) device file already parsed and stored on
        GitHub as a CSV files. Note, the formatting of these files puts some constraints on this process.
        If someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # immersion, scale and offset correction factors
            if row[1] == 'CC_a0':
                coeffs['a0'] = row[2]
            if row[1] == 'CC_a1':
                coeffs['a1'] = row[2]
            if row[1] == 'CC_Im':
                coeffs['Im'] = row[2]

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_cspp_dosta(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main DOSTA processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If calibration coefficients are available,
    the oxygen concentration is recalculated from the calibrated phase and
    thermistor temperature and the dataset processing level attribute is set
    to "processed". Otherwise, filled variables are returned and the dataset
    processing level attribute is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Site name where the CSPP is deployed
    :param deployment: name of the deployment for the input data file.
    :param lat: latitude of the CSPP deployment.
    :param lon: longitude of the CSPP deployment.
    :param depth: site depth where the CSPP is deployed
    **par_serial: Serial number of the PARAD sensor

    :return parad: xarray dataset with the processed DOSTA data
    """
    # process the variable length keyword arguments
    serial_number = kwargs.get('par_serial')

    # load the json data file as a dataframe for further processing
    data = json2df(infile)
    if data.empty:
        # json data file was empty, exiting
        return None

    # remove the PARAD date/time string from the dataset
    _ = data.pop('parad_date_time_string')

    # set up the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'parad.cal_coeffs.json')
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
        csv_url = find_calibration('PARAD', serial_number, sampling_time)
        if csv_url:
            dev.read_csv(csv_url)
            dev.save_coeffs()
            proc_flag = True
        else:
            print('A source for the PARAD calibration coefficients for {} could not be found'.format(infile))

    if proc_flag:
        # Apply the scale, offset and immersion correction factors from the factory calibration coefficients
        df['irradiance'] = opt_par_satlantic(df['raw_par'], dev.coeffs['a0'], dev.coeffs['a1'], dev.coeffs['Im'])
    else:
        # set the irradiance to NaN's since we don't have calibration coefficients
        df['irradiance'] = df['raw_par'].astype(float) * np.nan

    # create an xarray data set from the data frame
    parad = xr.Dataset.from_dataframe(parad)

    # pull out the profile ID from the filename
    _, fname = os.path.split(infile)
    profile_id = re.sub(r'\D+', '', fname)
    profile_id = "{}.{}.{}".format(profile_id[0], profile_id[1:4], profile_id[4:])

    # add the deployment and profile IDs to the dataset
    parad['deploy_id'] = xr.Variable('time', np.tile(deployment, len(parad.time)).astype(str))
    parad['profile_id'] = xr.Variable('time', np.tile(profile_id, len(parad.time)).astype(str))

    attrs = dict_update(CSPP_PARAD, CSPP)  # add the shared CSPP attributes
    attrs = dict_update(attrs, SHARED)  # add the shared common attributes
    parad = update_dataset(parad, platform, deployment, lat, lon, depth_range, attrs)
    if proc_flag:
        parad.attrs['processing_level'] = 'processed'
    else:
        parad.attrs['processing_level'] = 'partial'

    return parad


def main(argv=None):
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
        serial = args.serial  # serial number of the PARAD sensor

        # process the DOSTA data and save the results to disk
        parad = proc_cspp_dosta(infile, platform, deployment, lat, lon, depth, par_serial=serial)
        if parad:
            parad.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
