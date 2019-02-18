#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_imm
@file cgsn_processing/process/configs/attr_ctdmo.py
@author Christopher Wingard
@brief Attributes for dataset variables for instruments that are hosted via the inductive modem (IMM)
"""
import numpy as np

CTDMO = {
    'global': {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'units': '1'
    },
    'lat': {},
    'lon': {},
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Deployment site depth',
        'positive': 'down',
        'axis': 'Z'
    },
}

STATUS = {
    'global': {
        'title': 'uIMM CTD Data Records',
        'summary': (
            'Records the CTD data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
}

RAW = {
    'raw_conductivity': {
        'long_name': 'Raw Conductivity',
        'units': 'counts'
    },
    'raw_temperature': {
        'long_name': 'Raw Temperature',
        'units': 'counts'
    },
    'raw_pressure': {
        'long_name': 'Raw Pressure',
        'units': 'counts'
    }
}

DERIVED = {
    'conductivity': {
        'long_name': 'Sea Water Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius'
    },
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_salinity',
        'units': '1',
    },
    'in_situ_density': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'valid_min': '1000',
        'valid_max': '1035'
    }
}
