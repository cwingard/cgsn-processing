#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.proc_mmp
@file cgsn_processing/process/proc_mmp_coastal.py
@author Joe Futrelle
@brief Creates a NetCDF dataset for the MMP from JSON formatted source data
"""
import numpy as np
import os
import pandas as pd
import xarray as xr

from gsw import z_from_p, SP_from_C, SA_from_SP, CT_from_t, rho

from cgsn_processing.process.common import inputs, json2obj, json_obj2df, Coefficients, update_dataset, \
    ENCODING, dict_update, FILL_INT
from cgsn_processing.process.finding_calibrations import find_calibration
from cgsn_processing.process.configs.attr_mmp import MMP, MMP_ADATA, MMP_CDATA, MMP_EDATA
from cgsn_processing.process.configs.attr_common import SHARED
from cgsn_processing.process.proc_flort import Calibrations as FLR_Calibrations

from pyseas.data.do2_functions import do2_raw_to_doxy
from pyseas.data.flo_functions import flo_scale_and_offset, flo_bback_total
from pyseas.data.opt_functions import opt_par_biospherical_wfp
from pyseas.data.vel_functions import vel3dk_transform
from pyseas.data.generic_functions import magnetic_declination, magnetic_correction


class OXY_Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the DOFST-K factory calibration coefficients for a unit. Values
        come from either a serialized object created per instrument and
        deployment (calibration coefficients do not change in the middle of a
        deployment), or from parsed CSV files maintained on GitHub by the OOI
        Data teams.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from a Sea-Bird 43F DO sensor (aka DOFST) device file
        already parsed and stored on GitHub as a CSV files. Note, the
        formatting of these files puts some constraints on this process. If
        someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            if row[1] == 'CC_frequency_offset':
                coeffs['offset'] = row[2]
            if row[1] == 'CC_oxygen_signal_slope':
                coeffs['slope'] = row[2]
            if row[1] == 'CC_residual_temperature_correction_factor_a':
                coeffs['A'] = row[2]
            if row[1] == 'CC_residual_temperature_correction_factor_b':
                coeffs['B'] = row[2]
            if row[1] == 'CC_residual_temperature_correction_factor_c':
                coeffs['C'] = row[2]
            if row[1] == 'CC_residual_temperature_correction_factor_e':
                coeffs['E'] = row[2]

        # save the resulting dictionary
        self.coeffs = coeffs


class PAR_Calibrations(Coefficients):
    def __init__(self, coeff_file, csv_url=None):
        """
        Loads the PARAD-K factory calibration coefficients for a unit. Values
        come from either a serialized object created per instrument and
        deployment (calibration coefficients do not change in the middle of a
        deployment), or from parsed CSV files maintained on GitHub by the OOI
        Data teams.
        """
        # assign the inputs
        Coefficients.__init__(self, coeff_file)
        self.csv_url = csv_url

    def read_csv(self, csv_url):
        """
        Reads the values from a BioSpherical PAR sensor (aka PARAD) device file
        already parsed and stored on GitHub as a CSV files. Note, the
        formatting of these files puts some constraints on this process. If
        someone has a cleaner method, I'm all in favor...
        """
        # create the device file dictionary and assign values
        coeffs = {}

        # read in the calibration data
        cal = pd.read_csv(csv_url, usecols=[0, 1, 2])
        for idx, row in cal.iterrows():
            # scale and offset correction factors
            if row[1] == 'CC_dark_offset':
                coeffs['dark_offset'] = row[2]
            if row[1] == 'CC_scale_wet':
                coeffs['scale_wet'] = row[2]

        # save the resulting dictionary
        self.coeffs = coeffs


def proc_mmp_coastal(infile, platform, deployment, lat, lon, depth, **kwargs):
    """
    Processing function for a Coastal MMP with CTDPF, DOFST, FLORT, PARAD,
    and VEL3D sensors attached. Loads the JSON formatted parsed data file and
    extracts and processes the three different file types covering the five
    instruments ("A" = VEL3D, "C" = CTDPF and DOFST, and "E" = FLORT and
    PARAD). Appropriate calibration coefficients, to convert the raw data
    into engineering units, are applied. If no calibration coefficients are
    available, filled variables are returned and the dataset processing level
    attributes are set to "parsed". Otherwise, the dataset processing level is
    set to "partial" or "processed" depending on whether all the needed data is
    available to convert the raw data.

    :param infile: JSON formatted parsed data file
    :param platform: Name of the mooring the instrument is mounted on.
    :param deployment: Name of the deployment for the input data file.
    :param lat: Latitude of the mooring deployment.
    :param lon: Longitude of the mooring deployment.
    :param depth: Depth of the platform the instrument is mounted on.

    :kwarg flr_serial: The serial number of the attached FLORT (optional input)
    :kwarg oxy_serial: The serial number of the attached DOFST (optional input)
    :kwarg par_serial: The serial number of the attached PARAD (optional input)

    :return edata: An xarray dataset with the processed "E" file data, which
        includes the MMP engineering, FLORT and PARAD data
    :return cdata: An xarray dataset with the processed "C" file data, which
        includes the CTDPF and DOFST data
    :return adata: An xarray dataset with the processed "A" file data, which
        consists of the VEL3D data
    """
    # process the variable length keyword arguments
    flr_serial = kwargs.get('flr_serial')
    oxy_serial = kwargs.get('oxy_serial')
    par_serial = kwargs.get('par_serial')

    # load the data file as a json formatted object for further processing
    data = json2obj(infile)
    if not data:
        # json data file was empty, exiting
        return None, None, None

    # extract the profiler data from the 3 original source files
    edata = json_obj2df(data, 'edata')
    cdata = json_obj2df(data, 'cdata')
    adata = json_obj2df(data, 'adata')

    # pull out some profile status information
    profile_id = data['profile']['profile_id']
    ramp_status = data['profile']['ramp_status']
    profile_status = data['profile']['profile_status']
    start_depth = data['profile']['start_depth']
    end_depth = data['profile']['end_depth']

    # redefine the site depth to a list including the min/max depth of the profile
    if start_depth > end_depth:
        depth = [depth, end_depth, start_depth]
    else:
        depth = [depth, start_depth, end_depth]

    # --- process the data from each source: EDATA --- #
    # calculate the depth from the pressure record (convert 0.00 pressure fills to NaN)
    edata['pressure'] = [m if m > 1 else np.nan for m in edata['pressure']]
    edata['profiler_depth'] = z_from_p(edata['pressure'], lat)

    # drop the date_time_string
    edata.drop(columns=['date_time_string'], inplace=True)

    # rename some raw parameters for consistency with other datasets
    data.rename(columns={'raw_chl': 'raw_chlorophyll', 'raw_scatter': 'raw_backscatter'}, inplace=True)

    # create empty variables for the processed FLORT and PAR data (will fill in with processed data if available)
    empty_data = np.atleast_1d(edata['time']).astype(np.int32) * np.nan
    edata['estimated_chlorophyll'] = empty_data
    edata['fluorometric_cdom'] = empty_data
    edata['beta_700'] = empty_data
    edata['total_optical_backscatter'] = empty_data
    edata['irradiance'] = empty_data
    proc_flort = False
    proc_parad = False

    # now grab the calibration coefficients for the FLORT (if they exist)
    coeff_file = os.path.join(os.path.dirname(infile), 'flort.cal_coeffs.json')
    flr = FLR_Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        flr.load_coeffs()
        proc_flort = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('FLORT', flr_serial, (edata.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            flr.read_csv(csv_url)
            flr.save_coeffs()
            proc_flort = True

    # if calibration coefficients are available, process the FLORT data (scale and offset)
    if proc_flort:
        edata['estimated_chlorophyll'] = flo_scale_and_offset(edata['raw_chlorophyll'], flr.coeffs['dark_chla'],
                                                              flr.coeffs['scale_chla'])
        edata['fluorometric_cdom'] = flo_scale_and_offset(edata['raw_cdom'], flr.coeffs['dark_cdom'],
                                                          flr.coeffs['scale_cdom'])
        edata['beta_700'] = flo_scale_and_offset(edata['raw_backscatter'], flr.coeffs['dark_beta'],
                                                 flr.coeffs['scale_beta'])

    # now grab the calibration coefficients for the PARAD (if they exist)
    coeff_file = os.path.join(os.path.dirname(infile), 'parad.cal_coeffs.json')
    par = PAR_Calibrations(coeff_file)  # initialize calibration class
    if os.path.isfile(coeff_file):
        # we always want to use this file if it exists
        par.load_coeffs()
        proc_parad = True
    else:
        # load from the CI hosted CSV files
        csv_url = find_calibration('PARAD', par_serial, (edata.time.values.astype('int64') * 10 ** -9)[0])
        if csv_url:
            par.read_csv(csv_url)
            par.save_coeffs()
            proc_parad = True

    if proc_parad:
        edata['irradiance'] = opt_par_biospherical_wfp(edata['raw_par'], par.coeffs['dark_offset'],
                                                       par.coeffs['scale_wet'])

    edata['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(edata.time)).astype(str))
    edata['profile_id'] = xr.Variable(('time',), np.repeat(profile_id, len(edata.time)).astype(str))
    attrs = dict_update(MMP, MMP_EDATA)  # combine the common and dataframe specific attributes
    attrs = dict_update(attrs, SHARED)  # add the shared the attributes
    edata = update_dataset(edata, platform, deployment, lat, lon, depth, attrs)
    if (proc_flort and not proc_parad) or (proc_parad and not proc_flort):
        edata.attrs['processing_level'] = 'partial'
    elif proc_flort and proc_parad:
        edata.attrs['processing_level'] = 'processed'
    else:
        edata.attrs['processing_level'] = 'parsed'

    # --- process the data from each source: CDATA --- #
    if cdata.empty is False:
        # calculate the depth from the pressure record
        cdata['profiler_depth'] = z_from_p(cdata['pressure'], lat)

        # calculate the practical salinity of the seawater from the temperature and conductivity measurements
        cdata['salinity'] = SP_from_C(cdata['conductivity'], cdata['temperature'], cdata['pressure'])

        # calculate the in-situ density of the seawater from the absolute salinity and conservative temperature
        sa = SA_from_SP(cdata['salinity'].values, cdata['pressure'].values, lon, lat)  # absolute salinity
        ct = CT_from_t(sa, cdata['temperature'].values, cdata['pressure'].values)  # conservative temperature
        cdata['density'] = rho(sa, ct, cdata['pressure'])  # density

        # interpolate the temperature and salinity records into the edata and then calculate the total optical
        # backscatter coefficient
        degc = np.interp(edata['time'], cdata['time'], cdata['temperature'])
        psu = np.interp(edata['time'], cdata['time'], cdata['salinity'])
        edata['total_optical_backscatter'] = flo_bback_total(edata['beta_700'], degc, psu, flr.coeffs['scatter_angle'],
                                                             flr.coeffs['wavelength'], flr.coeffs['chi_factor'])

        # create empty variables for the processed oxygen data (will fill in with processed data if available)
        empty_data = np.atleast_1d(cdata['time']).astype(np.int32) * np.nan
        cdata['oxygen_concentration'] = empty_data
        cdata['oxygen_concentration_corrected'] = empty_data
        proc_dofst = False

        # now grab the calibration coefficients for the DOFST (if they exist)
        coeff_file = os.path.join(os.path.dirname(infile), 'dofst.cal_coeffs.json')
        oxy = PAR_Calibrations(coeff_file)  # initialize calibration class
        if os.path.isfile(coeff_file):
            # we always want to use this file if it exists
            oxy.load_coeffs()
            proc_dofst = True
        else:
            # load from the CI hosted CSV files
            csv_url = find_calibration('DOFST', oxy_serial, (edata.time.values.astype('int64') * 10 ** -9)[0])
            if csv_url:
                oxy.read_csv(csv_url)
                oxy.save_coeffs()
                proc_dofst = True

        if proc_dofst:
            doxy, doxy_corr = do2_raw_to_doxy(cdata['raw_oxygen'], oxy.coeffs['offset'], oxy.coeffs['slope'],
                                              oxy.coeffs['A'], oxy.coeffs['B'], oxy.coeffs['C'], oxy.coeffs['E'],
                                              cdata['pressure'], cdata['temperature'], cdata['salinity'], lat, lon)
            cdata['oxygen_concentration'] = doxy
            cdata['oxygen_concentration_corrected'] = doxy_corr

        cdata['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(cdata.time)).astype(str))
        cdata['profile_id'] = xr.Variable(('time',), np.repeat(profile_id, len(cdata.time)).astype(str))
        attrs = dict_update(MMP, MMP_CDATA)  # combine the common and dataframe specific attributes
        attrs = dict_update(attrs, SHARED)  # add the shared the attributes
        cdata = update_dataset(cdata, platform, deployment, lat, lon, depth, attrs)
        if proc_dofst:
            cdata.attrs['processing_level'] = 'processed'
        else:
            cdata.attrs['processing_level'] = 'parsed'
    else:
        cdata = None

    # --- process the data from each source: ADATA --- #
    if adata.empty is False:
        # create a depth record from the CTD data
        adata['profiler_depth'] = np.interp(adata['time'], cdata['time'], cdata['profiler_depth'])

        # drop the date_time_string
        adata.drop(columns=['date_time_string'], inplace=True)

        # reorder the beams list array, so it works with the transform function (drop the number of beams and add
        # a fill-value for the 5th beam (which does not actually exist)
        beams = np.atleast_2d(adata['beams'])
        beams = np.insert(np.delete(beams, 0, 1), 4, FILL_INT, 1)

        # convert the raw, beam velocity measurements to ENU velocities, corrected for magnetic declination, in m/s
        ENU = vel3dk_transform(adata['beam_0_velocity'], adata['beam_1_velocity'], adata['beam_2_velocity'],
                               adata['heading'], adata['pitch'], adata['roll'], beams)

        # separate out the components from the Earth coordinate transformed data matrix.
        u = np.array(ENU[0, :])[0]
        v = np.array(ENU[1, :])[0]
        adata['vertical_relative_velocity'] = np.array(ENU[2, :])[0]

        # correct for magnetic declination
        theta = magnetic_declination(lat, lon, adata['time'], adata['profiler_depth'])
        u_cor, v_cor = magnetic_correction(theta, u, v)

        # add the corrected velocities to the dataframe
        adata['eastward_relative_velocity'] = u_cor
        adata['northward_relative_velocity'] = v_cor

        adata['deploy_id'] = xr.Variable(('time',), np.repeat(deployment, len(adata.time)).astype(str))
        adata['profile_id'] = xr.Variable(('time',), np.repeat(profile_id, len(adata.time)).astype(str))
        attrs = dict_update(MMP, MMP_ADATA)  # combine the common and dataframe specific attributes
        attrs = dict_update(attrs, SHARED)  # add the shared the attributes
        adata = update_dataset(adata, platform, deployment, lat, lon, depth, attrs)
        adata.attrs['processing_level'] = 'processed'
    else:
        adata = None

    return edata, cdata, adata


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

    # instrument serial numbers
    flr_serial = args.devfile
    par_serial = args.devfile
    oxy_serial = args.devfile

    # process the CTDBP data and save the results to disk
    edata, cdata, adata = proc_mmp_coastal(infile, platform, deployment, lat, lon, depth,
                                           flr_serial=flr_serial, par_serial=par_serial, oxy_serial=oxy_serial)

    base = os.path.splitext(outfile)[0]
    if edata:
        efile = os.rename(outfile, base + '_edata.nc')
        edata.to_netcdf(efile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)

    if cdata:
        cfile = os.rename(outfile, base + '_cdata.nc')
        cdata.to_netcdf(cfile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)

    if adata:
        afile = os.rename(outfile, base + '_adata.nc')
        adata.to_netcdf(afile, mode='w', format='NETCDF4', engine='h5netcdf', encoding=ENCODING)

if __name__ == '__main__':
    main()
