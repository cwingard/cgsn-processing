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

from cgsn_processing.process.common import ENCODING, inputs, json2df, dict_update, update_dataset
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.configs.attr_cphox import CPHOX


def dissolved_oxygen(mlpl_doxy, degc, psu, dbar, lon, lat):
    """
    Calculate the dissolved oxygen concentration in umol/kg from the oxygen
    concentration in ml/l, temperature in degrees Celsius, salinity in
    practical salinity units, and pressure in decibars. The conversion is
    based on the Argo Data Management manual (Processing Argo OXYGEN
    data at the DAC level, 2022, v2.3.3 https://dx.doi.org/10.13155/39795).

    :param mlpl_doxy: oxygen concentration in ml/l as reported by the sensor
    :param degc: temperature in degrees Celsius recorded by the CTD sensor
    :param psu: salinity in practical salinity units recorded by the CTD sensor
    :param dbar: pressure in decibars recorded by the CTD sensor
    :param lon: longitude of the deployed sensor
    :param lat: latitude of the deployed sensor
    :return: dissolved oxygen concentration in umol/kg corrected for salinity,
        temperature, and pressure
    """
    # constants used in the calculations (see https://doi.org/10.13155/45915)
    b = [-6.24523e-3, -7.37614e-3, -1.03410e-2, -8.17083e-3]
    c = [-4.88682e-7]
    d = [24.4543, -67.4509, -4.8489, -5.44e-4]
    sref = 0.  # reference salinity (default value preset by the vendor)
    pref = 0.  # reference pressure (default value preset by the vendor)
    # Pcoef = [0.115, 0.00022, 0.0419]  # pressure correction coefficient (assumes correction applied)
    Pcoef = [0, 0.00016, 0.0307]  # pressure correction coefficient (assumes no correction applied)

    # convert the oxygen concentration from ml/l to umol/L
    molar_doxy = mlpl_doxy * 44.6596  # umol/L

    # salinity compensation of the oxygen concentration
    t_scaled = np.log((9298.15 - degc) / (273.15 + degc))
    t_abs = degc + 273.15
    pH20_tr = 1013.25 * np.exp(d[0] + d[1] * (100 / t_abs) + d[2] * np.log(t_abs / 100) + d[3] * sref)
    pH20_ts = 1013.25 * np.exp(d[0] + d[1] * (100 / t_abs) + d[2] * np.log(t_abs / 100) + d[3] * psu)
    a_tss = (1013.25 - pH20_tr) / (1013.25 - pH20_ts)
    scorr = a_tss ** np.exp((psu - sref) * (b[0] + b[1] * t_scaled + b[2] * t_scaled**2 + b[3] * t_scaled**3) +
                            c[0] * (psu**2 - sref**2))
    do_psal = molar_doxy * scorr

    # correction for pressure effects on quenching
    pcorr_sbe63 = np.exp(0.011 * pref / t_abs)
    do_psal_p = do_psal * (1 + (((Pcoef[1] * degc + Pcoef[2]) * dbar) / 1000)) / pcorr_sbe63

    # calculate the potential density from the CTD measurements
    SA = SA_from_SP(psu, dbar, lon, lat)
    pt0 = pt0_from_t(SA, degc, pref)
    CT = CT_from_pt(SA, pt0)
    sigma = (sigma0(SA, CT) + 1000) / 1000

    # convert the dissolved oxygen concentration to umol/kg
    doxy = do_psal_p / sigma
    return doxy


def ph_total(vrs_ext, degc, psu, dbar, k0, k2, f):
    """
    Calculate the total pH from the SeapHOx sensor. The total pH is calculated
    from the external voltage (vrs_ext), temperature (degC), salinity (psu),
    pressure (dbar), and the calibration coefficients (k0, k2, f). Source is
    Sea-Bird Scientific Application Note 99, "Calculating pH from ISFET pH
    Sensors".

    :param vrs_ext: external voltage from the FET sensor
    :param degc: temperature in degrees Celsius
    :param psu: salinity in practical salinity units
    :param dbar: pressure in decibars
    :param k0: calibration coefficient from vendor documentation
    :param k2: calibration coefficient from vendor documentation
    :param f: calibration coefficients (f0, f1, f2, f3, f4, f5) from the
        vendor documentation (as an array)
    :return: pH total
    """
    fp = f[0] * dbar + f[1] * dbar**2 + f[2] * dbar**3 + f[3] * dbar**4 + f[4] * dbar**5 + f[5] * dbar**6
    bar = dbar * 0.10  # convert pressure from dbar to bar

    # Nernstian response of the pH electrode (slope of the response)
    r = 8.3144621      # J/(mol K) universal gas constant
    t = degc + 273.15  # temperature in Kelvin
    f = 9.6485365e4    # C/mol Faraday constant
    snerst = r * t * np.log(10) / f

    # total chloride in seawater
    cl_total = (0.99889 / 35.453) * (psu / 1.80655) * (1000 / (1000 - 1.005 * psu))

    # partial Molal volume of HCl (calculated as Millero 1983)
    vhcl = 17.85 + 0.1044 * degc - 0.0001316 * degc**2

    # Sample ionic strength (calculated as Dickson et al. 2007)
    i = (19.924 * psu) / (1000 - 1.005 * psu)

    # Debye-Huckel constant for activity of HCl (calculated as Khoo et al. 1977)
    adh = 0.0000034286 * degc**2 + 0.00067503 * degc + 0.49172143

    # log of the activity coefficient of HCl as a function of temperature (calculated as Khoo et al. 1977)
    loghclt = ((-adh * np.sqrt(i)) / (1 + 1.394 * np.sqrt(i))) + (0.08885 - 0.000111 * degc) * i

    # log10 of the activity coefficient of HCl as a function of temperature and pressure (calculated as Johnson et
    # al. 2017)
    loghcltp = loghclt + (((vhcl * bar) / (np.log(10) * r * t * 10)) / 2)

    # total sulfate in seawater (calculated as Dickson et al. 2007)
    so4_total = (0.1400 / 96.062) * (psu / 1.80655)

    # acid disassociation constant of HSO4- (calculated as Dickson et al. 2007)
    ks = (1 - 0.001005 * psu) * np.exp((-4276.1 / t) + 141.328 - 23.093 * np.log(t) + ((-13856 / t) + 324.57 - 47.986 *
                                       np.log(t)) * np.sqrt(i) + ((35474 / t) - 771.54 + 114.723 * np.log(t)) *
                                       i - (2698 / t) * i**1.5 + (1776 / t) * i**2)

    # partial Molal volume of HSO4- (calculated as Millero 1983)
    v_hso4 = -18.03 + 0.0466 * degc + 0.000316 * degc**2

    # compressibility of sulfate (calculated as Millero 1983)
    kbar_s = (-4.53 + 0.09 * degc) / 1000

    # acid disassociation constant of HSO4- as function of salinity, temperature, and pressure (calculated as Millero
    # 1982)
    kstp = ks * np.exp((-v_hso4 * bar + 0.5 * kbar_s * bar**2) / (r * t * 10))

    # calculate the pH total, adjusted for pressure, temperature and salinity
    p_h = (((vrs_ext - k0 - k2 * degc - fp) / snerst) + np.log10(cl_total) + 2 * loghcltp -
           np.log10(1 + (so4_total / kstp)) - np.log10((1000 - 1.005 * psu) / 1000))

    return p_h


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
    # parse the kwargs to determine if estimated parameters are to be calculated
    estimated = kwargs.get('estimated', False)

    # load the json data file as a pandas data frame
    cphox = json2df(infile)
    if cphox.empty:
        # json data file was empty, exiting
        return None

    # TODO: use vendor calibration coefficients to re-calculate the total pH from the external voltage data

    # convert SeapHOx date/time string to a pandas.Timestamp date/time object and then to a epoch time in seconds
    utc = pd.to_datetime(cphox['sphox_date_time_string'], format='%Y-%m-%dT%H:%M:%S', utc=True)
    epts = [timegm(t.timetuple()) for t in utc]  # calculate the epoch time as seconds since 1970-01-01 in UTC
    cphox['sensor_time'] = epts

    # drop unnecessary time columns. Note: IMM-queried cphox will not have DCL timestamp
    if 'dcl_date_time_string' in cphox:
        cphox = cphox.drop(columns=['dcl_date_time_string', 'sphox_date_time_string'])
    else:
        cphox = cphox.drop(columns=['sphox_date_time_string'])

    # reset the error code and serial number to integers
    cphox['error_flag'] = cphox['error_flag'].astype(int)
    cphox['serial_number'] = cphox['serial_number'].astype(int)

    # convert the oxygen concentration from ml/l to umol/L and then to umol/kg per the Argo Data Management manual
    cphox['oxygen_molar_concentration'] = cphox['oxygen_concentration'] * 44.6596  # umol/L
    cphox['oxygen_concentration_per_kg'] = dissolved_oxygen(cphox['oxygen_concentration'].values,
                                                            cphox['temperature'].values, cphox['salinity'].values,
                                                            cphox['pressure'].values, lon, lat)

    # replace the deployment depth with the actual depth from the pressure sensor
    z = z_from_p(cphox['pressure'], lat)  # calculate the depth from the pressure
    darray = [depth, z.min(), z.max()]

    if estimated:  # calculate the estimated alkalinity
        # Use the Lee et al. (2006) models to estimate the total alkalinity from the salinity and temperature
        # (https://doi.org/10.1029/2006GL027207). More appropriate models may be available for the specific
        # deployment locations (especially in cases of freshwater intrusion). These estimates are intended to be
        # used by operators of the moorings in general assessments of the carbonate system as measured by other
        # co-located instruments.
        if 'CE' in platform:  # Coastal Endurance (Zone 4)
            cphox['estimated_alkalinity'] = (2305 + 53.23 * (cphox['salinity'] - 35) + 1.85 *
                                             (cphox['salinity'] - 35)**2 - 14.72 * (cphox['temperature'] - 20) -
                                             0.158 * (cphox['temperature'] - 20)**2 + 0.062 *
                                             (cphox['temperature'] - 20) * lon)
        else:  # Coastal Pioneer and Global Irminger (Zone 3)
            # North Atlantic (Pioneer and Irminger) model
            cphox['estimated_alkalinity'] = (2305 + 53.97 * (cphox['salinity'] - 35) + 2.74 *
                                             (cphox['salinity'] - 35)**2 - 1.16 * (cphox['temperature'] - 20) -
                                             0.040 * (cphox['temperature'] - 20)**2)

        # If the temperature is greater than 20 degrees Celsius, use the Subtropics model (Zone 1)
        zone1 = (2305 + 58.66 * (cphox['salinity'] - 35) + 2.32 * (cphox['salinity'] - 35)**2 -
                 1.41 * (cphox['temperature'] - 20) - 0.040 * (cphox['temperature'] - 20)**2)
        m = cphox['temperature'] > 20
        cphox['estimated_alkalinity'][m] = zone1[m]

    # create an xarray data set from the data frame
    cphox = xr.Dataset.from_dataframe(cphox)

    # assign/create needed dimensions, geo coordinates and update the metadata attributes for the data set
    cphox['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(cphox.time)).astype(str))
    attrs = dict_update(CPHOX, SHARED)  # add the shared the attributes
    cphox = update_dataset(cphox, platform, deployment, lat, lon, darray, attrs)
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
    if args.switch == "estimate":
        estimated = True
    else:
        estimated = False

    # process the SeapHOx data and save the results to disk
    cphox = proc_cphox(infile, platform, deployment, lat, lon, depth, estimated=estimated)
    if cphox:
        cphox.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
