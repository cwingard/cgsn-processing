#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_ifcb
@file cgsn_processing/process/proc_ifcb.py
@author Paul Whelan
@brief Creates a NetCDF dataset for IFCB from JSON formatted source data
"""
import os
import numpy as np
import pandas as pd
import xarray as xr

from datetime import datetime, timezone

from cgsn_processing.process.common import inputs, json2df, update_dataset, dict_update, ENCODING
from cgsn_processing.process.configs.attr_ifcb import HDR, ADC
from cgsn_processing.process.configs.attr_common import SHARED


def proc_ifcb(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main IFCB HDR and ADC file processing function. Loads the JSON formatted
    parsed data and converts the data into a NetCDF data file using xarray.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    **kwargs file_type: set the file type to HDR or ADC (default is HDR)

    :return df: An xarray dataset with the processed IFCB data
    """
    file_type = kwargs.get('file_type')
    if file_type and file_type.lower() in ['adc', 'hdr']:
        file_type = file_type.lower()
    else:
        raise ValueError('The IFCB file type must be a string set as either adc or hdr (case insensitive).')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    if file_type == 'adc':
        # Create time variable from file name timestamp + image offset as unixtime UTC
        fname = os.path.basename(infile)
        dtstring = fname[1: fname.find('_')-1]
        dt = datetime.strptime(dtstring, '%Y%m%dT%H%M%S')
        startfileUTC = dt.replace(tzinfo=timezone.utc).timestamp()
        df.insert(0, 'time', df['ADCtime'], True)
        df['time'] = pd.to_numeric(df['time']) + startfileUTC
        df.index = df['time']

        # Remove '#' from trigger column
        df = df.rename(columns={'trigger#': 'triggerNumber'})

        # set the attributes for the ADC data
        attrs = dict_update(ADC, SHARED)
    else:
        # set the attributes for the HDR data
        attrs = dict_update(HDR, SHARED)

    # create an xarray data set from the data frame
    df = xr.Dataset.from_dataframe(df)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    df['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(df.time)).astype(str))
    df = update_dataset(df, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    df.attrs['processing_level'] = 'parsed'
    return df


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
    file_type = args.switch

    # process the IFCB data and save the results to disk
    df = proc_ifcb(infile, platform, deployment, lat, lon, depth, file_type=file_type)
    if df:
        df.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
