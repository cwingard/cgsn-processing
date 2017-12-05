#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import numpy as np
import pandas as pd
import pickle
import sys

from pathlib import Path

# Create a Global dictionary with Basic Information about the moorings
BUOYS = {
    'ce01issm': {'name': 'Coastal Endurance Oregon Inshore Surface Mooring'},
    'ce01issp': {'name': 'Coastal Endurance Oregon Inshore Surface Piercing Profiler'},
    'ce02shsm': {'name': 'Coastal Endurance Oregon Shelf Surface Mooring'},
    'ce04ossm': {'name': 'Coastal Endurance Oregon Offshore Surface Mooring'},
    'ce06issm': {'name': 'Coastal Endurance Washington Inshore Surface Mooring'},
    'ce06issp': {'name': 'Coastal Endurance Washington Inshore Surface Piercing Profiler'},
    'ce07shsm': {'name': 'Coastal Endurance Washington Shelf Surface Mooring'},
    'ce09ossm': {'name': 'Coastal Endurance Washington Offshore Surface Mooring'},
    'ce09ospm': {'name': 'Coastal Endurance Washington Offshore Profiler Mooring'}
}


class Coefficients(object):
    """
    A Coefficients class with two methods to load/save the serialized calibration coefficients for an instrument.
    """
    def __init__(self, coeff_file):
        """
        Initialize the object with the path to coefficients file
        """
        # set the infile name and path
        self.coeff_file = coeff_file
        self.coeffs = {}

    def load_coeffs(self):
        """
        Obtain the calibration data for this instrument from the serialized data object.
        """
        # load the pickled blanks dictionary
        with open(self.coeff_file, 'rb') as f:
            coeffs = pickle.load(f)

        self.coeffs = coeffs

    def save_coeffs(self):
        """
        Save the calibration data for this instrument as a serialized data object.
        """
        # save the pickled blanks dictionary
        with open(self.coeff_file, 'wb') as f:
            pickle.dump(self.coeffs, f)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """
    Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def hex2int(hstr):
    """
    Convert an error flag value represented as a hex string to an integer
    """
    return int(hstr, 16)


def json2df(infile):
    """
    Read in a JSON formatted data file and return the results as a panda dataframe.
    """
    jf = Path(infile)
    try:
        # test to see if the file exists
        jf.resolve()
    except FileNotFoundError:
        # if not, return an empty data frame
        print("JSON data file {0} was not found, returning empty data frame".format(infile))
        return pd.DataFrame()
    else:
        # otherwise, read in the data file
        with open(infile) as jf:
            df = pd.DataFrame(json.load(jf))

        # some of the data files are empty, exit early if so.
        if df.empty:
            print("JSON data file {0} was empty, returning empty data frame".format(infile))
            return df

        # setup time and the index
        df['time'] = pd.to_datetime(df.time, unit='s')
        df.index = df['time']

        # convert all long integers (int64) to ones acceptable for further processing
        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)

        return df


def json_sub2df(infile, sub):
    """
    Read in a JSON formatted data file, pull out the subarray and return the results as a panda dataframe.
    """
    with open(infile) as jf:
        data = json.load(jf)
        df = pd.DataFrame(data[sub])
        if df.empty:
            return df

        df['time'] = pd.to_datetime(df.time, unit='s')
        df.index = df['time']

        for col in df.columns:
            if df[col].dtype == np.int64:
                df[col] = df[col].astype(np.int32)

        return df


def df2omtdf(df, lat=0., lon=0., depth=0., time_var='time'):
    """
    Modifies a dataframe to be suitable for use with the from_dataframe
    method of pocean's OrthogonalMultidimensionalTimeseries
    """
    # rename time var to "t"
    df['t'] = df.pop(time_var)

    # fill lat/lon/depth values
    df['y'] = lat
    df['x'] = lon
    df['z'] = depth

    # just one station
    df['station'] = 0

    # convert all int64s to int32s
    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

    return df


def reset_long(df):
    """
    Resets all int64s (longs) in a dataframe to int32 (int). ERDDAP cannot handle longs.
    """
    # convert all int64s to int32s
    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

    return df


def split_column(df, colname, n=None, singular=None, names=None):
    """
    Convert col = [[a, b, c], [d, e, f]]
    into
    col1 = [a, d]
    col2 = [b, e]
    col3 = [c, f]
    """
    if names is None:
        if singular is None:
            singular = colname
        names = ['{}{}'.format(singular, i+1) for i in range(n)]
    else:
        n = len(names)
    for i, name in zip(range(n), names):
        df[name] = [v[i] for v in df[colname]]
    df.pop(colname)
    return df


def inputs(args=None):
    """
    Sets the main input arguments for the processor. At the least, the input and output files need to be specified,
    as well as the platform name, deployment name, latitude and longitude. Optionally, you can specify the sources of
    the factory calibration data (either a stored serialized object, or a link (either file path for factory provided
    data file(s) or a URL to OOI CI maintained CSV files). File names should always include path names. Finally a
    simple integer switch is provided for cases where the processor needs to function differently depending on some
    set of basic conditions.
    """
    if args is None:
        args = sys.argv[1:]
        
    # initialize argument parser
    parser = argparse.ArgumentParser(description="""Process data files, converting data from engineering units
                                                    to scientific units and saving as NetCDF""",
                                     epilog="""Process and convert data file to NetCDF""")

    # assign arguments for the infile and outfile and a generic switch that can
    # be used, if needed, to set different options (e.g. if switch == 1, do
    # this or that).
    parser.add_argument("-i", "--infile", dest="infile", type=str, required=True)
    parser.add_argument("-o", "--outfile", dest="outfile", type=str, required=True)
    parser.add_argument("-p", "--platform", dest="platform", type=str, required=True)
    parser.add_argument("-d", "--deployment", dest="deployment", type=str, required=True)
    parser.add_argument("-lt", "--latitude", dest="latitude", type=float, required=True)
    parser.add_argument("-lg", "--longitude", dest="longitude", type=float, required=True)
    parser.add_argument("-dp", "--depth", dest="depth", type=float, required=False)
    parser.add_argument("-bs", "--bin_size", dest="bin_size", type=float, required=False)
    parser.add_argument("-cf", "--coeff_file", dest="coeff_file", type=str, required=False)
    parser.add_argument("-sn", "--serial_number", dest="serial", type=str, required=False)
    parser.add_argument("-df", "--devfile", dest="devfile", type=str, required=False)
    parser.add_argument("-u", "--csvurl", dest="csvurl", type=str, required=False)
    parser.add_argument("-s", "--switch", dest="switch", type=int, default=0)

    # parse the input arguments and create a parser object
    return parser.parse_args(args)
