#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_gps
@file cgsn_processing/process/configs/attr_gps.py
@author Christopher Wingard
@brief Attributes for the GPS variables
"""

GPS = {
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
    'lat': {},
    'lng': {},
    'speed_over_ground': {},
    'course_over_ground': {},
    'fix_quality': {},
    'number_satellites': {},
    'horiz_dilution_precision': {},
    'altitude': {},
    'gps_date_string': {},
    'gps_time_string': {},
    'latitude_string': {},
    'longitude_string': {},
}
