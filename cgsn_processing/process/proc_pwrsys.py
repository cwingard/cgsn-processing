#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_psc
@file cgsn_processing/process/proc_pwrsys.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the power system controller data from JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_mpea import MPEA
from cgsn_processing.process.configs.attr_psc import PSC
from cgsn_processing.process.configs.attr_common import SHARED


def proc_pwrsys(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Mooring power system controller (either the PSC or MPEA) processing
    function. Loads the JSON formatted parsed data and converts data into a
    NetCDF data file using xarray. Dataset processing level attribute is set
    to "parsed". There is no processing of the data, just a straight
    conversion from JSON to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    **kwargs pwrsys_type: Name of the power system type, either psc or mpea.

    :return psc: An xarray dataset with the mooring power system data
    """
    # process the variable length keyword arguments
    pwrsys_type = kwargs.get('pwrsys_type')
    if pwrsys_type and pwrsys_type.lower() in ['psc', 'mpea']:
        pwrsys_type = pwrsys_type.lower()
    else:
        IOError('You need to specify the power system type, either psc or mpea, before the data can be processed)')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the date and time string variable.
    df.drop_vars(columns=['dcl_date_time_string'], inplace=True)

    # create dummy attrs variable
    attrs = None

    if pwrsys_type == 'psc':
        # we don't have a fuel cell, we've never had one, and we never will. time to stop pretending, bye-bye fuel cell
        fuel_cell = ['fuel_cell1_state', 'fuel_cell1_voltage', 'fuel_cell1_current',
                     'fuel_cell2_state', 'fuel_cell2_voltage', 'fuel_cell2_current',
                     'fuel_cell_volume']
        df.drop_vars(columns=fuel_cell, inplace=True)

        # set up the attributes dictionary
        attrs = dict_update(PSC, SHARED)

    if pwrsys_type == 'mpea':
        # While originally intended to provide power for AUV docks, that functionality of the CVT was never fully
        # developed or used. There are multiple channels for which we have no data, and at this time never will.
        # Dropping them to make a cleaner data set.
        cv_channels = ['cv3_state', 'cv3_voltage', 'cv3_current',
                       'cv4_state', 'cv4_voltage', 'cv4_current',
                       'cv5_state', 'cv5_voltage', 'cv5_current',
                       'cv6_state', 'cv6_voltage', 'cv6_current',
                       'cv7_state', 'cv7_voltage', 'cv7_current']
        df.drop_vars(columns=cv_channels, inplace=True)

        # set up the attributes dictionary
        attrs = dict_update(MPEA, SHARED)

    # convert the different hex strings (already converted to an integer in the parser) used for flags
    # to unsigned integers
    for col in df.columns:
        if col in ['error_flag1', 'error_flag2', 'error_flag3', 'override_flag']:
            df[col] = df[col].astype(np.uintc)

    # create an xarray data set from the data frame
    pwrsys = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    pwrsys['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(pwrsys.time)).astype(str))
    pwrsys = update_dataset(pwrsys, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    pwrsys.attrs['processing_level'] = 'parsed'

    return pwrsys


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
    pwrsys_type = args.switch  # name of power system type, either psc or mpea

    # process the mooring power system data and save the results to disk
    pwrsys = proc_pwrsys(infile, platform, deployment, lat, lon, depth, pwrsys_type=pwrsys_type)
    if pwrsys:
        pwrsys.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
