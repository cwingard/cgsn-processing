#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_optaa
@file cgsn_processing/process/configs/attr_optaa.py
@author Christopher Wingard
@brief Attributes for the OPTAA variables
"""

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
        'long_name': '',
        'standard_name': '',
        'units': '1',
    },
    'a_reference_dark': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'pressure_raw': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'a_signal_dark': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'external_temp_raw': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'external_temp': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'internal_temp_raw': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'internal_temp': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'c_reference_dark': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'c_signal_dark': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'elapsed_run_time': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'num_wavelengths': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'a_wavelengths': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'c_wavelengths': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'c_reference_raw': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'a_reference_raw': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'c_signal_raw': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'a_signal_raw:': {
        'long_name': '',
        'standard_name': '',
        'units': 'counts',
    },
    'a_pd:': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'a_pd_ts:': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'a_pd_ts_s:': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'c_pd:': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'c_pd_ts:': {
        'long_name': '',
        'standard_name': '',
        'units': '',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    }
}
