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

from pyaxiom.netcdf.sensors import TimeSeries

from cgsn_processing.process.common import Coefficients, inputs, json2df
from cgsn_processing.process.configs.attr_optaa import OPTAA

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
    optaa['internal_temp'] = opt_internal_temp(optaa['internal_temp_raw'].values)
    optaa['external_temp'] = opt_external_temp(optaa['external_temp_raw'].values)

    # calculate pressure, if sensor is equipped
    if np.all(coeffs['pressure_coeff'] == 0):
        # no pressure sensor, ignoring.
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
        apd[ii, :], _ = opt_pd_calc(a_ref[ii, :], a_sig[ii, :], coeffs['a_offsets'], optaa['internal_temp'].values[ii],
                                    coeffs['temp_bins'], coeffs['ta_array'])
        # calculate the uncorrected optical attenuation coefficient [m^-1]
        cpd[ii, :], _ = opt_pd_calc(c_ref[ii, :], c_sig[ii, :], coeffs['c_offsets'], optaa['internal_temp'].values[ii],
                                    coeffs['temp_bins'], coeffs['tc_array'])
    
    # save the results back to the dictionary and add the beam attenuation and absorbance wavelengths to the data.
    optaa['apd'] = apd.tolist()
    optaa['cpd'] = cpd.tolist()

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

    # apply the device file and calculate the temperature, salinity and scatter corrections
    df = apply_dev(df, dev.coeffs)
    df = apply_tscorr(df, dev.coeffs)
    df = apply_scatcorr(df, dev.coeffs)

    # Setup the global attributes for the NetCDF file and create the NetCDF TimeSeries object
    global_attributes = {
        'title': 'Optical Absorbance and Attenuation from OPTAA',
        'summary': (
            'Measures the absorabance and attenuation of particulate and dissolved matter from the WET Labs AC-S.'
        ),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
        'comment': 'Mooring ID: {}-{}'.format(platform.upper(), re.sub('\D', '', deployment))
    }
    ts = TimeSeries(
        output_directory=outpath,
        latitude=lat,
        longitude=lng,
        station_name=platform,
        global_attributes=global_attributes,
        times=df.time.values.astype(np.int64) * 10**-9,
        verticals=df.depth.values,
        output_filename=outfile,
        vertical_positive='down')

    nc = ts._nc     # create a netCDF4 object from the TimeSeries object

    # create a new dimension for the wavelength array, padded out to a size of 100 to account for the variable number
    # of wavelengths and then create arrays for the the 'a' and 'c'-channel wavelengths
    nc.createDimension('a_wavelengths', size=100)
    nc.createDimension('c_wavelengths', size=100)
    npad = 100 - dev.coeffs['num_wavelengths']
    fill = np.ones(npad) * -999999999.

    d = nc.createVariable('a_wavelengths', 'f', ('a_wavelengths',))
    d.setncatts(OPTAA['a_wavelengths'])
    d[:] = np.concatenate((dev.coeffs['a_wavelengths'], fill)).tolist()
    d = nc.createVariable('c_wavelengths', 'f', ('c_wavelengths',))
    d.setncatts(OPTAA['c_wavelengths'])
    d[:] = np.concatenate((dev.coeffs['c_wavelengths'], fill)).tolist()

    # add the data from the data frame and set the attributes
    for c in df.columns:
        # skip the coordinate variables, if present, already added above via TimeSeries
        if c in ['time', 'lat', 'lon', 'depth']:
            # print("Skipping axis '{}' (already in file)".format(c))
            continue

        # create the netCDF.Variable object for the date/time string
        if c == 'dcl_date_time_string':
            d = nc.createVariable(c, 'S23', ('time',))
            d.setncatts(OPTAA[c])
            d[:] = df[c].values
        elif c == 'deploy_id':
            d = nc.createVariable(c, 'S6', ('time',))
            d.setncatts(OPTAA[c])
            d[:] = df[c].values
        elif c in ['apd', 'apd_ts', 'apd_ts_s', 'cpd', 'cpd_ts',
                   'a_signal_raw', 'a_reference_raw',
                   'c_signal_raw', 'c_reference_raw']:
            # first determine the data type and create accordingly
            if c in ['a_signal_raw', 'a_reference_raw']:
                d = nc.createVariable(c, 'i4', ('time', 'a_wavelengths',))
                data = np.array(np.vstack(df[c].values), dtype='int32')
            elif c in ['c_signal_raw', 'c_reference_raw']:
                d = nc.createVariable(c, 'i4', ('time', 'c_wavelengths',))
                data = np.array(np.vstack(df[c].values), dtype='int32')
            elif c in ['apd', 'apd_ts', 'apd_ts_s']:
                d = nc.createVariable(c, 'f', ('time', 'a_wavelengths',))
                data = np.array(np.vstack(df[c].values), dtype='float32')
            else:
                d = nc.createVariable(c, 'f', ('time', 'c_wavelengths',))
                data = np.array(np.vstack(df[c].values), dtype='float32')
            # and now assign the data, padding out to 100 wavelengths
            d.setncatts(OPTAA[c])
            d[:] = np.concatenate((data, np.tile(fill, (len(df.time), 1))), axis=1)
        else:
            # use the TimeSeries object to add the remaining variables
            ts.add_variable(c, df[c].values, fillvalue=-999999999, attributes=OPTAA[c])

    # synchronize the data with the netCDF file and close it
    nc.sync()
    nc.close()

if __name__ == '__main__':
    main()
