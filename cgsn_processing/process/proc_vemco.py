#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_vemco
@file cgsn_processing/process/proc_vemco.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the VEMCO data from the JSON formatted data
"""
import glob
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import xarray as xr

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from cgsn_processing.process.common import ENCODING, inputs, json2obj, json_obj2df, update_dataset
from cgsn_processing.process.configs.attr_vemco import VEMCO


def proc_vemco(infile, platform, deployment, lat, lon, depth):
    """
    Processing function for the Vemco VR2C Acoustic Fish Tag Receiver. Loads
    the JSON formatted parsed data and the dataset processing level attribute
    is set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :return status: An xarray dataset with the processed VR2C status data
    :return tags: An xarray dataset with the processed VR2C tag detections
    """
    # load the json data file as a hierarchical dictionary for further processing
    vemco = json2obj(infile)
    if not vemco:
        # json data file was empty, exiting
        return None, None

    # rename the VR2C Date and Time variable and calculate the clock offset (used to track the VR2C clock drift)
    x = vemco['status'].pop('vr2c_date_time', None)
    vemco['status']['sensor_time'] = x
    vemco['status']['clock_offset'] = [vemco['status']['time'][i] - x[i] for i in range(len(x))]

    # create the status data set and update the metadata attributes
    status = json_obj2df(vemco, 'status')
    status = xr.Dataset.from_dataframe(status)
    status['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(status.time)).astype(str))
    status = update_dataset(status, platform, deployment, lat, lon, [depth, depth, depth], VEMCO)
    status.attrs['processing_level'] = 'parsed'

    # now do the same for the tag messages, if they are present
    tags = None  # we always have status messages, but we won't always have tag detections
    if vemco['tags']['time']:
        # create the tags data set and update the metadata attributes
        tags = json_obj2df(vemco, 'tags')
        tags = xr.Dataset.from_dataframe(tags)
        tags['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(tags.time)).astype(str))
        tags = update_dataset(tags, platform, deployment, lat, lon, [depth, depth, depth], VEMCO)
        tags.attrs['processing_level'] = 'parsed'

    # return the processed data
    return status, tags


def plot_vemco(sites, save_dirs):
    """
    """
    # set the base directories for the raw and parsed data
    raw_dir = os.path.abspath('/home/ooiuser/DS')
    parsed_dir = os.path.abspath('/home/ooiuser/data/parsed')
    data = {}
    for idx, site in enumerate(sites):
        # create a list of all the CSV files (aka tag detections) for that site
        csv_files = glob.glob(os.path.join(parsed_dir, site, '*_tags.csv'))

        # read in the CSV files and concatenate them into a single dataframe
        df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
        df['time'] = pd.to_datetime(df.time, unit='s')
        df = df.set_index('time')
        df = df.sort_index()

        # save the concatenated dataframe to a CSV file in the raw data directory
        #platform = site.split('/')[0]
        platform = site.split('/')[1]
        df.to_csv(os.path.join(raw_dir, save_dirs[idx], platform + '_vemco_fish_tags.csv'), mode='w',
                  date_format='%Y-%m-%dT%H:%M:%SZ')

        # add the data to the dictionary
        data[platform] = df

    # plot the data combining all the sites into a single plot
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    for platform, df in data.items():
        # group the data into unique tag IDs observed per day
        detections = df.groupby(df.index.date).tag_id.nunique()

        # plot a running total of the number of unique tags observed over the entire deployment
        ax[0].plot(detections.cumsum(), label=platform)
        ax[0].set_ylabel('Unique Tags Observed')

        # plot the number of unique tag IDs observed per day
        ax[1].bar(detections.index, detections.values, width=3/24, label=platform)
        detections.plot(ax=ax[1], label=platform, style='o')
        ax[1].set_ylabel('Unique Tags per Day')

    # add the legend, and other plot attributes
    ax[0].legend(loc='upper left')
    ax[0].set_xlim(pd.Timestamp('2024-10-01', tz='UTC'), pd.Timestamp.now('UTC'))
    ax[0].xaxis.set_major_locator(mdates.DayLocator(interval=14))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax[1].yaxis.set_major_locator(MultipleLocator(1))
    ax[1].yaxis.set_major_formatter(FormatStrFormatter('% 1.0f'))
    fig.autofmt_xdate()


def main(argv=None):
    """
    Command line function to process the VEMCO data using the proc_vemco
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

    # process the VEMCO data and save the results to disk
    status, tags = proc_vemco(infile, platform, deployment, lat, lon, depth)
    if status is not None:
        status.to_netcdf(outfile.replace('.nc', '_status.nc'), mode='w', format='NETCDF4',
                         engine='netcdf4', encoding=ENCODING)

    if tags is not None:
        tags.to_netcdf(outfile.replace('.nc', '_tags.nc'), mode='w', format='NETCDF4',
                       engine='netcdf4', encoding=ENCODING)

        # save the tag data to a CSV file for PI use and later plotting
        tags = tags.squeeze(dim='station', drop=True)  # remove the station dimension
        tags = tags.reset_coords()
        df = tags.to_dataframe()  # convert the xarray dataset to a pandas dataframe
        columns = ['serial_number', 'sequence', 'code_space', 'tag_id', 'sensor_data']
        csvfile = infile.replace('.json', '_tags.csv')  # save the CSV file in the same directory as the JSON file
        df.to_csv(csvfile, mode='w', columns=columns)   # save the CSV file


if __name__ == '__main__':
    main()
