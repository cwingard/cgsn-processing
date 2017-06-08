#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_RDA
@file cgsn_processing/process/configs/attr_RDA.py
@author Joe Futrelle
@brief Attributes for the RDA variables
"""

RDA = {
    'global': {
        'title': 'RDA Status',
        'summary': 'Current and Voltage Levels for the RDA',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes (CGSN)',
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
    'main_voltage': {'units': 'V'},
    'main_current': {'units': 'mA'},
    'error_flags': {'units': '1'},
    'rda_type': {'units': '1'}
}
