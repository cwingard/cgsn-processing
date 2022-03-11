#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import collections
import datetime
import glob
import json
import numpy as np
import os
import pandas as pd
import re
import sys

from dateutil import rrule
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

# Create a dictionary to correct some inconsistencies between an xarray dataset and a CF compliant NetCDF file
ENCODING = {
    'time': {'_FillValue': None},
    'lat': {'_FillValue': None},
    'lon': {'_FillValue': None},
    'z': {'_FillValue': None},
    'station': {'dtype': str},
    'deploy_id': {'dtype': str}
}

# Create global default fill values
FILL_INT = -9999999
FILL_NAN = np.nan


class NumpyEncoder(json.JSONEncoder):
    """
    Special json encoder for numpy types, where we have nested numpy arrays in a dictionary.
    Allows saving the data to a json file. Used by the Coefficients class to save instrument
    calibration coefficients to disk

    From our trusty friends at StackOverflow: https://stackoverflow.com/a/49677241
    """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32,
                            np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Coefficients(object):
    """
    A Coefficients class with two methods to load/save the serialized calibration coefficients for an instrument.
    """
    def __init__(self, coeff_file):
        """
        Initialize the class with the path to coefficients file and an empty dictionary structure for
        the calibration data
        """
        # set the infile name and path
        self.coeff_file = coeff_file
        self.coeffs = {}

    def load_coeffs(self):
        """
        Obtain the calibration data for this instrument from a JSON data file.
        """
        with open(self.coeff_file, 'r') as f:
            coeffs = json.load(f)

        # JSON loads arrays as lists. We need to convert those to arrays for our work
        for c in coeffs:
            if isinstance(coeffs[c], list):
                coeffs[c] = np.asarray(coeffs[c])

        self.coeffs = coeffs

    def save_coeffs(self):
        """
        Save the calibration data for this instrument to a JSON data file.
        """
        with open(self.coeff_file, 'w') as f:
            jdata = json.dumps(self.coeffs, cls=NumpyEncoder)
            f.write(jdata)


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


def join_df(df1, df2):
    """
    Join two data frames, padding missing values with the appropriate fill value. Recasting data types in the joined
    data frames back to their original settings from prior to the join.

    :param df1: primary dataframe to merge the secondary dataframe into
    :param df2: secondary dataframe
    :return joined: combined primary and secondary dataframes
    """
    # capture the data types in the original data frames
    orig = df1.dtypes.to_dict()
    orig.update(df2.dtypes.to_dict())

    # join the data frames
    joined = df1.join(df2, how='outer')

    # data types are converted to a float in the above operation, need to convert integers and strings back to their
    # original data types and reset the fill values to appropriate values instead of NaN.
    for col in joined:
        if orig[col] == 'int32':
            joined[col].fillna(-9999999, inplace=True)
            joined[col] = joined[col].astype(orig[col])

        if orig[col] == 'object':
            joined[col].fillna('unknown', inplace=True)
            joined[col] = joined[col].astype('|S')

    return joined


def json2obj(infile):
    """
    Read in a JSON formatted data file and return the results as a json formatted data object.
    """
    jf = Path(infile)
    try:
        # test to see if the file exists
        jf.resolve()
    except FileNotFoundError:
        # if not, return an empty data frame
        print("JSON data file {0} was not found, returning empty data frame".format(infile))
        return None
    else:
        # otherwise, read in the data file
        with open(infile) as jf:
            data = json.load(jf)

        return data


def json2df(infile):
    """
    Read in a JSON formatted data file and return the results as a panda dataframe.
    """
    jf = Path(infile)
    if not jf.is_file():
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


def json_obj2df(data, sub):
    """
    Take a JSON formatted data object, read it in as a dict, pull out the subarray of interest, and return the results
    as a panda data frame.
    """
    df = pd.DataFrame(data[sub])
    if df.empty:
        return df

    # Depending on the json data, time may or may not be present in the subarray. In those cases, it will be at the
    # root level of the json data.
    if 'time' in df.keys():
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', drop=True, inplace=True)
    else:
        df['time'] = pd.to_datetime(data['time'], unit='s')
        df.set_index('time', drop=True, inplace=True)

    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

    return df


def colocated_ctd(infile, ctd_name):
    """
    Using the instrument name and datetime information from the instrument file name, find the co-located CTD data
    to use in further processing steps.

    :param infile: instrument file name with the full, absolute path
    :param ctd_name: name of the CTD file to match to the instrument file name
    :return ctd: CTD data covering the time period of interest for input file, will be an empty data frame
                 if no co-located CTD data can be found.
    """
    # create an empty ctd dataframe for use below
    ctd = pd.DataFrame()

    # using the source instrument's full path information, split out the path and file name.
    instrmt_path, instrmt_file = os.path.split(infile)
    instrmt_name = os.path.basename(instrmt_path)
    ctd_path = re.sub(instrmt_name, ctd_name, instrmt_path)

    # data files are named with either a date stamp, or a date+time stamp followed by the instrument name.
    x = re.match(r'([\d]{8}|[\d]{8}_[\d]{6}).([\w]*).json', instrmt_file)
    if x:   # extract the date from the file name
        if len(x.group(1)) == 8:
            instrmt_date = datetime.datetime.strptime(x.group(1), '%Y%m%d')
        else:
            instrmt_date = datetime.datetime.strptime(x.group(1), '%Y%m%d_%H%M%S')
    else:
        # cannot determine date of the instrument file, exit the function
        return ctd

    # given the date, find our co-located ctd data files
    tdelta = datetime.timedelta(days=1)
    for dt in rrule.rrule(rrule.DAILY, dtstart=instrmt_date - tdelta, until=instrmt_date + tdelta):
        dt_str = dt.strftime('%Y%m%d')
        ctd_file = f'{dt_str}.*.json'
        co_located = glob.glob((ctd_path + '/' + ctd_file))
        if co_located:
            df = json2df(os.path.abspath(co_located[0]))
            if not df.empty:
                ctd = pd.concat((ctd, df), sort=False)

    return ctd


def update_dataset(ds, platform, deployment, lat, lon, depth, attrs):
    """
    Updates a data set with global and variable level metadata attributes and
    sets appropriate dimensions and coordinate axes based on the CF Metadata
    Standard, version 1.7, for a single time series at a nominal fixed spatial
    location.

    :param ds: Data set to update
    :param platform: Platform name
    :param deployment: Deployment name
    :param lat: Deployment latitude in decimal degrees North
    :param lon: Deployment longitude in decimal degrees East
    :param depth: Array indicating the deployment depth, and the vertical
        minimum and maximum extent of the depth range for the instrument in
        this data set
    :param attrs: Global and variable level attributes for the data set
    :return ds: The updated data set
    """
    # convert the depth array to named variables
    deploy_depth = depth[0]     # instrument deployment depth
    min_depth = depth[1]        # minimum vertical extent of the instrument depth
    max_depth = depth[2]        # maximum vertical extent of the instrument depth
    # note, the minimum and maximum depths will vary if the instrument includes a
    # pressure sensor, otherwise they will be set to the deployment depth

    # add the non-dimensional coordinate variables
    ds = ds.assign_coords({
        'lat': lat,
        'lon': lon,
        'z': deploy_depth,
        'station': platform.upper()
    })

    # Convert time from nanoseconds to seconds since 1970
    ds['time'] = dt64_epoch(ds.time)

    # update the global attributes with deployment specific details
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment)),
        'date_created': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00Z"),
        'geospatial_lat_max': lat,
        'geospatial_lat_min': lat,
        'geospatial_lon_max': lon,
        'geospatial_lon_min': lon,
        'geospatial_vertical_max': max_depth,
        'geospatial_vertical_min': min_depth,
        'geospatial_vertical_positive': 'down',
        'geospatial_vertical_units': 'm'
    })

    # assign the updated attributes to the global metadata and the individual variables
    ds.attrs = attrs['global']
    for v in ds.variables:
        if v not in ['time', 'lat', 'lon', 'z', 'station', 'wavelength_number']:
            ds[v].attrs = dict_update(attrs[v], {'coordinates': 'time lat lon z station'})
        else:
            ds[v].attrs = attrs[v]

    # reset all integers set as long, or int64, as an int32. ERDDAP doesn't like longs
    for v in ds.variables:
        if ds[v].dtype == np.int64:
            ds[v] = ds[v].astype(np.int32)

    # return the data set for further work
    return ds


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


def dict_update(source, overrides):
    """
    Update a nested dictionary or similar mapping. Modifies ``source`` in place.

    From https://stackoverflow.com/a/30655448. Replaces original dict_update used by poceans-core, also pulled from
    the same thread.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = dict_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


def dt64_epoch(dt64):
    """
    Convert a panda or xarray date/time value represented as a datetime64 object (nanoseconds since 1970) to a float,
    representing an epoch time stamp (seconds since 1970-01-01).

    :param dt64: panda or xarray datatime64 object
    :return epts: epoch time as seconds since 1970-01-01
    """
    epts = dt64.values.astype(float) / 10.0 ** 9
    return epts


def epoch_time(time_string):
    """
    Convert a date/time string into a Unix epoch time stamp (seconds since 1970-01-01)

    :param time_string: Input date/time string in ISO-8601 format.
    :return epts: The date/time string value converted into a Unix epoch time stamp
    """
    # convert the date and time string into a pandas datetime64 object
    dt = pd.Timestamp(time_string)

    # calculate the epoch time as seconds since 1970-01-01 in UTC
    epts = dt.value / 10.0 ** 9
    return epts


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
    parser.add_argument("-dp", "--depth", dest="depth", type=float, required=True)
    parser.add_argument("-ba", "--burst_average", dest="burst", default=False, action='store_true')
    parser.add_argument("-bs", "--bin_size", dest="bin_size", type=float, required=False)
    parser.add_argument("-bd", "--blanking_distance", dest="blanking_distance", type=float, required=False)
    parser.add_argument("-cf", "--coeff_file", dest="coeff_file", type=str, required=False)
    parser.add_argument("-sn", "--serial_number", dest="serial", type=str, required=False)
    parser.add_argument("-dsn", "--dosta_serial_number", dest="dosta_serial", type=str, required=False)
    parser.add_argument("-fsn", "--flord_serial_number", dest="flord_serial", type=str, required=False)
    parser.add_argument("-df", "--devfile", dest="devfile", type=str, required=False)
    parser.add_argument("-u", "--csvurl", dest="csvurl", type=str, required=False)
    parser.add_argument("-s", "--switch", dest="switch", type=str, required=False)

    # parse the input arguments and create a parser object
    return parser.parse_args(args)
