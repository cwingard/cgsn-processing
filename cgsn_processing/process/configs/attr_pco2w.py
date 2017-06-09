#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2w
@file cgsn_processing/process/configs/attr_pco2w.py
@author Christopher Wingard
@brief Attributes for the PCO2W variables
"""
import numpy as np

PCO2W = {
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
    'measurements': {
        'long_name': 'Measurements Array',
        'standard_name': 'measurements',
        'units': '1',
    },
    'collect_date_time': {
        'long_name': 'Sample Collection Date and Time Stamp',
        'standard_name': 'date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'process_date_time': {
        'long_name': 'Sample Processing Date and Time Stamp',
        'standard_name': 'date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'unique_id': {},
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
    'light_measurements': {
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'voltage_battery': {
        'long_name': 'Battery Voltage',
        'standard_name': 'battery_voltage',
        'units': 'V'
    },
    'thermistor_raw': {},
    'thermistor': {
        'long_name': 'Temperature',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celsius'
    },
    'blank_434': {
        'long_name': 'Blank Intensity 434 nm',
        'standard_name': 'blank_434',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'blank_620': {
        'long_name': 'Blank Intensity 620 nm',
        'standard_name': 'blank_620',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'standard_name': 'internal_clock_offset',
        'units': 'seconds'
    },
    'pCO2': {
        'long_name': 'Seawater pCO2',
        'standard_name': 'seawater_pco2',
        'units': 'ppm'
    }
}
