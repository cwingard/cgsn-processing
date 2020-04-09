#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_parsers.process.proc_optaa
@file cgsn_parsers/process/proc_optaa
@author Initially by Russell Desiderio with rewriting by Christopher Wingard
@brief Reads in the parsed OPTAA data and applies the calibration, temperature, salinity and scattering corrections
    to the data, saving the resulting data to NetCDF files for further review
"""
import json
import numpy as np
import os
import pandas as pd
import re
import requests
import xarray as xr

from cgsn_processing.process.common import Coefficients, inputs, json2obj, update_dataset, ENCODING, FILL_INT
from cgsn_processing.process.configs.attr_optaa import OPTAA
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.opt_functions import opt_internal_temp, opt_external_temp
from pyseas.data.opt_functions import opt_pressure, opt_pd_calc, opt_tempsal_corr


class Calibrations(Coefficients):
    def __init__(self, coeff_file, dev_file=None, hdr_url=None, tca_url=None, tcc_url=None):
        """
        Loads the OPTAA factory calibration coefficients for a unit. Values come from either a serialized object
        created per instrument and deployment (calibration coefficients do not change in the middle of a deployment),
        from the factory supplied device file, or from parsed CSV files maintained on GitHub by the OOI CI team.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.dev_file = dev_file
        self.hdr_url = hdr_url
        self.tca_url = tca_url
        self.tcc_url = tcc_url

    def read_devfile(self, dev_file):
        """
        Reads the values from an ac-s device file into a python dictionary.
        """
        # read in the device file
        with open(dev_file, 'r') as f:
            data = f.readlines()
    
        # create the coefficients dictionary and assign values, first from the header portion of the device file
        nbin = np.int(data[8].split()[0])   # going to need this value later...
        coeffs = {
            'serial_number': np.mod(np.int(data[1].split()[0], 16), 4096),
            'temp_calibration': np.float(data[3].split()[1]),
            'pressure_coeff': np.array(data[4].split()[0:2]).astype(np.float),
            'pathlength': np.float(data[6].split()[0]),
            'num_wavelengths': np.int(data[7].split()[0]),
            'num_temp_bins': nbin,
            'temp_bins': np.array(data[9].split()[:-3]).astype(np.float)
        }

        # now we assign values from the array portion of the file
        awvl = []
        cwvl = []
        aoff = []
        coff = []
        ta_array = []
        tc_array = []
        for line in data[10:-1]:
            line = line.split()
            cwvl.append(np.float(re.sub('C', '', line[0])))
            awvl.append(np.float(re.sub('A', '', line[1])))
            coff.append(np.float(line[3]))
            aoff.append(np.float(line[4]))
            tc_array.append(np.array(line[5:5+nbin]).astype(np.float))
            ta_array.append(np.array(line[nbin+5:-12]).astype(np.float))
            
        # beam attenuation and absorption channel wavelengths
        coeffs['c_wavelengths'] = np.array(cwvl)
        coeffs['a_wavelengths'] = np.array(awvl)
        # beam attenuation and absorption channel clear water offsets
        coeffs['c_offsets'] = np.array(coff)
        coeffs['a_offsets'] = np.array(aoff)
        # temperature compensation values as f(wavelength, temperature) for the
        # beam attenuation and absorption channels
        coeffs['tc_array'] = np.array(tc_array)
        coeffs['ta_array'] = np.array(ta_array)
        
        # and save the resulting dictionary
        self.coeffs = coeffs
    
    def read_devurls(self, hdr_url, tca_url, tcc_url):
        """
        Reads the values from an ac-s device file already parsed and stored on
        Github as a set of 3 CSV files. Note, the formatting of those files 
        puts some constraints on this process. If someone has a cleaner method,
        I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}
        
        # read in the mostly header portion of the calibration data
        hdr = pd.read_csv(hdr_url, usecols=[0, 1, 2])
        for idx, row in hdr.iterrows():
            # beam attenuation and absorption channel clear water offsets
            if row[1] == 'CC_acwo':
                coeffs['a_offsets'] = np.array(json.loads(row[2]))
            if row[1] == 'CC_ccwo':
                coeffs['c_offsets'] = np.array(json.loads(row[2]))
            # beam attenuation and absorption channel wavelengths
            if row[1] == 'CC_awlngth':
                coeffs['a_wavelengths'] = np.array(json.loads(row[2]))
            if row[1] == 'CC_cwlngth':
                coeffs['c_wavelengths'] = np.array(json.loads(row[2]))
            # internal temperature compensation values
            if row[1] == 'CC_tbins':
                coeffs['temp_bins'] = np.array(json.loads(row[2]))
            # temperature of calibration water
            if row[1] == 'CC_tcal':
                coeffs['temp_calibration'] = np.float(row[2])

        # serial number, stripping off all but the numbers
        coeffs['serial_number'] = np.int(re.sub('[^0-9]', '',  hdr.serial[0]))
        # number of wavelengths
        coeffs['num_wavelengths'] = len(coeffs['a_wavelengths'])
        # number of internal temperature compensation bins
        coeffs['num_temp_bins'] = len(coeffs['temp_bins'])
        # pressure coefficients, set to 0 since not included in the CI csv files
        coeffs['pressure_coeff'] = [0, 0]

        # temperature compensation values as f(wavelength, temperature) for the
        # beam attenuation and absorption channels
        ta_array = []
        tc_array = []

        tcc = requests.get(tcc_url)
        for line in tcc.content.decode('utf-8').splitlines():
            tc_array.append(np.array(line.split(',')).astype(np.float))

        tca = requests.get(tca_url)
        for line in tca.content.decode('utf-8').splitlines():
            ta_array.append(np.array(line.split(',')).astype(np.float))

        coeffs['tc_array'] = np.array(tc_array)
        coeffs['ta_array'] = np.array(ta_array)
        
        # save the resulting dictionary
        self.coeffs = coeffs


def apply_dev(optaa, coeffs):
    """
    Processes the raw data contained in the optaa dictionary and applies the 
    factory calibration coefficents contained in the coeffs dictionary to
    convert the data into initial science units.
    """
    # convert internal and external temperature sensors
    optaa['internal_temp'] = opt_internal_temp(optaa['internal_temp_raw'])
    optaa['external_temp'] = opt_external_temp(optaa['external_temp_raw'])

    # calculate pressure, if sensor is equipped
    if np.all(coeffs['pressure_coeff'] == 0):
        # no pressure sensor, ignoring.
        optaa['pressure'] = np.NaN * np.array(optaa.pressure_raw)
    else:
        offset = coeffs['pressure_coeff'][0]
        slope = coeffs['pressure_coeff'][1]
        optaa['pressure'] = opt_pressure(optaa['pressure_raw'], offset, slope)

    # size up inputs and create a mask index to select real wavelengths (not the pads)
    a_ref = optaa['a_reference_raw']
    a_sig = optaa['a_signal_raw']
    c_ref = optaa['c_reference_raw']
    c_sig = optaa['c_signal_raw']
    npackets = a_ref.shape[0]
    wvlngth = a_ref[0, :].values != FILL_INT

    # initialize the output arrays
    apd = a_ref * np.nan
    cpd = c_ref * np.nan
    
    # calculate the L1 OPTAA data products (uncorrected beam attenuation and absorbance) for particulates
    # and dissolved organic matter with clear water removed.
    for ii in range(npackets):
        # calculate the uncorrected optical absorption coefficient [m^-1]
        apd[ii, wvlngth], _ = opt_pd_calc(a_ref[ii, wvlngth], a_sig[ii, wvlngth], coeffs['a_offsets'],
                                          optaa['internal_temp'].values[ii], coeffs['temp_bins'],
                                          coeffs['ta_array'])
        # calculate the uncorrected optical attenuation coefficient [m^-1]
        cpd[ii, wvlngth], _ = opt_pd_calc(c_ref[ii, wvlngth], c_sig[ii, wvlngth], coeffs['c_offsets'],
                                          optaa['internal_temp'].values[ii], coeffs['temp_bins'],
                                          coeffs['tc_array'])

    # save the results back to the data set
    optaa['apd'] = apd
    optaa['cpd'] = cpd

    # return the optaa dictionary with the factory calibrations applied
    return optaa


def apply_tscorr(optaa, coeffs, temp=None, salinity=None):
    """
    Corrects the absorption and beam attenuation data for the absorption
    of seawater as a function of seawater temperature and salinity (the
    calibration blanking offsets are determined using pure water.)
    
    If inputs temp or salinity are not supplied as calling arguments, then the 
    following default values are used.
        
        temp: temperature values recorded by the ac-s's external thermistor.
        salinity: 33.0 psu

    Otherwise, each of the arguments for temp and salinity should be either a 
    scalar, or a 1D array or a row or column vector with the same number of time
    points as 'a' and 'c'.
    """
    # setup the temperature and salinity arrays
    if temp is None:
        temp = optaa['external_temp'].values
    else: 
        if np.array(temp).size == 1:
            temp = np.ones_like(optaa['external_temp']) * temp
        else:
            temp = np.array(temp)
    
    if temp.size != optaa['time'].size:
        raise Exception("Mismatch: temperature array != number of OPTAA measurements")

    if salinity is None:
        salinity = np.ones_like(optaa['external_temp']) * 33.0
    else:
        if np.array(salinity).size == 1:
            salinity = np.ones_like(optaa['external_temp']) * salinity
        else:
            salinity = np.array(salinity)

    if salinity.size != optaa['time'].size:
        raise Exception("Mismatch: salinity array != number of OPTAA measurements")

    # setup and size the inputs
    apd = optaa['apd']
    cpd = optaa['cpd']
    npackets = apd.shape[0]
    wvlngth = ~np.isnan(apd[0, :].values)

    # initialize the output arrays
    apd_ts = apd * np.nan
    cpd_ts = cpd * np.nan

    # apply the temperature and salinity corrections
    for ii in range(npackets):
        apd_ts[ii, wvlngth] = opt_tempsal_corr('a', apd[ii, wvlngth], coeffs['a_wavelengths'],
                                               coeffs['temp_calibration'], temp[ii], salinity[ii])
        cpd_ts[ii, wvlngth] = opt_tempsal_corr('c', cpd[ii, wvlngth], coeffs['c_wavelengths'],
                                               coeffs['temp_calibration'], temp[ii], salinity[ii])
    
    # save the results
    optaa['apd_ts'] = apd_ts
    optaa['cpd_ts'] = cpd_ts
    return optaa


def apply_scatcorr(optaa, coeffs, method=1):
    """
    Correct the absorbance data for scattering using Method 1 (the default), with 715 nm used as the scattering
    wavelength.
    """
    if method != 1:
        raise Exception('Only scatter method = 1 is coded for the time being.')

    # find the closest wavelength to the reference wavelength
    reference_wavelength = 715.0
    idx = np.argmin(np.abs(coeffs['a_wavelengths'] - reference_wavelength))

    # use that wavelength as our scatter correction wavelength
    apd_ts = optaa['apd_ts']
    apd_ts_s = apd_ts - apd_ts[:, idx]

    # save the results
    optaa['apd_ts_s'] = apd_ts_s
    return optaa


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

    # load the json data file as a dictionary object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # load the instrument calibration data
    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('OPTAA', str(data['serial_number'][0]), data['time'][0])
        if csv_url:
            tca_url = re.sub('.csv', '__CC_taarray.ext', csv_url)
            tcc_url = re.sub('.csv', '__CC_tcarray.ext', csv_url)
            dev.read_devurls(csv_url, tca_url, tcc_url)
            dev.save_coeffs()
        else:
            print('A source for the OPTAA calibration coefficients for {} could not be found'.format(infile))
            return None

    # check the device file coefficients against the data file contents
    if dev.coeffs['serial_number'] != data['serial_number'][0]:
        raise Exception('Serial Number mismatch between ac-s data and the device file.')
    if dev.coeffs['num_wavelengths'] != data['num_wavelengths'][0]:
        raise Exception('Number of wavelengths mismatch between ac-s data and the device file.')

    # create the time coordinate array and setup a base data frame with all the 1D variables
    time = np.array(data['time'])
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(time, unit='s')
    df.set_index('time', drop=True, inplace=True)
    df['z'] = depth
    df['deploy_id'] = deployment
    df['serial_number'] = np.atleast_1d(data['serial_number']).astype(np.int32)
    df['elapsed_run_time'] = np.atleast_1d(data['elapsed_run_time']).astype(np.int32)
    df['internal_temp_raw'] = np.atleast_1d(data['internal_temp_raw']).astype(np.int32)
    df['external_temp_raw'] = np.atleast_1d(data['external_temp_raw']).astype(np.int32)
    df['pressure_raw'] = np.atleast_1d(data['pressure_raw']).astype(np.int32)
    df['a_signal_dark'] = np.atleast_1d(data['a_signal_dark']).astype(np.int32)
    df['a_reference_dark'] = np.atleast_1d(data['a_reference_dark']).astype(np.int32)
    df['c_signal_dark'] = np.atleast_1d(data['c_signal_dark']).astype(np.int32)
    df['c_reference_dark'] = np.atleast_1d(data['c_reference_dark']).astype(np.int32)

    # convert the data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the two dimensional arrays from the raw a and c channel measurements using the number of wavelengths
    # padded to 100 as the dimensional array.
    wavelength_number = np.arange(100).astype(np.int32)  # used as a dimensional variable
    pad = 100 - dev.coeffs['num_wavelengths']
    fill_int = (np.ones(pad) * FILL_INT).astype(np.int32)
    a_wavelengths = np.concatenate([dev.coeffs['a_wavelengths'], fill_int * np.nan])
    c_wavelengths = np.concatenate([dev.coeffs['c_wavelengths'], fill_int * np.nan])
    ac = xr.Dataset({
        'a_wavelengths': (['time', 'wavelength_number'], np.tile(a_wavelengths, (len(time), 1))),
        'a_signal_raw': (['time', 'wavelength_number'],
                         np.concatenate([np.array(data['a_signal_raw']).astype(np.int32),
                                         np.tile(fill_int, (len(time), 1))], axis=1)),
        'a_reference_raw': (['time', 'wavelength_number'],
                            np.concatenate([np.array(data['a_reference_raw']).astype(np.int32),
                                            np.tile(fill_int, (len(time), 1))], axis=1)),
        'c_wavelengths': (['time', 'wavelength_number'], np.tile(c_wavelengths, (len(time), 1))),
        'c_signal_raw': (['time', 'wavelength_number'],
                         np.concatenate([np.array(data['c_signal_raw']).astype(np.int32),
                                         np.tile(fill_int, (len(time), 1))], axis=1)),
        'c_reference_raw': (['time', 'wavelength_number'],
                            np.concatenate([np.array(data['c_reference_raw']).astype(np.int32),
                                            np.tile(fill_int, (len(time), 1))], axis=1)),
    }, coords={'time': (['time'], pd.to_datetime(time, unit='s')),
               'wavelength_number': wavelength_number})

    # setup and save the raw data
    raw = xr.merge([ds, ac])

    # update the data set with the appropriate attributes
    raw = update_dataset(raw, platform, deployment, lat, lon, [depth, depth, depth], OPTAA)
    raw['wavelength_number'].attrs['actual_wavelengths'] = data['num_wavelengths'][0]

    # save the raw data to disk
    rawfile = re.sub('.nc$', '_raw.nc', outfile)
    raw.to_netcdf(rawfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)

    # setup and save the processed data
    proc = xr.merge([ds, ac])

    # drop the first 60 seconds worth of data from the data set per vendor recommendation
    proc = proc.where(proc.elapsed_run_time / 1000 > 60, drop=True)

    # apply the device file and calculate the temperature, salinity (assuming default of 33) and scatter corrections
    proc = apply_dev(proc, dev.coeffs)
    proc = apply_tscorr(proc, dev.coeffs)
    proc = apply_scatcorr(proc, dev.coeffs)

    # remove the raw parameters, no longer needed.
    proc = proc.drop(['elapsed_run_time', 'internal_temp_raw', 'external_temp_raw', 'pressure_raw', 'a_signal_dark',
                      'a_reference_dark', 'c_signal_dark', 'c_reference_dark', 'a_signal_raw', 'a_reference_raw',
                      'c_signal_raw', 'c_reference_raw'])

    burst = proc  # make a copy of the original dataset
    burst['time'] = burst['time'].dt.round('30Min')  # reset the time values to the nearest half-hour
    burst = burst.resample(time='30Min', keep_attrs=True, skipna=True).median()  # median average the bursts
    burst['deploy_id'] = deployment  # add deployment back in as resample removes

    # update the data set with the appropriate attributes
    proc = update_dataset(burst, platform, deployment, lat, lon, [depth, depth, depth], OPTAA)
    proc['wavelength_number'].attrs['actual_wavelengths'] = data['num_wavelengths'][0]

    # save the processed data (median averaged every 30 minutes) to disk
    procfile = re.sub('.nc$', '_proc.nc', outfile)
    proc.to_netcdf(procfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
