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
    'lat': {
        'long_name': 'latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north'
    },
    'lon': {
        'long_name': 'longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east'
    },
    'speed_over_ground': {'units': 'knot'},
    'course_over_ground': {'units': 'degrees'},
    'fix_quality': {'units': '1'},
    'number_satellites': {'units': '1'},
    'horiz_dilution_precision': {'units': '1'},
    'altitude': {'units': 'm'},
    'gps_date_string': {'units': '1'},
    'gps_time_string': {'units': '1'},
    'latitude_string': {'units': '1'},
    'longitude_string': {'units': '1'}
}
