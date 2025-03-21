#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mopak
@file cgsn_processing/process/configs/attr_mopak.py
@author Christopher Wingard
@brief Attributes for the hydrogen gas variables
"""
MOPAK = {
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
    'acceleration_x': {},
    'acceleration_y': {},
    'acceleration_z': {},
    'angular_rate_x': {},
    'angular_rate_y': {},
    'angular_rate_z': {},
    'magnetometer_x': {},
    'magnetometer_y': {},
    'magnetometer_z': {},
    'timer': {}
}
