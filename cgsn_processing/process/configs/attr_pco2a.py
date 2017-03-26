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
    'sample_id': {},
    'co2_date_time_string': {},
    'zero_a2d': {},
    'current_a2d': {},
    'measured_co2': {},
    'pCO2': {},
    'avg_irga_temperature': {},
    'humidity': {},
    'humidity_temperature': {},
    'gas_stream_pressure': {},
    'irga_detector_temperature': {},
    'irga_source_temperature': {},
    'z_water': {
        'long_name': 'Water Intake Depth',
        'standard_name': 'depth_of_water_intake_port',
        'units': 'm',
        'positive': 'down'
    },
    'z_air': {
        'long_name': 'Air Intake Altitude',
        'standard_name': 'altitude_of_air_intake_port',
        'units': 'm',
        'positive': 'down'
    }
}
