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
import scipy.interpolate as sci

from cgsn_processing.process.common import Coefficients, inputs, json2df
from ion_functions.data.opt_functions import opt_internal_temp, opt_external_temp
from ion_functions.data.opt_functions import opt_pressure, opt_pd_calc, opt_tempsal_corr


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
        with open(dev_file, 'rb') as f:
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
        coeffs['serial_number'] = np.int(re.sub('[^0-9]','', hdr.serial[0]))
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
        for line in tcc.content.splitlines():
            tc_array.append(np.array(line.split(',')).astype(np.float))

        tca = requests.get(tca_url)
        for line in tca.content.splitlines():
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
    optaa['internal_temp'] = opt_internal_temp(optaa['internal_temp_raw'].values)
    optaa['external_temp'] = opt_external_temp(optaa['external_temp_raw'].values)

    # calculate pressure, if sensor is equipped
    if np.all(coeffs['pressure_coeff'] == 0):
        # do not use None, which will cause sio.savemat to croak.
        optaa['pressure'] = np.NaN * np.array(optaa.pressure_raw)
    else:
        offset = coeffs['pressure_coeff'][0]
        slope = coeffs['pressure_coeff'][1]
        optaa['pressure'] = opt_pressure(optaa['pressure_raw'].values, offset, slope)
    
    # calculate the L1 OPTAA data products (uncorrected beam attenuation and absorbance) for particulates
    # and dissolved organic matter with clear water removed.
    a_ref = np.array(np.vstack(optaa['a_reference_raw'].values), dtype='int32')
    a_sig = np.array(np.vstack(optaa['a_signal_raw'].values), dtype='int32')
    c_ref = np.array(np.vstack(optaa['c_reference_raw'].values), dtype='int32')
    c_sig = np.array(np.vstack(optaa['c_signal_raw'].values), dtype='int32')
    
    # size up inputs
    npackets = a_ref.shape[0]
    nwavelengths = a_ref.shape[1]
    # initialize the output arrays
    apd = np.zeros([npackets, nwavelengths])
    cpd = np.zeros([npackets, nwavelengths])
    
    for ii in range(npackets):
        # calculate the uncorrected optical absorption coefficient [m^-1]
        apd[ii, :], _ = opt_pd_calc(a_ref[ii, :], a_sig[ii, :], coeffs['a_offsets'], 
            temp[ii], coeffs['temp_bins'], coeffs['ta_array'])
        # calculate the uncorrected optical attenuation coefficient [m^-1]
        cpd[ii, :], _ = opt_pd_calc(c_ref[ii, :], c_sig[ii, :], coeffs['c_offsets'], 
            temp[ii], coeffs['temp_bins'], coeffs['tc_array'])
    
    # save the results back to the dictionary and add the beam attenuation and absorbance wavelengths to the data.
    optaa['apd'] = apd.tolist()
    optaa['cpd'] = cpd.tolist()
    optaa['a_wavelengths'] = (np.tile(coeffs['a_wavelengths'], (npackets, 1))).tolist()
    optaa['c_wavelengths'] = (np.tile(coeffs['c_wavelengths'], (npackets, 1))).tolist()

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
    scalar, or a 1D array or row or column vector with the same number of time
    points as 'a' and 'c'.
    """
    # setup the temperature and salinity arrays
    if temp is None:
        temp = optaa['external_temp'].values
    else: 
        if np.array(temp).size == 1:
            temp = np.ones(np.size(optaa['time'])) * temp
        else:
            temp = np.array(temp)
    
    if temp.size != np.size(optaa['time']):
        raise Exception("Mismatch: temperature array != number of OPTAA measurements")

    if salinity is None:
        salinity = np.ones(np.size(optaa['time'])) * 33.0
    else:
        if np.array(salinity).size == 1:
            salinity = np.ones(np.size(optaa['time'])) * salinity
        else:
            salinity = np.array(salinity)

    if salinity.size != np.size(optaa['time']):
        raise Exception("Mismatch: salinity array != number of OPTAA measurements")

    # setup and size the inputs
    apd = np.array(np.vstack(optaa['apd'].values), dtype='float')
    cpd = np.array(np.vstack(optaa['cpd'].values), dtype='float')
    npackets = apd.shape[0]
    nwavelengths = apd.shape[1]

    # initialize the output arrays
    apd_ts = np.zeros([npackets, nwavelengths])
    cpd_ts = np.zeros([npackets, nwavelengths])

    # apply the temperature and salinity corrections
    for ii in range(npackets):
        apd_ts[ii, :] = opt_tempsal_corr('a', apd[ii, :], coeffs['a_wavelengths'], 
            coeffs['temp_calibration'], temp[ii], salinity[ii])
        cpd_ts[ii, :] = opt_tempsal_corr('c', cpd[ii, :], coeffs['c_wavelengths'], 
            coeffs['temp_calibration'], temp[ii], salinity[ii])
    
    # save the results
    optaa['apd_ts'] = apd_ts.tolist()
    optaa['cpd_ts'] = cpd_ts.tolist()

    return optaa


def apply_scatcorr(optaa, coeffs, method=1):
    """
    Correct the absorbance data for scattering using Method 1 (the default), with 715 nm used as the scattering
    wavelength.
    """
    if method != 1:
        raise Exception('Only scatter method = 1 is coded for the time being.')

    reference_wavelength = 715.0

    # find the closest wavelength to the reference wavelength
    idx = np.argmin(np.abs(coeffs['a_wavelengths'] - reference_wavelength))

    # use that wavelength as our scatter correction wavelength
    apd_ts = np.array(np.vstack(optaa['apd_ts'].values), dtype='float')
    scatter = apd_ts[:, idx]
    apd_ts_s = apd_ts - scatter[:, None]

    # save the results
    optaa['apd_ts_s'] = apd_ts_s.tolist()
    return optaa


def main():
    # load the input arguments
    args = inputs()
    infile = os.path.abspath(args.infile)
    outpath, outfile = os.path.split(args.outfile)
    platform = args.platform
    deployment = args.deployment
    lat = args.latitude
    lng = args.longitude
    depth = np.float(args.switch)  # utilize the switch option to set the deployment depth

    coeff_file = os.path.abspath(args.coeff_file)
    dev = Calibrations(coeff_file)  # initialize calibration class
    
    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        dev.load_coeffs()
    elif args.devfile:
        # load from the factory supplied device file
        devfile = os.path.abspath(args.devfile)
        dev.read_devfile(devfile)
        dev.save_coeffs()
    elif args.csvurl:
        # load from the CI hosted CSV files
        hdr_url = args.csvurl
        tca_url = re.sub('.csv', '__CC_taarray.ext', hdr_url)
        tcc_url = re.sub('.csv', '__CC_tcarray.ext', hdr_url)
        dev.read_devurls(hdr_url, tca_url, tcc_url)
        dev.save_coeffs()
    else:
        raise Exception('A source for the OPTAA calibration coefficients could not be found')
    
    # load the json data file and return a panda dataframe
    df = json2df(infile)
    if df.empty:
        # This is an empty file, end processing
        return None

    df['depth'] = depth
    df['deploy_id'] = deployment

    # check the device file coefficients against the data file contents
    if dev.coeffs['serial_number'] != df.serial_number[0]:
        raise Exception('Serial Number mismatch between ac-s data and the device file.')
    if dev.coeffs['num_wavelengths'] != df.num_wavelengths[0]:
        raise Exception('Number of wavelengths mismatch between ac-s data and the device file.')

    # there is some monkey business imposed by having to go from json and list
    # formatting to numpy arrays and back to lists. There may be better ways of
    # doing this...
    df = apply_dev(df, dev.coeffs)
    df = apply_tscorr(df, dev.coeffs)
    df = apply_scatcorr(df, dev.coeffs)

if __name__ == '__main__':
    main()
