#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_optaa
@file cgsn_processing/process/proc_optaa
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
import warnings
import xarray as xr

from gsw import SP_from_C

from cgsn_processing.process.common import Coefficients, inputs, json2obj, colocated_ctd, \
    update_dataset, ENCODING, FILL_INT
from cgsn_processing.process.configs.attr_optaa import OPTAA
from cgsn_processing.process.finding_calibrations import find_calibration

from pyseas.data.opt_functions import opt_internal_temp, opt_external_temp
from pyseas.data.opt_functions import opt_pressure, opt_pd_calc, opt_tempsal_corr


class Calibrations(Coefficients):
    def __init__(self, coeff_file, dev_file=None, hdr_url=None, tca_url=None, tcc_url=None):
        """
        Loads the OPTAA factory calibration coefficients for a unit. Values
        come from either a serialized object created per instrument and
        deployment (calibration coefficients do not change in the middle of a
        deployment), from the factory supplied device file, or from parsed CSV
        files maintained on GitHub by the OOI Data team.
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
        nbin = int(data[8].split()[0])   # going to need this value later...
        coeffs = {
            'serial_number': np.mod(int(data[1].split()[0], 16), 4096),
            'temp_calibration': float(data[3].split()[1]),
            'pressure_coeff': np.array(data[4].split()[0:2]).astype(float),
            'pathlength': float(data[6].split()[0]),
            'num_wavelengths': int(data[7].split()[0]),
            'num_temp_bins': nbin,
            'temp_bins': np.array(data[9].split()[:-3]).astype(float)
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
            cwvl.append(float(re.sub('C', '', line[0])))
            awvl.append(float(re.sub('A', '', line[1])))
            coff.append(float(line[3]))
            aoff.append(float(line[4]))
            tc_array.append(np.array(line[5:5+nbin]).astype(float))
            ta_array.append(np.array(line[nbin+5:-12]).astype(float))
            
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
                coeffs['temp_calibration'] = float(row[2])

        # serial number, stripping off all but the numbers
        coeffs['serial_number'] = int(re.sub('[^0-9]', '',  hdr.serial[0]))
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
            tc_array.append(np.array(line.split(',')).astype(float))

        tca = requests.get(tca_url)
        for line in tca.content.decode('utf-8').splitlines():
            ta_array.append(np.array(line.split(',')).astype(float))

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
        optaa['pressure'].values = np.nan * np.array(optaa.pressure_raw)
    else:
        offset = coeffs['pressure_coeff'][0]
        slope = coeffs['pressure_coeff'][1]
        optaa['pressure'] = opt_pressure(optaa['pressure_raw'], offset, slope)

    # setup inputs and create a mask index to select real wavelengths (not the pads)
    a_ref = optaa['a_reference_raw']
    a_sig = optaa['a_signal_raw']
    c_ref = optaa['c_reference_raw']
    c_sig = optaa['c_signal_raw']
    npackets = a_ref.shape[0]
    wvlngth = ~np.isnan(optaa['a_wavelengths'].values)[0, :]

    # initialize the output arrays
    apd = a_ref * np.nan
    cpd = c_ref * np.nan
    
    # calculate the L1 OPTAA data products (uncorrected beam attenuation and absorbance) for particulate
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


def apply_scatcorr(optaa, coeffs):
    """
    Correct the absorbance data for scattering using Method 1, with the
    wavelength closest to 715 nm used as the reference wavelength for the
    scattering correction.

    :param optaa: xarray dataset with the temperature and salinity corrected
        absorbance data array that will be corrected for the effects of
        scattering.
    :param coeffs: Factory calibration coefficients in a dictionary structure

    :return optaa: xarray dataset with the method 1 scatter corrected
        absorbance data array added.
    """
    # find the closest wavelength to 715 nm
    reference_wavelength = 715.0
    idx = np.argmin(np.abs(coeffs['a_wavelengths'] - reference_wavelength))

    # use that wavelength as our scatter correction wavelength
    apd_ts = optaa['apd_ts']
    apd_ts_s = apd_ts - apd_ts[:, idx]

    # save the results
    optaa['apd_ts_s'] = apd_ts_s
    return optaa


def estimate_chl_poc(optaa, coeffs):
    """
    Derive estimates of Chlorophyll-a and particulate organic carbon (POC)
    concentrations from the temperature, salinity and scatter corrected
    absorption and beam attenuation data.

    :param optaa: xarray dataset with the scatter corrected absorbance data.
    :param coeffs: Factory calibration coefficients in a dictionary structure

    :return optaa: xarray dataset with the estimates for chlorophyll and POC
        concentrations added.
    """
    # use the standard chlorophyll line height estimation with an extinction coefficient of 0.020.
    m676 = np.argmin(np.abs(coeffs['a_wavelengths'] - 676.0))
    m650 = np.argmin(np.abs(coeffs['a_wavelengths'] - 650.0))
    m715 = np.argmin(np.abs(coeffs['a_wavelengths'] - 715.0))
    apg = optaa['apd_ts_s']
    aphi = apg[:, m676] - 39/65 * apg[:, m650] - 26/65 * apg[:, m715]
    optaa['estimated_chlorophyll'] = aphi / 0.020

    # estimate the POC concentration from the attenuation at 660 nm
    m660 = np.argmin(np.abs(coeffs['c_wavelengths'] - 660.0))
    cpg = optaa['cpd_ts']
    optaa['estimated_poc'] = cpg[:, m660] * 380

    return optaa


def calculate_ratios(optaa, coeffs):
    """
    Calculate pigment ratios to use in analyzing community composition and/or
    bloom health. As these ratios are subject to the effects of biofouling it
    is expected that these values will start to become chaotic with noise
    dominating the signal. Thus these ratios can also serve as biofouling
    indicators.

    :param optaa: xarray dataset with the scatter corrected absorbance data.
    :param coeffs: Factory calibration coefficients in a dictionary structure

    :return optaa: xarray dataset with the estimates for chlorophyll and POC
        concentrations added.
    """
    apg = optaa['apd_ts_s']
    m440 = np.argmin(np.abs(coeffs['a_wavelengths'] - 440.0))
    m412 = np.argmin(np.abs(coeffs['a_wavelengths'] - 412.0))
    m490 = np.argmin(np.abs(coeffs['a_wavelengths'] - 490.0))
    m530 = np.argmin(np.abs(coeffs['a_wavelengths'] - 530.0))
    m676 = np.argmin(np.abs(coeffs['a_wavelengths'] - 676.0))

    optaa['ratio_cdom'] = apg[:, m412] / apg[:, m440]
    optaa['ratio_carotenoids'] = apg[:, m490] / apg[:, m440]
    optaa['ratio_phycobilins'] = apg[:, m530] / apg[:, m440]
    optaa['ratio_qband'] = apg[:, m676] / apg[:, m440]

    return optaa


def proc_optaa(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Main OPTAA processing function. Loads the JSON formatted parsed data and
    applies appropriate calibration coefficients to convert the raw, parsed
    data into engineering units. If no calibration coefficients are available,
    filled variables are returned and a dataset processing level attribute is
    set to "parsed".

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwargs ctd_name: Name of directory with data from a co-located CTD. This
           data will be used to apply temeprature and salinity corrections
           to the data. Otherwise, defaults are used with salinity set to
           33 psu and temperature from the OPTAAs external temperature
           sensor.
    :kwargs burst: Boolean flag to indicate whether or not to apply burst
           averaging to the data. Default is to not apply burst averaging.

    :return optaa: An xarray dataset with the processed OPTAA data
    """
    # process the variable length keyword arguments
    ctd_name = kwargs.get('ctd_name')
    burst = kwargs.get('burst')

    # load the json data file as a dictionary object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None

    # setup the instrument calibration data object
    coeff_file = os.path.join(os.path.dirname(infile), 'optaa.cal_coeffs.json')
    dev = Calibrations(coeff_file)  # initialize calibration class
    proc_flag = False

    # check for the source of calibration coeffs and load accordingly
    if os.path.isfile(coeff_file):
        # we always want to use this file if it already exists
        dev.load_coeffs()
        proc_flag = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('OPTAA', str(data['serial_number'][0]), data['time'][0])
        if csv_url:
            tca_url = re.sub('.csv', '__CC_taarray.ext', csv_url)
            tcc_url = re.sub('.csv', '__CC_tcarray.ext', csv_url)
            dev.read_devurls(csv_url, tca_url, tcc_url)
            dev.save_coeffs()
            proc_flag = True

    # check the device file coefficients against the data file contents
    if dev.coeffs['serial_number'] != data['serial_number'][0]:
        raise Exception('Serial Number mismatch between ac-s data and the device file.')
    if dev.coeffs['num_wavelengths'] != data['num_wavelengths'][0]:
        raise Exception('Number of wavelengths mismatch between ac-s data and the device file.')

    # create the time coordinate array and setup a base data frame
    optaa_time = data['time']
    df = pd.DataFrame()
    df['time'] = pd.to_datetime(optaa_time, unit='s')
    df.set_index('time', drop=True, inplace=True)

    # setup and load the 1D parsed data
    empty_data = np.atleast_1d(data['serial_number']).astype(int) * np.nan
    # raw data parsed from the data file
    df['serial_number'] = np.atleast_1d(data['serial_number']).astype(int)
    df['elapsed_run_time'] = np.atleast_1d(data['elapsed_run_time']).astype(int)
    df['internal_temp_raw'] = np.atleast_1d(data['internal_temp_raw']).astype(int)
    df['external_temp_raw'] = np.atleast_1d(data['external_temp_raw']).astype(int)
    df['pressure_raw'] = np.atleast_1d(data['pressure_raw']).astype(int)
    df['a_signal_dark'] = np.atleast_1d(data['a_signal_dark']).astype(int)
    df['a_reference_dark'] = np.atleast_1d(data['a_reference_dark']).astype(int)
    df['c_signal_dark'] = np.atleast_1d(data['c_signal_dark']).astype(int)
    df['c_reference_dark'] = np.atleast_1d(data['c_reference_dark']).astype(int)
    # processed variables to be created if a device file is available
    df['internal_temp'] = empty_data
    df['external_temp'] = empty_data
    df['pressure'] = empty_data
    df['estimated_chlorophyll'] = empty_data
    df['estimated_poc'] = empty_data
    df['ratio_cdom'] = empty_data
    df['ratio_carotenoids'] = empty_data
    df['ratio_phycobilins'] = empty_data
    df['ratio_qband'] = empty_data

    # check for data from a co-located CTD and test to see if it covers our time range of interest.
    df['ctd_pressure'] = empty_data
    df['ctd_temperature'] = empty_data
    df['ctd_salinity'] = empty_data
    temperature = None
    salinity = None
    ctd = pd.DataFrame()
    if ctd_name:
        ctd = colocated_ctd(infile, ctd_name)

    if not ctd.empty:
        # set the CTD and OPTAA time to the same units of seconds since 1970-01-01
        ctd_time = ctd.time.values.astype(float) / 10.0 ** 9

        # test to see if the CTD covers our time of interest for this optaa file
        coverage = ctd_time.min() <= min(optaa_time) and ctd_time.max() >= max(optaa_time)

        # reset initial estimates of in-situ temperature and salinity if we have full coverage
        if coverage:
            pressure = np.mean(np.interp(optaa_time, ctd_time, ctd.pressure))
            df['ctd_pressure'] = pressure

            temperature = np.mean(np.interp(optaa_time, ctd_time, ctd.temperature))
            df['ctd_temperature'] = temperature

            salinity = SP_from_C(ctd.conductivity.values * 10.0, ctd.temperature.values, ctd.pressure.values)
            salinity = np.mean(np.interp(optaa_time, ctd_time, salinity))
            df['ctd_salinity'] = salinity

    # convert the 1D data frame to an xarray dataset
    ds = xr.Dataset.from_dataframe(df)

    # create the 2D arrays from the raw a and c channel measurements using the number of wavelengths
    # padded to 100 as the dimensional array.
    wavelength_number = np.arange(100).astype(int)  # used as a dimensional variable
    num_wavelengths = np.array(data['a_signal_raw']).shape[1]
    pad = 100 - num_wavelengths
    fill_nan = np.ones(pad) * np.nan
    fill_int = (np.ones(pad) * FILL_INT).astype(int)
    a_wavelengths = np.concatenate([dev.coeffs['a_wavelengths'], fill_nan])
    c_wavelengths = np.concatenate([dev.coeffs['c_wavelengths'], fill_nan])
    empty_data = np.concatenate([np.array(data['a_signal_raw']).astype(int),
                                 np.tile(fill_nan, (len(optaa_time), 1))], axis=1) * np.nan
    ac = xr.Dataset({
        # raw data parsed from the data file
        'a_wavelengths': (['time', 'wavelength_number'], np.tile(a_wavelengths, (len(optaa_time), 1))),
        'a_signal_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['a_signal_raw']).astype(int),
                         np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'a_reference_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['a_reference_raw']).astype(int),
                            np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'c_wavelengths': (['time', 'wavelength_number'], np.tile(c_wavelengths, (len(optaa_time), 1))),
        'c_signal_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['c_signal_raw']).astype(int),
                         np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        'c_reference_raw': (['time', 'wavelength_number'], np.concatenate([np.array(data['c_reference_raw']).astype(int),
                            np.tile(fill_int, (len(optaa_time), 1))], axis=1)),
        # processed variables to be created if a device file is available
        'apd': (['time', 'wavelength_number'], empty_data),
        'apd_ts': (['time', 'wavelength_number'], empty_data),
        'apd_ts_s': (['time', 'wavelength_number'], empty_data),
        'cpd': (['time', 'wavelength_number'], empty_data),
        'cpd_ts': (['time', 'wavelength_number'], empty_data)
    }, coords={'time': (['time'], pd.to_datetime(optaa_time, unit='s')),
               'wavelength_number': wavelength_number})

    # combine the 1D and 2D datasets into a single xarray dataset
    optaa = xr.merge([ds, ac])

    # drop the first 60 seconds worth of data from the data set per vendor recommendation
    optaa.elapsed_run_time.values = optaa.elapsed_run_time.where(optaa.elapsed_run_time / 1000 > 60)
    optaa = optaa.dropna(dim='time', subset=['elapsed_run_time'])

    # apply a median average to the burst (if desired) and add the deployment ID
    if burst:
        # suppress warnings for now. In the first case, changes suggested cause a ValueError and the second
        # warning is expected given we are averaging before calculating some of the values
        warnings.filterwarnings(action='ignore', category=FutureWarning)
        warnings.filterwarnings(action='ignore', message='All-NaN slice encountered')

        # resample to a 15 minute interval and shift the clock to make sure we capture the time "correctly"
        optaa = optaa.resample(time='15Min', base=55, loffset='5Min').median(dim='time', keep_attrs=True)
        optaa['deploy_id'] = xr.Variable('time', np.atleast_1d(deployment).astype(str))
    else:
        optaa['deploy_id'] = xr.Variable('time', np.tile(deployment, len(optaa.time)).astype(str))

    # if there is calibration data, apply it now
    if proc_flag:
        # apply the device file and the temperature, salinity and scatter corrections
        optaa = apply_dev(optaa, dev.coeffs)
        optaa = apply_tscorr(optaa, dev.coeffs, temperature, salinity)
        optaa = apply_scatcorr(optaa, dev.coeffs)

        # estimate chlorophyll-a and POC concentrations from the absorption and attenuation data, respectively.
        optaa = estimate_chl_poc(optaa, dev.coeffs)

        # calculate pigment and CDOM ratios to provide variables useful in characterizing the community structure and
        # the status of the sensor itself (biofouling tracking).
        optaa = calculate_ratios(optaa, dev.coeffs)

    # update the data set with the appropriate attributes
    optaa = update_dataset(optaa, platform, deployment, lat, lon, [depth, depth, depth], OPTAA)
    optaa['wavelength_number'].attrs['actual_wavelengths'] = np.intc(num_wavelengths)

    # if we used burst averaging, reset fill values and attributes for the raw a and c signal and reference values
    int_arrays = ['a_signal_raw', 'a_reference_raw', 'c_signal_raw', 'c_reference_raw']
    if burst:
        for k in optaa.variables:
            if k in int_arrays:
                optaa[k].attrs['_FillValue'] = np.nan
                optaa[k] = optaa[k].where(optaa[k] > -1000)

    if proc_flag:
        optaa.attrs['processing_level'] = 'processed'
    else:
        optaa.attrs['processing_level'] = 'parsed'

    # return the final processed dataset
    return optaa


def main(argv=None):
    """
    Command line function to process the OPTAA data using the proc_optaa
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
    ctd_name = args.devfile  # name of co-located CTD
    burst = args.burst

    # process the OPTAA data and save the results to disk
    optaa = proc_optaa(infile, platform, deployment, lat, lon, depth, ctd_name=ctd_name, burst=burst)
    if optaa:
        optaa.to_netcdf(outfile, mode='w', format='NETCDF4', engine='netcdf4', encoding=ENCODING)


if __name__ == '__main__':
    main()
