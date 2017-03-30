#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_presf
@file cgsn_processing/process/configs/attr_presf.py
@author Joe Futrelle
@brief Attributes for the PRESF variables
"""

PRESF = {
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
    'absolute_pressure': {
        'units': 'mbar'
    },
    'seawater_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius'
    }
}
