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

from cgsn_processing.process.common import inputs

env = Environment(loader=FileSystemLoader('templates'))

"""
ERDDAP Valid values are:
    double (64-bit floating point),
    float (32-bit floating point),
    long (64-bit signed integer),
    int (32-bit signed integer),
    short (16-bit signed integer),
    byte (8-bit signed integer),
    char (essentially: 16-bit unsigned integer),
    boolean, and
    String (any length).
"""
# create a dictionary mapping and the valid values and their meanings
dmap = {
    'float64': 'double',
    'float32': 'float',
    'int64': 'long',
    'int32': 'int',
    'int16': 'short',
    'b': 'byte',
    'uint16': 'char',
    'bool': 'boolean',
    'S1': 'String',
    'bytes8': 'String',
    'string': 'String',
    'string8': 'String'
    }


def dvar_info(nc, dmap=None):
    # Assign sourceName:[destinationName, ioos_category, dataType, colorBarMinimum, colorBarMaximum]
    dvars = {}
    for var in list(nc.variables):
        print var
        # default is ioos_category "Unknown".  Don't calculate limits yet.
        erddap_type = dmap[np.dtype(nc[var]).name]
        dvars[var] = {
            'destinationName': var,
            'ioos_category': 'Unknown',
            'dataType': erddap_type,
            'colorBarMinimum': None,
            'colorBarMaximum': None
            }
        # calculate limits for all vars that are not strings
        if erddap_type is not 'String':
            dvars[var]['colorBarMinimum'] = nc[var][:].min()
            dvars[var]['colorBarMaximum'] = nc[var][:].max()
        if np.ma.is_masked(dvars[var]['colorBarMaximum']):
            dvars[var]['colorBarMaximum'] = None
        if np.ma.is_masked(dvars[var]['colorBarMinimum']):
            dvars[var]['colorBarMinimum'] = None

    # set destinationName, ioos_category, datatype and limits for coordinate variables
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
        'destinationName': 'altitude',
        'ioos_category': 'Location',
        'dataType': dmap[zvar.dtype.name],
        'colorBarMinimum': -8000.0,
        'colorBarMaximum': 8000.0,
        'units': 'm'
        }
    return dvars


def main():
    # load the input arguments
    args = inputs()
    inpath, infile = os.path.abspath(args.infile)
    outfile = os.path.abspath(args.outfile)
    datasetID = args.deployment

    # open a NetCDF CF-1.6+, DSG featureType=timeSeries file
    nc = netCDF4.Dataset(infile)
    cdm_timeseries_variables = 'latitude, longitude, altitude, feature_type_instance'
    keywords = ','.join(list(nc.variables))
    dvars = dvar_info(nc, dmap=dmap)
    if 'timeSeries' in nc.featureType:
        template = env.get_template('timeSeries.xml')
        ds_xml = template.render(datasetID=datasetID,
                                 reloadEveryNMinutes='30',
                                 fileDir=inpath,
                                 fileNameRegex='.*\.nc',
                                 subsetVariables=cdm_timeseries_variables,
                                 infoUrl='http://oceanobservatories.org',
                                 cdm_timeseries_variables=cdm_timeseries_variables,
                                 keywords=keywords,
                                 dvars=dvars)

        with open(outfile, "w") as f:
            f.write("{}".format(ds_xml))


if __name__ == '__main__':
    main()
