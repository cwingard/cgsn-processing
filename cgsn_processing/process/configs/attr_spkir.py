#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_spkir
@file cgsn_processing/process/configs/attr_spkir.py
@author Joe Futrelle
@brief Attributes for the SPKIR variables
"""

SPKIR = {
    'global': {
        'title': '(title goes here)',
        'summary': '(summary goes here)',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'internal_temperature': {
        'units': 'degree_Celsius'
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
}
