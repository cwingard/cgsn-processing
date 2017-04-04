#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_flort
@file cgsn_processing/process/configs/attr_flort.py
@author Christopher Wingard
@brief Attributes for the FLORT variables
"""

FLORT = {
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
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'flort_date_time_string':{
        'long_name': 'FLORT Date and Time Stamp',
        'standard_name': 'flort_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'measurement_wavelength_beta': {},
    'raw_signal_beta': {
        'units': 'counts'
    },
    'measurement_wavelength_chl': {},
    'raw_signal_chl': {
        'units': 'counts'
    },
    'measurement_wavelength_cdom': {},
    'raw_signal_cdom': {
        'units': 'counts'
    },
    'raw_internal_temp': {
        'units': 'counts'
    },
    'estimated_chlorophyll': {
        'units': 'mg L-1'
    },
    'fluorometric_cdom': {
        'units': 'ppm'
    },
    'beta_700': {
        'units': 'm-1 sr-1'
    }
}
