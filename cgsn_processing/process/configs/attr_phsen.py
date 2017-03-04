#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""
import numpy as np

PHSEN = {
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
    'reference_measurements': {
        'long_name': 'Reference Measurements Array',
        'standard_name': 'reference_measurements',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'light_measurements': {
        'long_name': 'Light Measurements Array',
        'standard_name': 'light_measurements',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'record_length': {
        'long_name': 'Record Length',
        'standard_name': 'record_length',
        'units': '1'
    },
    'record_type': {
        'long_name': 'Record Type',
        'standard_name': 'record_type',
        'units': '1'
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'standard_name': 'instrument_time',
        'units': 'seconds since 1904-01-01',
    },
    'thermistor_start': {
        'long_name': 'Temperature Start',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celcius'
    },
    'voltage_battery': {
        'long_name': 'Battery Voltage',
        'standard_name': 'battery_voltage',
        'units': 'V'
    },
    'thermistor_end': {
        'long_name': 'Temperature End',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celcius'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'standard_name': 'internal_clock_offset',
        'units': 'seconds'
    },
    'pH': {
        'long_name': 'Seawater pH',
        'standard_name': 'seawater_ph',
        'units': '1'
    }
}
