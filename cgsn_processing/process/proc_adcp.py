#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_adcp
@file cgsn_processing/process/proc_adcp.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for ADCP from JSON formatted source data
"""
import datetime
import json
import numpy as np
import os
import pandas as pd
import xarray as xr
import re

from cgsn_processing.process.common import inputs, dict_update
from cgsn_processing.process.configs.attr_adcp import ADCP, PD0, PD8, DERIVED


def json_sub2df(data, sub):
    """
    Take a JSON formatted data object, read in as a dict, pull out the subarray of interest, and return the results as
    a panda data frame.
    """
    df = pd.DataFrame(data[sub])
    if df.empty:
        return df

    df['time'] = pd.to_datetime(data['time'], unit='s')
    df.set_index('time', drop=True, inplace=True)

    for col in df.columns:
        if df[col].dtype == np.int64:
            df[col] = df[col].astype(np.int32)

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
    adcp_type = args.switch

    # load the json data file
    with open(infile) as jf:
        data = json.load(jf)

    # create the time coordinate array and setup a data frame with the global values used above
    time = np.array(data['time'])
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(time, unit='s')
    df.index = df['time']
    df['deploy_id'] = deployment
    glbl = xr.Dataset.from_dataframe(df)

    # Process PD0 formatted data
    if adcp_type.lower == 'pd0':

        # create the bin number coordinate array
        bin_number = np.arange(data['fixed']['num_cells'][0] - 1).astype(np.int32)

        # load the fixed header data packets
        df = json_sub2df(data, 'fixed')
        fx = xr.Dataset.from_dataframe(df)

        # combine the time_per_ping_seconds and the time_per_ping_minutes into a single variable, ping_period.
        fx['ping_period'] = fx['time_per_ping_seconds'] + (fx['time_per_ping_minutes'] / 60)
        fx = fx.drop(['time_per_ping_seconds', 'time_per_ping_minutes'])    # drop the sub-components

        # load the variable leader data packets
        df = json_sub2df(data, 'variable')
        vbl = xr.Dataset.from_dataframe(df)

        # drop real-time clock arrays 1 and 2, rewriting the data as an ISO 8601 combined date and time string.
        rtc_string = ["{:2d}{:02d}{:02d}{:02d}T{:02d}{:02d}{:02d}.{:03d}Z".format(rtc[0], rtc[1], rtc[2], rtc[3],
                                                                                  rtc[4], rtc[5], rtc[6], rtc[7])
                      for rtc in vbl['real_time_clock2'].values]
        rtc = xr.Dataset({'real_time_clock': (['time'], rtc_string)},
                         coords={'time': (['time'], pd.to_datetime(time, unit='s'))})
        vbl = vbl.drop(['real_time_clock1', 'real_time_clock2'])    # drop the sub-components

        # use the ensemble number and increment variables (ensemble number rolls over at 65535) to calculate the
        # sequential ensemble number
        vbl['ensemble_number'] = vbl['ensemble_number'] + (vbl['ensemble_number_increment'] * 65535)
        vbl = vbl.drop(['ensemble_number_increment'])   # drop the sub-components

        # create the 2D velocity, correlation magnitude, echo intensity and percent good data sets
        vel = xr.Dataset({
            'eastward': (['time', 'bin_number'], np.array(data['velocity']['eastward']).astype(np.int32)),
            'northward': (['time', 'bin_number'], np.array(data['velocity']['northward']).astype(np.int32)),
            'vertical': (['time', 'bin_number'], np.array(data['velocity']['vertical']).astype(np.int32)),
            'error': (['time', 'bin_number'], np.array(data['velocity']['error']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        cor = xr.Dataset({
            'magnitude_beam1': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam1']).astype(np.int32)),
            'magnitude_beam2': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam2']).astype(np.int32)),
            'magnitude_beam3': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam3']).astype(np.int32)),
            'magnitude_beam4': (['time', 'bin_number'], np.array(data['correlation']['magnitude_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        echo = xr.Dataset({
            'intensity_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1']).astype(np.int32)),
            'intensity_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2']).astype(np.int32)),
            'intensity_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3']).astype(np.int32)),
            'intensity_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        per = xr.Dataset({
            'good_3beam': (['time', 'bin_number'], np.array(data['percent']['good_3beam']).astype(np.int32)),
            'transforms_reject': (['time', 'bin_number'], np.array(data['percent']['transforms_reject']).astype(np.int32)),
            'bad_beams': (['time', 'bin_number'], np.array(data['percent']['bad_beams']).astype(np.int32)),
            'good_4beam': (['time', 'bin_number'], np.array(data['percent']['good_4beam']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        # combine it all into one data set
        adcp = xr.merge([glbl, fx, vbl, rtc, vel, cor, echo, per])
        adcp['time'] = adcp.time.values.astype(float) / 10.0 ** 9  # Convert from nanoseconds to seconds since 1970
        adcp_attrs = PD0    # use the PD0 attributes

        # Compute the vertical extent of the data for the global metadata attributes
        if adcp.sysconfig_vertical_orientation.values[0][0]:
            # ADCP is looking upwards, max depth is the deployment depth and the min depth is the surface
            vmax = depth
            vmin = 0.0
        else:
            # ADCP is looking downward, we reverse the logic from above and compute the full range for the max depth
            vmin = depth
            vmax = vmin + adcp.depth_cell_length.values[0][0] / 100 * max(bin_number)

    elif adcp_type == 'PD8':
        # load the subset of variable header data included with a PD8 dataset
        df = json_sub2df(data, 'variable')
        vbl = xr.Dataset.from_dataframe(df)

        # pull the bin number out of the velocity data set
        bin_number = np.array(data['velocity']['bin_number'][0]).astype(np.int32)

        # create the 2D velocity and echo intensity data sets
        vel = xr.Dataset({
            'direction': (['time', 'bin_number'], np.array(data['velocity']['direction']).astype(np.float)),
            'magnitude': (['time', 'bin_number'], np.array(data['velocity']['magnitude']).astype(np.float)),
            'eastward': (['time', 'bin_number'], np.array(data['velocity']['eastward']).astype(np.int32)),
            'northward': (['time', 'bin_number'], np.array(data['velocity']['northward']).astype(np.int32)),
            'vertical': (['time', 'bin_number'], np.array(data['velocity']['vertical']).astype(np.int32)),
            'error': (['time', 'bin_number'], np.array(data['velocity']['error']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        echo = xr.Dataset({
            'intensity_beam1': (['time', 'bin_number'], np.array(data['echo']['intensity_beam1']).astype(np.int32)),
            'intensity_beam2': (['time', 'bin_number'], np.array(data['echo']['intensity_beam2']).astype(np.int32)),
            'intensity_beam3': (['time', 'bin_number'], np.array(data['echo']['intensity_beam3']).astype(np.int32)),
            'intensity_beam4': (['time', 'bin_number'], np.array(data['echo']['intensity_beam4']).astype(np.int32))
        }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
                   'bin_number': bin_number})

        # combine it all into one data set
        adcp = xr.merge([glbl, vbl, vel, echo])
        adcp['time'] = adcp.time.values.astype(float) / 10.0 ** 9  # Convert from nanoseconds to seconds since 1970
        adcp_attrs = PD8    # use the PD8 attributes

        # Compute the vertical extent of the data for the global metadata attributes. Only Pioneer uses PD8 and all of
        # their units are on MFNs looking upward.
        vmax = depth
        vmin = 0.0

    # add a default station identifier as a coordinate variable to the adcp dataset
    adcp.coords['station'] = np.int32(0)
    adcp = adcp.expand_dims('station', axis=None)

    # add the geospatial coordinates using station as the dimension
    geo_coords = xr.Dataset({
        'lat': ('station', [lat]),
        'lon': ('station', [lon]),
        'z': ('station', [depth])
    }, coords={'station': [np.int32(0)]})
    adcp = xr.merge([adcp, geo_coords])

    # add to the global attributes for the ADCP
    attrs = dict_update(ADCP, adcp_attrs)   # merge default and PD0 attribute dictionaries into a single dictionary
    attrs = dict_update(attrs, DERIVED)     # add the derived attributes

    # update the global attributes
    attrs['global'] = dict_update(attrs['global'], {
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment)),
        'date_created': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00Z"),
        'geospatial_lat_max': lat,
        'geospatial_lat_min': lat,
        'geospatial_lon_max': lon,
        'geospatial_lon_min': lon,
        'geospatial_vertical_max': vmax,
        'geospatial_vertical_min': vmin,
        'geospatial_vertical_positive': 'down',
        'geospatial_vertical_units': 'm'
    })

    # ... and assign the updated attributes to the global metadata and the individual variables ...
    adcp.attrs = attrs['global']
    for v in adcp.variables:
        if v not in ['time', 'lat', 'lon', 'z', 'station', 'bin_number']:
            adcp[v].attrs = dict_update(attrs[v], {'coordinates': 'time lat lon z'})
        else:
            adcp[v].attrs = attrs[v]

    # correct some encoding inconsistencies between xarray and a CF compliant NetCDF file
    encoding = {
        'time': {'_FillValue': False},
        'lat': {'_FillValue': False},
        'lon': {'_FillValue': False},
        'z': {'_FillValue': False},
        'station': {'dtype': np.int32}
    }

    # save the file
    adcp.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=encoding)


if __name__ == '__main__':
    main()
