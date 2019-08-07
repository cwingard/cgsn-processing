#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mmp
@file cgsn_processing/process/configs/attr_mmp.py
@author Joe Futrelle
@brief Attributes for the MMP variables
"""

MMP = {
    'global': {
        'title': 'McLane Moored Profiler Data',
        'summary': 'Datasets from the McLane Moored Profiler (MMP).',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000',
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
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius'
    },
    'psu': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'valid_min': '0',
        'valid_max': '40'
    },
    'rho': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'valid_min': '0',
        'valid_max': '35'
    }
}

MMP_ADATA = {
}

MMP_CDATA = {
}

MMP_EDATA = {
}
