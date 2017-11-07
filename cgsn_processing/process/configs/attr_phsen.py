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
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'measurements': {
        'long_name': 'Measurements Array',
        'units': '1',
    },
    'blank_refrnc_434': {
        'long_name': 'DI Blank Reference Intensity 434 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'blank_signal_434': {
        'long_name': 'DI Blank Signal Intensity 434 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'blank_refrnc_578': {
        'long_name': 'DI Blank Reference Intensity 578 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'blank_signal_578': {
        'long_name': 'DI Blank Signal Intensity 578 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'reference_434': {
        'long_name': 'Reference Intensity 434 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'signal_434': {
        'long_name': 'Signal Intensity 434 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'reference_578': {
        'long_name': 'Reference Intensity 578 nm',
        'units': 'counts',
        'coordinates': 'time z longitude latitude',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'signal_578': {
        'long_name': 'Signal Intensity 578 nm',
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
        'units': '1'
    },
    'record_type': {
        'long_name': 'Record Type',
        'units': '1'
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'units': 'seconds since 1904-01-01',
    },
    'thermistor_start': {
        'long_name': 'Temperature Start',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celsius'
    },
    'voltage_battery': {
        'long_name': 'Battery Voltage',
        'units': 'V'
    },
    'thermistor_end': {
        'long_name': 'Temperature End',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celsius'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'units': 'seconds'
    },
    'pH': {
        'long_name': 'Seawater pH',
        'standard_name': 'sea_water_ph_reported_on_total_scale',
        'units': '1'
    }
}
