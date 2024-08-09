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

from gsw import SP_from_C, SA_from_SP, CT_from_t, rho, z_from_p

from cgsn_processing.process.common import ENCODING, inputs, epoch_time, json2df, update_dataset, dict_update
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_ctdbp import CTDBP
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.proc_flort import Calibrations

from pyseas.data.do2_functions import do2_salinity_correction
from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total


def proc_ctdbp(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the different versions of CTDBP. Loads the JSON
    formatted parsed data and applies appropriate calibration coefficients to
    convert the raw parsed data into engineering units. If no calibration
    coefficients are available, filled variables are returned and the dataset
    processing level attribute is set to "parsed". If the calibration,
    coefficients are available then the dataset processing level attribute is
    set to "processed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwarg ctd_type: Set the type of CTD: solo, with a dosta, or with a flort attached
    :kwarg flr_serial: The serial number of the attached FLORT (optional input)

    :return ctdbp: An xarray dataset with the processed CTDBP data
    """
    # process the variable length keyword arguments
    ctd_type = kwargs.get('ctd_type')
    if ctd_type:
        ctd_type = ctd_type.lower()
    flr_serial = kwargs.get('flr_serial')

    if ctd_type not in ['solo', 'dosta', 'flort']:
        raise ValueError('The CTDBP type must be a string set as either solo, dosta or flort (case insensitive).')

    # load the json data file as a panda data frame for further processing
    ctd = json2df(infile)
    if ctd.empty:
        # json data file was empty, exiting
        return None

    # clean up variables and setting the processing flag
    ctd['sensor_time'] = epoch_time(ctd['ctd_date_time_string'].values[0])
    ctd.drop(columns=['ctd_date_time_string', 'dcl_date_time_string'], inplace=True)
    proc_flag = False

    # reset the depth array using the deployment depth and the min and max from the pressure record
    d = z_from_p(ctd['pressure'], lat)
    depth = [depth, d.min(), d.max()]

    # calculate the practical salinity of the seawater from the temperature and conductivity measurements
    ctd['salinity'] = SP_from_C(ctd['conductivity'].values * 10.0, ctd['temperature'].values, ctd['pressure'].values)

    # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
    sa = SA_from_SP(ctd['salinity'].values, ctd['pressure'].values, lon, lat)  # absolute salinity
    ct = CT_from_t(sa, ctd['temperature'].values, ctd['pressure'].values)      # conservative temperature
    ctd['density'] = rho(sa, ct, ctd['pressure'].values)                       # density

    if ctd_type in ['solo', 'dosta']:
        # set the processing flag
        proc_flag = True

        # apply temperature, salinity and pressure corrections to dissolved oxygen measurement
        if ctd_type == 'dosta':
            ctd['oxygen_concentration_corrected'] = do2_salinity_correction(ctd['oxygen_concentration'].values,
                                                                            ctd['pressure'].values,
                                                                            ctd['temperature'].values,
                                                                            ctd['salinity'].values, lat, lon)

    if ctd_type == 'flort':
        # create empty variables for the processed FLORT data
        ctd['estimated_chlorophyll'] = ctd['raw_chlorophyll'] * np.nan
        ctd['fluorometric_cdom'] = ctd['raw_cdom'] * np.nan
        ctd['beta_700'] = ctd['raw_backscatter'] * np.nan
        ctd['total_optical_backscatter'] = ctd['beta_700'] * np.nan

        # now grab the calibration coefficients for the FLORT (if they exist)
        coeff_file = os.path.join(os.path.dirname(infile), 'flort.cal_coeffs.json')
        flr = Calibrations(coeff_file)  # initialize calibration class
        if os.path.isfile(coeff_file):
            # we always want to use this file if it exists
            flr.load_coeffs()
            proc_flag = True
        else:
            # load from the CI hosted CSV files
            csv_url = find_calibration('FLORT', flr_serial, (ctd.time.values.astype('int64') * 10 ** -9)[0])
            if csv_url:
                flr.read_csv(csv_url)
                flr.save_coeffs()
                proc_flag = True

        # if calibration coefficients are available, process the FLORT data
        if proc_flag:
            ctd['estimated_chlorophyll'] = flo_scale_and_offset(ctd['raw_chlorophyll'], flr.coeffs['dark_chla'],
                                                                flr.coeffs['scale_chla'])
            ctd['fluorometric_cdom'] = flo_scale_and_offset(ctd['raw_cdom'], flr.coeffs['dark_cdom'],
                                                            flr.coeffs['scale_cdom'])
            ctd['beta_700'] = flo_scale_and_offset(ctd['raw_backscatter'], flr.coeffs['dark_beta'],
                                                   flr.coeffs['scale_beta'])
            ctd['total_optical_backscatter'] = flo_bback_total(ctd['beta_700'], ctd['temperature'], ctd['salinity'],
                                                               flr.coeffs['scatter_angle'], flr.coeffs['wavelength'],
                                                               flr.coeffs['chi_factor'])

    # create an xarray data set from the data frame
    ctd = xr.Dataset.from_dataframe(ctd)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    ctd['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(ctd.time)).astype(str))
    attrs = dict_update(CTDBP, SHARED)  # add the shared the attributes
    ctd = update_dataset(ctd, platform, deployment, lat, lon, depth, attrs)
    if proc_flag:
        ctd.attrs['processing_level'] = 'processed'
    else:
        ctd.attrs['processing_level'] = 'partial'

    return ctd


def main(argv=None):
    """
    Command line function to process the CTDBP data using the proc_ctdbp
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
    ctd_type = args.switch
    flr_serial = args.serial  # serial number of the FLORT

    # process the CTDBP data and save the results to disk
    ctdbp = proc_ctdbp(infile, platform, deployment, lat, lon, depth, ctd_type=ctd_type, flr_serial=flr_serial)
    if ctdbp:
        ctdbp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
