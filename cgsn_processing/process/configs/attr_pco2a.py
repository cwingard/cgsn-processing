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
    'sample_id': {
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'co2_date_time_string': {
        'long_name': 'Instrument Date and Time String',
        'standard_name': 'instrument_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'zero_a2d': {'units': 'counts'},
    'current_a2d': {'units': 'counts'},
    'measured_co2': {'units': 'ppm'},
    'pCO2': {'units': 'ppm'},
    'avg_irga_temperature': {'units': 'degrees_Celsius'},
    'humidity': {'units': 'mbar'},
    'humidity_temperature': {'units': 'degrees_Celsius'},
    'gas_stream_pressure': {'units': '1'},
    'irga_detector_temperature': {'units': 'degrees_Celsius'},
    'irga_source_temperature': {'units': 'degrees_Celsius'},
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
