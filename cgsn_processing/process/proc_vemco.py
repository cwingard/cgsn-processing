#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_vemco
@file cgsn_processing/process/proc_vemco.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the VEMCO data from the JSON formatted data
"""
import argparse
import glob
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sys
import xarray as xr

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from cgsn_processing.process.common import ENCODING, json2obj, json_obj2df, update_dataset
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


def plot_vemco(site_dirs, save_dirs, png_dir):
    """
    Function to plot the VEMCO data for the OOI Endurance array. The function
    reads in the parsed data from the CSV files, concatenates them into a single
    dataframe, and then saves the concatenated dataframe to a CSV file in the
    raw data directory. The function then plots the data combining all the sites
    into a single plot.

    :param site_dirs: List of directories containing the parsed data for each site
    :param save_dirs: List of directories to save the concatenated data for each site
    :param png_dir: Directory to save the plot
    :return: None
    """
    # set the base directories for the raw and parsed data
    raw_dir = os.path.abspath('/home/ooiuser/DS')
    parsed_dir = os.path.abspath('/home/ooiuser/data/parsed')
    data = {}
    for idx, site in enumerate(site_dirs):
        # create a list of all the CSV files (aka tag detections) for that site
        csv_files = glob.glob(os.path.join(parsed_dir, site, '*_tags.csv'))

        # read in the CSV files and concatenate them into a single dataframe
        df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
        df['time'] = pd.to_datetime(df.time, unit='s')
        df = df.set_index('time')
        df = df.sort_index()

        # save the concatenated dataframe to a CSV file in the raw data directory
        platform = site.split('/')[0]
        df.to_csv(os.path.join(raw_dir, save_dirs[idx], platform + '_vemco_fish_tags.csv'), mode='w',
                  date_format='%Y-%m-%dT%H:%M:%SZ')

        # add the data to the dictionary
        data[platform] = df

    # plot the data combining all the sites into a single plot
    fig, ax = plt.subplots(2, 1, figsize=(11, 8.5), sharex=True)
    colors = ['RoyalBlue', 'Orange', 'LimeGreen']
    bottom = None
    idx = 0
    for platform, df in data.items():
        # group the data into unique tag IDs observed per day and reindex to fill in any missing days
        detections = df.groupby(df.index.date).tag_id.nunique()
        detections = detections.reindex(pd.date_range('2024-10-01', pd.Timestamp.now(), freq='D'), fill_value=0)

        # plot a running total of the number of unique tags observed over the entire deployment
        ax[0].plot(detections.cumsum(), label=platform, linewidth=3.0, color=colors[idx])
        ax[0].set_ylabel('Number of Tags')

        # plot the number of unique tags observed per day
        if idx == 0:
            bottom = detections.copy()
            ax[1].bar(detections.index, detections, label=platform, color=colors[idx])
        else:
            ax[1].bar(detections.index, detections, bottom=bottom, label=platform, color=colors[idx])
            bottom += detections
        # set the y-axis label for the lower subplot and increment the index
        ax[1].set_ylabel('Number of Tags')
        idx += 1

    # add the legend
    ax[0].legend(loc='lower right')

    # set x- and y-axis limits and styles for the upper subplot
    ax[0].set_ylim(0, None)
    ax[0].set_xlim(pd.Timestamp('2024-10-01'), pd.Timestamp('2025-06-01'))
    ax[0].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax[0].minorticks_off()
    fig.autofmt_xdate()

    # set x- and y-axis limits and styles for the lower subplot
    ax[1].set_ylim(0, None)
    ax[1].yaxis.set_major_locator(MultipleLocator(1))
    ax[1].yaxis.set_major_formatter(FormatStrFormatter('% 1.0f'))

    # add a title and save the plot
    ax[0].title.set_text('Cumulative Unique Daily Tag Observations')
    ax[1].title.set_text('Unique Tag Observations per Day')
    plt.savefig(os.path.join(raw_dir, png_dir, 'ooi_endurance_vemco_fish_tags.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)


def inputs(args=None):
    """
    Overwrite default argparse options set up in cgsn_processing.process.common
    in order to account for the different input parameters required for
    processing and plotting the VEMCO data.

    :param args: List of input arguments to parse
    :return: parser object with input arguments
    """
    if args is None:
        args = sys.argv[1:]

    # initialize argument parser
    parser = argparse.ArgumentParser(description="""Depending on the subparser choose, either process the 
                                                    data files, converting data from engineering units
                                                    to scientific units and saving as NetCDF, or create
                                                    plots of the data. The input arguments are parsed and
                                                    passed to the appropriate function.""",
                                     epilog="""Plot or process and convert data file(s) to NetCDF""")
    # create subparsers for the different processing options
    subparsers = parser.add_subparsers(title="subcommands")

    # create a parser for the process subcommand
    parser_process = subparsers.add_parser('proc_vemco')
    parser_process.add_argument('-i', '--infile', dest='infile', type=str, required=True)
    parser_process.add_argument('-o', '--outfile', dest='outfile', type=str, required=True)
    parser_process.add_argument('-p', '--platform', dest='platform', type=str, required=True)
    parser_process.add_argument('-d', '--deployment', dest='deployment', type=str, required=True)
    parser_process.add_argument('-lt', '--latitude', dest='latitude', type=float, required=True)
    parser_process.add_argument('-lg', '--longitude', dest='longitude', type=float, required=True)
    parser_process.add_argument('-dp', '--depth', dest='depth', type=float, required=True)
    parser_process.set_defaults(func=proc_vemco)

    # create a parser for the plot subcommand
    parser_plot = subparsers.add_parser('plot_vemco')
    parser_plot.add_argument('-pd', '--site_dirs', dest='site_dirs', nargs='+', type=str, required=True,
                             help='List of directories containing the parsed data')
    parser_plot.add_argument('-rd', '--save_dirs', dest='save_dirs', nargs='+', type=str, required=True,
                             help='List of directories to save the concatenated data')
    parser_plot.add_argument('-p', '--png_dir', dest='png_dir', type=str, required=True,
                             help='Directory to save the resulting plot')
    parser_plot.set_defaults(func=plot_vemco)

    # parse the input arguments and create a parser object to return
    return parser.parse_args(args)


def main(argv=None):
    """
    Command line function to process the VEMCO data using the proc_vemco
    function. Command line arguments are parsed and passed to the function.

    :param argv: List of command line arguments
    """
    # load the input arguments
    args = inputs(argv)
    if args.func.__name__ == 'plot_vemco':
        # plot the VEMCO data for the OOI Endurance array
        plot_vemco(args.site_dirs, args.save_dirs, args.png_dir)
    elif args.func.__name__ == 'proc_vemco':
        # process the VEMCO data using the input arguments
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

            # save the tag data to a CSV file for later plotting and PI use (see plot_vemco, which is called separately)
            tags = tags.squeeze(dim='station', drop=True)  # remove the station dimension
            tags = tags.reset_coords()
            df = tags.to_dataframe()  # convert the xarray dataset to a pandas dataframe
            columns = ['serial_number', 'sequence', 'code_space', 'tag_id', 'sensor_data']
            csvfile = infile.replace('.json', '_tags.csv')  # save the CSV file in the same directory as the JSON file
            df.to_csv(csvfile, mode='w', columns=columns)   # save the CSV file
    else:
        print('No valid function selected. Exiting.')
        sys.exit(1)


if __name__ == '__main__':
    main()
