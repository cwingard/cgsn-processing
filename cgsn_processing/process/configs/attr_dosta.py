#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_dosta
@file cgsn_processing/process/configs/attr_dosta.py
@author Christopher Wingard
@brief Attributes for the dissolved oxygen (DOSTA) sensor
"""
DOSTA = {
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
    'date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'product_number': {
        'units': '1'
    },
    'serial_number': {
        'units': '1'
    },
    'estimated_oxygen_concentration': {
        'units': 'umol/L'
    },
    'estimated_oxygen_saturation': {
        'units': 'percent'
    },
    'optode_temperature': {
        'units': 'degree_Celsius'
    },
    'calibrated_phase': {
        'units': 'degree'
    },
    'temp_compensated_phase': {
        'units': 'degree'
    },
    'blue_phase': {
        'units': 'degree'
    },
    'red_phase': {
        'units': 'degree'
    },
    'blue_amplitude': {
        'units': 'mV'
    },
    'red_amplitude': {
        'units': 'mV'
    },
    'raw_temperature': {
        'units': 'mV'
    }
}
