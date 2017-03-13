#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mmp
@file cgsn_processing/process/configs/attr_mmp.py
@author Joe Futrelle
@brief Attributes for the MMP variables
"""

MMP = {
    'z': {
        'long_name': 'depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
    },
    'depth': {
        'long_name': 'depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
    },
    'pressure': {
        'long_name': 'sea pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'mbar'
    },
    'temperature': {
        'long_name': 'temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius'
    }
}

MMP_ADATA = {
}

MMP_CDATA = {
}

MMP_EDATA = {
}
