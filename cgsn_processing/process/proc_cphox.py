#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_cphox
@file cgsn_processing/process/proc_cphox.py
@author Christopher Wingard
@brief Creates a NetCDF dataset for the Sea-Bird Electronics Deep SeapHOx V2
    data from the JSON formatted data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from calendar import timegm
from gsw import SA_from_SP, pt0_from_t, CT_from_pt, sigma0, z_from_p
import PyCO2SYS as pyco2

from cgsn_processing.process.common import ENCODING, inputs, json2df, update_dataset
from cgsn_processing.process.configs.attr_cphox import CPHOX


def ph_total(vrs_ext, degc, psu, dbar, k0, k2, f):
    """
    Calculate the total pH from the SeapHOx sensor. The total pH is calculated
    from the external voltage (vrs_ext), temperature (degC), salinity (psu),
    pressure (dbar), and the calibration coefficients (k0, k2, f). Source is
    Sea-Bird Scientific Application Note 99, "Calculating pH from ISFET pH
    Sensors" ().

    :param vrs_ext:
    :param degc:
    :param psu:
    :param dbar:
    :param k0:
    :param k2:
    :param f:
    :return:
    """
    fp = f[0] * dbar + f[1] * dbar**2 + f[2] * dbar**3 + f[3] * dbar**4 + f[4] * dbar**5 + f[5] * dbar**6
    bar = dbar * 0.10  # convert pressure from dbar to bar

    # Nernstian response of the pH electrode (slope of the response)
    R = 8.3144621      # J/(mol K) universal gas constant
    T = degc + 273.15  # temperature in Kelvin
    F = 9.6485365e4    # C/mol Faraday constant
    snerst = R * T * np.log(10) / F

    # total chloride in seawater
    cl_total = (0.99889 / 35.453) * (psu / 1.80655) * (1000 / (1000 - 1.005 * psu))

    # partial Molal volume of HCl (calculated as Millero 1983)
    vhcl = 17.85 + 0.1044 * degc - 0.0001316 * degc**2

    # Sample ionic strength (calculated as Dickson et al. 2007)
    I = (19.924 * psu) / (1000 - 1.005 * psu)

    # Debye-Huckel constant for activity of HCl (calculated as Khoo et al. 1977)
    Adh = 0.0000034286 * degc**2 + 0.00067503 * degc + 0.49172143

    # log of the activity coefficient of HCl as a function of temperature (calculated as Khoo et al. 1977)
    loghclt = ((-Adh * np.sqrt(I)) / (1 + 1.394 * np.sqrt(I))) + (0.08885 - 0.000111 * degc) * I

    # log10 of the activity coefficient of HCl as a function of temperature and pressure (calculated as Johnson et
    # al. 2017)
    loghcltp = loghclt + (((vhcl * bar) / (np.log(10) * R * T * 10)) / 2)

    # total sulfate in seawater (calculated as Dickson et al. 2007)
    so4_total = (0.1400 / 96.062) * (psu / 1.80655)

    # acid disassociation constant of HSO4- (calculated as Dickson et al. 2007)
    Ks = (1 - 0.001005 * psu) * np.exp((-4276.1 / T) + 141.328 - 23.093 * np.log(T) + ((-13856 / T) + 324.57 - 47.986 *
                                       np.log(T)) * np.sqrt(I) + ((35474 / T) - 771.54 + 114.723 * np.log(T)) *
                                       I - (2698 / T) * I**1.5 + (1776 / T) * I**2)

    # partial Molal volume of HSO4- (calculated as Millero 1983)
    vHSO4 = -18.03 + 0.0466 * degc + 0.000316 * degc**2

    # compressibility of sulfate (calculated as Millero 1983)
    KbarS = (-4.53 + 0.09 * degc) / 1000

    # acid disassociation constant of HSO4- as function of salinity, temperature, and pressure (calculated as Millero
    # 1982)
    Kstp = Ks * np.exp((-vHSO4 * bar + 0.5 * KbarS * bar**2) / (R * T * 10))

    # calculate the pH total, adjusted for pressure, temperature and salinity
    pH = (((vrs_ext - k0 - k2 * degc - fp) / snerst) + np.log10(cl_total) + 2 * loghcltp -
          np.log10(1 + (so4_total / Kstp)) - np.log10((1000 - 1.005 * psu) / 1000))

    return pH


def proc_cphox(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for the Sea-Bird Electronics Deep SeapHOx (combined
    CTD, dissolved oxygen and pH sensor). Loads the JSON formatted parsed
    data and saves the data to a NetCDF file.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform relative to the sea surface.
    :return cphox: xarray dataset with the processed SeapHOx data
    """
    # load the json data file as a pandas data frame
    cphox = json2df(infile)
    if cphox.empty:
        # json data file was empty, exiting
        return None

    # convert SeapHOx date/time string to a pandas.Timestamp date/time object and then to a epoch time in seconds
    utc = pd.to_datetime(cphox['sphox_date_time_string'], format='%Y-%m-%dT%H:%M:%S', utc=True)
    epts = [timegm(t.timetuple()) for t in utc]  # calculate the epoch time as seconds since 1970-01-01 in UTC
    cphox['sensor_time'] = epts

    # drop the DCL date and time string, we no longer need it
    cphox = cphox.drop(columns=['dcl_date_time_string', 'sphox_date_time_string'])

    # reset the error code and serial number to integers
    cphox['error_flag'] = cphox['error_flag'].astype(int)
    cphox['serial_number'] = cphox['serial_number'].astype(int)

    # convert the oxygen concentration from ml/l to umol/L and then to umol/kg per the SBE63 manual
    SA = SA_from_SP(cphox['salinity'].values, cphox['pressure'].values, lon, lat)
    pt0 = pt0_from_t(SA, cphox['temperature'].values, cphox['pressure'].values)
    CT = CT_from_pt(SA, pt0)
    sigma = sigma0(SA, CT)
    cphox['oxygen_molar_concentration'] = cphox['oxygen_concentration'] * 44661.5 / 1000.  # umol/L
    cphox['oxygen_concentration_per_kg'] = cphox['oxygen_concentration'] * 44661.5 / (sigma + 1000.)  # umol/kg

    # replace the deployment depth with the actual depth from the pressure sensor
    depth = z_from_p(cphox['pressure'], lat)  # calculate the depth from the pressure
    darray = [depth.mean(), depth.min(), depth.max()]

    # Use the Lee et al. (2006) model to estimate the total alkalinity from the salinity and temperature (zone 4)
    cphox['estimated_alkalinity'] = (2305 + 53.23 * (cphox['salinity'] - 35) + 1.85 * (cphox['salinity'] - 35)**2 -
                                     14.72 * (cphox['temperature'] - 20) - 0.158 * (cphox['temperature'] - 20)**2 +
                                     0.062 * (cphox['temperature'] - 20) * lon)

    # calculate the estimated pCO2 from the estimated alkalinity and measured pH
    cphox['estimated_pco2'] = pyco2.sys(par1=cphox['estimated_alkalinity'], par1_type=1, par2=cphox['seawater_ph'],
                                        par2_type=3, opt_pH_scale=1, pressure=cphox['pressure'],
                                        temperature=cphox['temperature'], salinity=cphox['salinity'])['pCO2']

    # create an xarray data set from the data frame
    cphox = xr.Dataset.from_dataframe(cphox)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    cphox['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(cphox.time)).astype(str))
    cphox = update_dataset(cphox, platform, deployment, lat, lon, darray, CPHOX)
    return cphox


def main(argv=None):
    """
    Command line function to process the SeapHOx data using the proc_cphox
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

    # process the CTDBP data and save the results to disk
    cphox = proc_cphox(infile, platform, deployment, lat, lon, depth)
    if cphox:
        cphox.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
