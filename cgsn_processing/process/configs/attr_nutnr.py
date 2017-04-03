#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_nutnr
@file cgsn_processing/process/configs/attr_nutnr.py
@author Christopher Wingard
@brief Attributes for the ISUS nitrate sensor
"""
NUTNR = {
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
    'measurement_type': {},
    'serial_number': {},
    'date_string': {},
    'decimal_hours': {},
    'nitrate_concentration': {},
    'auxiliary_fit_1st': {},
    'auxiliary_fit_2nd': {},
    'auxiliary_fit_3rd': {},
    'rms_error': {},
    'temperature_internal': {},
    'temperature_spectrometer': {},
    'temperature_lamp': {},
    'lamp_on_time': {},
    'humidity': {},
    'voltage_lamp': {},
    'voltage_analog': {},
    'voltage_main': {},
    'average_reference': {},
    'variance_reference': {},
    'seawater_dark': {},
    'spectal_average': {},
    'channel_measurements': {}
}
