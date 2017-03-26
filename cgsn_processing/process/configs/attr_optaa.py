#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_optaa
@file cgsn_processing/process/configs/attr_optaa.py
@author Christopher Wingard
@brief Attributes for the OPTAA variables
"""
import numpy as np

OPTAA = {
    'deploy_id': {
        'long_name': 'Deployment ID',
        'standard_name': 'deployment_id',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'serial_number': {
        'long_name': 'Unit Serial Number',
        'standard_name': 'serial_number',
        'units': '1',
    },
    'a_reference_dark': {
        'long_name': 'A Channel Dark Reference',
        'standard_name': 'a_reference_dark',
        'units': 'counts',
    },
    'pressure_raw': {
        'long_name': 'Raw Pressure',
        'standard_name': 'pressure_raw',
        'units': 'counts',
    },
    'pressure': {
        'long_name': 'Pressure',
        'standard_name': 'pressure_raw',
        'units': 'dbar',
    },
    'a_signal_dark': {
        'long_name': 'A Channel Dark Signal',
        'standard_name': 'a_signal_dark',
        'units': 'counts',
    },
    'external_temp_raw': {
        'long_name': 'Raw External Temperature',
        'standard_name': 'external_temperature_raw',
        'units': 'counts',
    },
    'external_temp': {
        'long_name': 'In-Situ Temperature',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celsius',
    },
    'internal_temp_raw': {
        'long_name': 'Raw Internal Temperature',
        'standard_name': 'internal_temperature_raw',
        'units': 'counts',
    },
    'internal_temp': {
        'long_name': 'Instrument Temperature',
        'standard_name': 'instrument_temperature',
        'units': 'degree_Celsius',
    },
    'c_reference_dark': {
        'long_name': 'C Channel Dark Reference',
        'standard_name': 'c_reference_dark',
        'units': 'counts',
    },
    'c_signal_dark': {
        'long_name': 'C Channel Dark Signal',
        'standard_name': 'c_signal_dark',
        'units': 'counts',
    },
    'elapsed_run_time': {
        'long_name': 'Elapsed Run Time',
        'standard_name': 'elapsed_run_time',
        'units': 'ms',
    },
    'num_wavelengths': {
        'long_name': 'Number of Wavelengths',
        'standard_name': 'number_wavelengths',
        'units': '1',
    },
    'a_wavelengths': {
        'long_name': 'A Channel Wavelengths',
        'standard_name': 'a_wavelengths',
        'units': 'nm',
        'fill_value': -999999999.
    },
    'c_wavelengths': {
        'long_name': 'c Channel Wavelengths',
        'standard_name': 'c_wavelengths',
        'units': 'nm',
        'fill_value': -999999999.
    },
    'c_reference_raw': {
        'long_name': 'C Channel Raw Reference',
        'standard_name': 'c_reference_raw',
        'units': 'counts',
        'fill_value': np.int32(-999999999),
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'a_reference_raw': {
        'long_name': 'A Channel Raw Reference',
        'standard_name': 'a_reference_raw',
        'units': 'counts',
        'fill_value': np.int32(-999999999),
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'c_signal_raw': {
        'long_name': 'C Channel Raw Signal',
        'standard_name': 'c_signal_raw',
        'units': 'counts',
        'fill_value': np.int32(-999999999),
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'a_signal_raw': {
        'long_name': 'A Channel Raw Signal',
        'standard_name': 'a_signal_raw',
        'units': 'counts',
        'fill_value': np.int32(-999999999),
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'apd': {
        'long_name': 'Particulate and Dissolved Absorbance',
        'standard_name': 'particulate_dissolved_absorbance',
        'units': 'm-1',
        'fill_value': -999999999.,
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'apd_ts': {
        'long_name': 'Particulate and Dissolved Absorbance with TS Correction',
        'standard_name': 'particulate_dissolved_absorbance_ts',
        'units': 'm-1',
        'fill_value': -999999999.,
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'apd_ts_s': {
        'long_name': 'Particulate and Dissolved Absorbance with TS and Scatter Correction',
        'standard_name': 'particulate_dissolved_absorbance_ts_scat',
        'units': 'm-1',
        'fill_value': -999999999.,
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'cpd': {
        'long_name': 'Particulate and Dissolved Attenuation',
        'standard_name': 'particulate_dissolved_attenuation',
        'units': 'm-1',
        'fill_value': -999999999.,
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'cpd_ts': {
        'long_name': 'Particulate and Dissolved Attenuation with TS Correction',
        'standard_name': 'particulate_dissolved_attenuation_ts',
        'units': 'm-1',
        'fill_value': -999999999.,
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    }
}
