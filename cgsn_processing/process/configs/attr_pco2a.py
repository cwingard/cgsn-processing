#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2a
@file cgsn_processing/process/configs/attr_pco2a.py
@author Christopher Wingard
@brief Attributes for the PCO2A variables
"""

PCO2A = {
    'global': {
        'title': 'Partial Pressure of CO2 in the Air and Water',
        'summary': (
            'Measures partial pressure of CO2 in the air and water, concurrently.'
        ),
    },
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
    'co2_source': {
        'units': '1',
    },
    'zero_a2d': {'units': 'counts'},
    'current_a2d': {'units': 'counts'},
    'measured_co2': {'units': 'ppm'},
    'pCO2': {'units': 'ppm'},
    'avg_irga_temperature': {'units': 'degrees_Celsius'},
    'humidity': {'units': 'percent'},
    'humidity_temperature': {'units': 'degrees_Celsius'},
    'gas_stream_pressure': {'units': 'mbar'},
    'irga_detector_temperature': {'units': 'degrees_Celsius'},
    'irga_source_temperature': {'units': 'degrees_Celsius'},
}
