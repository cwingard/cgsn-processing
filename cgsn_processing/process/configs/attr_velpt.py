#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_velpt
@file cgsn_processing/process/configs/attr_velpt.py
@author Christopher Wingard
@brief Attributes for the Nortek Aquadopp (VELPT)
"""
VELPT = {
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
    # 'date_time_array': {},
    'error_code': {},
    'battery_voltage': {},
    'speed_of_sound': {},
    'heading': {},
    'pitch': {},
    'roll': {},
    'pressure': {},
    'status_code': {},
    'temperature': {},
    'velocity_east': {},
    'velocity_north': {},
    'velocity_vertical': {},
    'amplitude_beam1': {},
    'amplitude_beam2': {},
    'amplitude_beam3': {}
}
