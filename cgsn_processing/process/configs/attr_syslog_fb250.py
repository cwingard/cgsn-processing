#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_fb250
@file cgsn_processing/process/configs/attr_fb250.py
@author Joe Futrelle
@brief Attributes for the FB250 variables
"""

FB250 = {
    'global': {
        'title': 'Sailor 250 FleetBroadband Telemetry Statistics',
        'summary': 'Summary statistics on telemetry success, duration and signal strengths',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'standard_name': 'deployment_id',
        'units': '1',
    },
    'date_time_string': {
        'long_name': 'Date and Time Stamp',
        'standard_name': 'date_time_string',
        'units': '1',
    },
    'depth': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000',
    },
    'link_state': {'units': '1'},
    'rssi': {'units': '1'},
    'temperature': {},
    'latitude': {
        'long_name': 'latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north'
    },
    'longitude': {
        'long_name': 'longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east'
    },
    'fb250_device_id': {'units': '1'},
    'link_attempts': {'units': 'count'},
    'elapsed_time': {'units': 's'}
}
