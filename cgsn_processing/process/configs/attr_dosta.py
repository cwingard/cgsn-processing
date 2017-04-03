#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_dosta
@file cgsn_processing/process/configs/attr_dosta.py
@author Christopher Wingard
@brief Attributes for the hydrogen gas variables
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
    'product_number': {},
    'serial_number': {},
    'estimated_oxygen_concentration': {},
    'estimated_oxygen_saturation': {},
    'optode_temperature': {},
    'calibrated_phase': {},
    'temp_compensated_phase': {},
    'blue_phase': {},
    'red_phase': {},
    'blue_amplitude': {},
    'red_amplitude': {},
    'raw_temperature': {}
}
