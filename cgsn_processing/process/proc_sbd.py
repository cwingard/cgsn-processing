#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_sbd
@file cgsn_processing/process/proc_sbd.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the CPM or STC supervisor logs sent
    via Iridium SBD messaging from the JSON formatted source data
"""
import numpy as np
import os
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update
from cgsn_processing.process.configs.attr_sbd import CPM, STC
from cgsn_processing.process.configs.attr_common import SHARED


def proc_sbd(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main processing function for supervisor logs sent via the Iridium
    SBD messaging system. Loads the JSON formatted parsed data and
    creates a NetCDF file for use in monitoring the system health.
    Dataset processing level attribute is set to "parsed"; there is
    no processing of the data, just a straight conversion from JSON
    to NetCDF.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwargs superv_type: Specify the source of the supervisor log file, either
        a CPM or STC.

    :return sbd: An xarray dataset with the processed supervisor data
    """
    # get the supervisor type and force the string to lowercase if supplied
    superv_type = kwargs.get('superv_type')
    if superv_type and superv_type.lower() in ['cpm', 'stc']:
        superv_type = superv_type.lower()
    else:
        raise ValueError('The supervisor type must be a string set as either cpm or stc (case insensitive).')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # drop the email date/time string and transfer status string variables
    df.drop(columns=['date_time_email', 'transfer_status'], inplace=True)

    # convert the different hex strings (already converted to an integer in the parser) to unsigned integers
    for col in df.columns:
        if col in ['wake_code', 'ground_fault_enable', 'error_flags', 'error_flags1', 'error_flags2']:
            df[col] = df[col].astype(np.uintc)

    # create an xarray data set from the data frame
    sbd = xr.Dataset.from_dataframe(df)

    # clean up the dataset and assign attributes
    sbd['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(sbd.time)).astype(str))
    if superv_type == 'cpm':
        attrs = dict_update(CPM, SHARED)
    else:
        attrs = dict_update(STC, SHARED)
    sbd = update_dataset(sbd, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    sbd.attrs['processing_level'] = 'parsed'

    return sbd


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
    superv_type = args.switch

    # process the supervisor data and save the results to disk
    sbd = proc_sbd(infile, platform, deployment, lat, lon, depth, superv_type=superv_type)
    if sbd:
        sbd.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
