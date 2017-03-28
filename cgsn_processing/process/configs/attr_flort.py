#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2a
@file cgsn_processing/process/configs/attr_pco2a.py
@author Christopher Wingard
@brief Attributes for the PCO2A variables
"""

PCO2A = {
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
    'raw_signal_beta': {},
    'measurement_wavelength_chl': {},
    'raw_signal_chl': {},
    'measurement_wavelength_cdom': {},
    'raw_signal_cdom': {},
    'raw_internal_temp': {},
    'estimated_chlorophyll': {},
    'fluorometric_cdom': {},
    'beta_700': {}
}
