#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_pco2a
@file cgsn_processing/process/proc_pco2a.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the PCO2A from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from cgsn_processing.process.common import inputs, json2df, update_dataset, ENCODING, dict_update, colocated_ctd
from cgsn_processing.process.configs.attr_pco2a import PCO2A
from cgsn_processing.process.configs.attr_common import SHARED

from gsw import SP_from_C
from pyseas.data.co2_functions import co2_ppressure, co2_co2flux


def wind_10m(u, v, zwnd=4.0):
    """
    Instantaneous wind speed at a height of 10 m derived from the METBK east
    (v) and north (u) wind speed measurements recorded at height zwnd. Used
    to calculate the pCO2 flux.

    :param u: northward wind speed (m/s)
    :param v: eastward wind speed (m/s)
    :param zwnd: height of wind speed measurements (m) above the sea surface,
        deaults to 4.0 m
    :return u10: the instantaneous wind speed at a height of 10 m (m/s)
    """
    # calculate wind speed at 10 m
    u10 = np.sqrt(u ** 2 + v ** 2) * (10.0 / zwnd) ** 0.11
    return u10


def proc_pco2a(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main PCO2A processing function. Loads the JSON formatted parsed data and
    converts data into a NetCDF data file using xarray.  Partial pressure of
    CO2 (uatm) in air or seawater is calculated from the CO2 mole fraction
    (ppm), the gas stream pressure (mbar) and standard atmospheric pressure set
    to a default of 1013.25 mbar/atm. Data is resampled to an hourly average
    and the pCO2 flux (mmol/m2/day) is calculated using the CO2 flux function
    from the pyseas package (derived from  Wanninkhof 1992,
    doi:10.1029/92JC00188)

    :param infile: JSON formatted parsed data file.
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.
    **kwargs metbk_name: Name of directory with data from the co-located METBK
        sensor. The wind data will be used to calculate the pCO2 flux.

    :return pco2a: xarray dataset with the PCO2A data.
    :return flux: xarray dataset with hourly averaged PCO2A data and calculated
        pCO2 flux.
    """
    # process the variable length keyword arguments
    metbk_name = kwargs.get('metbk_name')

    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # there was no data in this file, ending early
        return None

    # clean up some of the data
    df.drop(['dcl_date_time_string', 'co2_date_time_string'], axis=1, inplace=True)

    # rename the CO2 measurement variable to remove the word "water" since it can be from either air or water, and
    # use the terminology from the vendor documentation.
    df.rename(columns={'measured_water_co2': 'co2_mole_fraction'}, inplace=True)

    # calculate the partial pressure of CO2 in the air and water samples
    df['pCO2'] = co2_ppressure(df['co2_mole_fraction'], df['gas_stream_pressure'])

    # create an xarray data set from the data frame
    pco2a = xr.Dataset.from_dataframe(df)

    # split out the air and water samples for further processing below
    air = pco2a['pCO2'].where(pco2a['co2_source'] == 'A', drop=True)
    air = air.rename('pCO2_atmospheric')
    water = pco2a['pCO2'].where(pco2a['co2_source'] == 'W', drop=True)
    water = water.rename('pCO2_seawater')

    # clean up the PCO2A dataset and assign attributes
    pco2a['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(pco2a.time)).astype(str))
    attrs = dict_update(PCO2A, SHARED)  # add the shared attributes
    pco2a = update_dataset(pco2a, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    pco2a.attrs['processing_level'] = 'processed'

    # resample the air and water datasets to hourly averages
    air['time'] = air.time.dt.round('1H')  # round the time to the nearest hour
    air = air.resample(time='1H').median(dim='time', keep_attrs=True)
    air = air.interpolate_na(dim='time', max_gap='3Hour')  # interpolate any gaps less than 3 hours in the data
    air = air.where(~np.isnan(air), drop=True)  # drop any remaining NaNs

    water['time'] = water.time.dt.round('1H')  # round the time to the nearest hour
    water = water.resample(time='1H').median(dim='time', keep_attrs=True)
    water = water.interpolate_na(dim='time', max_gap='3Hour')  # interpolate any gaps less than 3 hours in the data
    water = water.where(~np.isnan(water), drop=True)  # drop any remaining NaNs

    # combine the air and water datasets back into a single dataset
    flux = xr.merge([air, water], join='inner')

    # create filled values for the instantaneous 10 m wind speed and the pCO2 flux (in case the metbk data is missing)
    fill_data = np.full(len(flux.time), np.nan)
    flux['air_temperature'] = xr.DataArray(fill_data, coords=[flux.time], dims=['time'])
    flux['sea_surface_temperature'] = xr.DataArray(fill_data, coords=[flux.time], dims=['time'])
    flux['sea_surface_salinity'] = xr.DataArray(fill_data, coords=[flux.time], dims=['time'])
    flux['u10'] = xr.DataArray(fill_data, coords=[flux.time], dims=['time'])
    flux['co2_flux'] = xr.DataArray(fill_data, coords=[flux.time], dims=['time'])

    # check for data from a co-located METBK and test to see if it covers our time range of interest.
    metbk = pd.DataFrame()
    if metbk_name:
        metbk = colocated_ctd(infile, metbk_name)

    if not metbk.empty:
        metbk = xr.Dataset.from_dataframe(metbk)

        # test to see if the metbk covers our time of interest for this PCO2A file
        td = timedelta(hours=1)
        coverage = (metbk['time'].min() <= flux['time'].min() and metbk['time'].max() + td >= flux['time'].max())

        # interpolate the CTD data if we have full coverage
        if coverage:
            # resample the metbk data to 10 minute median averages and calculate the 10 m wind speed and
            # sea surface salinity
            metbk = metbk.resample(time='10Min').median(dim='time', keep_attrs=True)
            u10 = wind_10m(metbk['northward_wind_velocity'], metbk['eastward_wind_velocity'])
            psu = SP_from_C(metbk['sea_surface_conductivity'] * 10, metbk['sea_surface_temperature'], 0)

            # interpolate the 10 m wind speed to the flux time stamps as well as the other metbk variables
            u10 = np.interp(flux['time'], metbk['time'], u10)
            psu = np.interp(flux['time'], metbk['time'], psu)
            sst = np.interp(flux['time'], metbk['time'], metbk['sea_surface_temperature'])
            air_temp = np.interp(flux['time'], metbk['time'], metbk['air_temperature'])

            # assign the metbk variables to the flux dataset
            flux['u10'] = xr.DataArray(u10, coords=[flux.time], dims=['time'])
            flux['sea_surface_salinity'] = xr.DataArray(psu, coords=[flux.time], dims=['time'])
            flux['sea_surface_temperature'] = xr.DataArray(sst, coords=[flux.time], dims=['time'])
            flux['air_temperature'] = xr.DataArray(air_temp, coords=[flux.time], dims=['time'])

            # calculate the pCO2 flux (in umol/m^2/s) using the 10 m wind speed, sea surface temperature, and salinity
            flux['co2_flux'] = co2_co2flux(flux['seawater_co2_ppressure'], flux['atmospheric_co2_ppressure'], u10,
                                           sst, psu) * 1e6

    # add the attributes to the flux dataset
    flux['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(flux.time)).astype(str))
    attrs = dict_update(PCO2A, SHARED)  # add the shared attributes
    flux = update_dataset(flux, platform, deployment, lat, lon, [depth, depth, depth], attrs)
    flux.attrs['processing_level'] = 'processed'

    return pco2a, flux


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

    # process the PCO2A data and save the results to disk
    pco2a, flux = proc_pco2a(infile, platform, deployment, lat, lon, depth)
    if pco2a:
        flux_file = outfile.replace('_pco2a_', '_pco2_flux_')
        pco2a.to_netcdf(outfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)
        flux.to_netcdf(flux_file, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)


if __name__ == '__main__':
    main()
