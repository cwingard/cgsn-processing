#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.generate_dataset
@file cgsn_processing/process/generate_dataset.py
@author Christopher Wingard
@brief Create an ERDDAP dataset snippet by reading a NetCDF CF-1.6 DSG featureType=TimeSeries file
"""
import numpy as np
import netCDF4
import os

from jinja2 import Environment, FileSystemLoader
from cgsn_processing.process.common import InputError, inputs

templates = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), 'templates')
ENV = Environment(loader=FileSystemLoader(templates), trim_blocks=True)

# create a dictionary mapping the netCDF data types to valid ERDDAP types, where the valid types are:
#     double (64-bit floating point),
#     float (32-bit floating point),
#     long (64-bit signed integer),
#     int (32-bit signed integer),
#     short (16-bit signed integer),
#     byte (8-bit signed integer),
#     char (essentially 16-bit unsigned integer),
#     boolean, and
#     String (any length).
DMAP = {
    'float64': 'double',
    'float32': 'float',
    'int64': 'long',
    'int32': 'int',
    'int16': 'short',
    'b': 'byte',
    'uint16': 'char',
    'bool': 'boolean',
    'bytes8': 'String',
    'S1': 'String',
    'string': 'String',
    'string8': 'String'
    }


def variable_info(nc, dmap=None):
    """
    Assign the sourceName, destinationName, ioos_category, dataType, colorBarMinimum and colorBarMaximum to the
    <dataVariable> tag in the dataset.xml based on attributes in the NetCDF4 file for each variable.
    """
    dvars = {}
    for var in list(nc.variables):
        # begin by setting the defaults for all variables.
        erddap_type = dmap[nc[var].datatype.name]
        # let's see if we set the ioos_category
        try:
            ioos = nc[var].ioos_category
        except AttributeError:
            ioos = 'Unknown'
        # now set the values
        dvars[var] = {
            'destinationName': var,
            'ioos_category': ioos,
            'dataType': erddap_type,
            'colorBarMinimum': None,
            'colorBarMaximum': None
            }
        # calculate the colorBar limits
        if erddap_type is not 'String':
            dvars[var]['colorBarMinimum'] = nc[var][:].min()
            dvars[var]['colorBarMaximum'] = nc[var][:].max()
        if np.ma.is_masked(dvars[var]['colorBarMaximum']):
            dvars[var]['colorBarMaximum'] = None
        if np.ma.is_masked(dvars[var]['colorBarMinimum']):
            dvars[var]['colorBarMinimum'] = None

    # reset the destinationName, ioos_category, dataType and colorBar limits for the coordinate variables
    tvar = nc.get_variables_by_attributes(standard_name='time')[0]
    dvars[tvar.name] = {
        'destinationName': 'time',
        'ioos_category': 'Time',
        'dataType': dmap[tvar.dtype.name],
        'colorBarMinimum': None,
        'colorBarMaximum': None
        }

    xvar = nc.get_variables_by_attributes(standard_name='longitude')[0]
    dvars[xvar.name] = {
        'destinationName': 'longitude',
        'ioos_category': 'Location',
        'dataType': dmap[xvar.dtype.name],
        'colorBarMinimum': -180.0,
        'colorBarMaximum': 180.0
        }

    yvar = nc.get_variables_by_attributes(standard_name='latitude')[0]
    dvars[yvar.name] = {
        'destinationName': 'latitude',
        'ioos_category': 'Location',
        'dataType': dmap[yvar.dtype.name],
        'colorBarMinimum': -90.0,
        'colorBarMaximum': 90.0
        }

    zvar = nc.get_variables_by_attributes(axis='Z')[0]
    dvars[zvar.name] = {
        'destinationName': 'depth',
        'ioos_category': 'Location',
        'dataType': dmap[zvar.dtype.name],
        'colorBarMinimum': -30.0,
        'colorBarMaximum': 10000.0,
        'units': 'm'
        }
    return dvars


def main(argv=None):
    """
    Load a NetCDF file to use as a template for creating the dataset.xml file, set the dataset ID and create the
    dataset based on the timeSeries.xml template.
    """
    # load the input arguments, pulling in the paths and file names of the input and output files as well as the
    # dataset ID.
    args = inputs(argv)
    inpath, infile = os.path.split(os.path.abspath(args.infile))
    outfile = os.path.abspath(args.outfile)
    datasetID = args.deployment

    # open a NetCDF CF-1.6+, DSG featureType=timeSeries file
    nc = netCDF4.Dataset(os.path.join(inpath, infile))
    cdm_timeseries_variables = 'latitude, longitude, crs, platform'
    keywords = ','.join(list(nc.variables))
    dvars = variable_info(nc, dmap=DMAP)
    if 'timeSeries' in nc.featureType:
        template = ENV.get_template('timeSeries.xml')
        ds_xml = template.render(datasetID=datasetID,
                                 datasetTitle="{}".format(nc.title),
                                 summaryInfo="{}".format(nc.summary),
                                 reloadEveryNMinutes='30',
                                 fileDir="{}/".format(inpath),
                                 fileNameRegex='.*\.nc',
                                 subsetVariables=cdm_timeseries_variables,
                                 cdm_timeseries_variables=cdm_timeseries_variables,
                                 keywords=keywords,
                                 dvars=dvars)
    else:
        raise InputError('featureType', 'NetCDF source file is not a timeSeries featureType')

    # save the dataset
    with open(outfile, "w") as f:
        f.write("{}".format(ds_xml))


if __name__ == '__main__':
    main()
