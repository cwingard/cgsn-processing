#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_presf
@file cgsn_processing/process/configs/attr_presf.py
@author Joe Futrelle
@brief Attributes for the PRESF variables
       11212023 ppw added RBRQ3 variables
"""

PRESF = {
    'global': {
        'title': 'Seafloor Pressure',
        'summary': 'Seafloor pressure integrated over 60 minutes showing tidal signature',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes, (CGSN)',
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
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
    },
    'presf_date_time_string': {
        'long_name': 'PRESF Date and Time Stamp',
        'standard_name': 'presf_date_time_string',
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
    'pressure_temp': {
        'units': 'degrees_Celsius'
    },
    'absolute_pressure': {
        'units': 'psi'
    },
    'seafloor_pressure': {
        'units': 'dbar'
    },
    'seawater_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius'
    }
}

RBRQ3 = {
    'global': {
        'title': 'Seafloor Pressure',
        'summary': 'Seafloor pressure ???',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes, (CGSN)',
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
        'long_name': 'RBRQ3 Date and Time Stamp',
        'standard_name': '_date_time_string',
        'units': '1',
    },
    'unix_date_time_ms': {
        'long_name': 'RBRQ3 Unix date time ms',
        'standard_name': 'time_ms',
        'units': '1',
    },
    'depth_00': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000',
    },
    'temperature_00': {
        'long_name': 'Temperature of ???',
        'units': 'degrees_Celsius',
    },
    'pressure_00': {
        'long_name': 'Pressure of ???',
        'units': 'degrees_Celsius',
    },
    'temperature_01': {
        'long_name': 'Temperature of ???',
        'units': 'degrees_Celsius',
    },
    'seapressure_00': {
        'long_name': 'Sea floor pressure',
        'standard_name': 'seafloor_pressure',
        'units': 'dbar',
    },
    'period_00': {
        'long_name': 'Period of ???',
        'units': 'seconds???',
    },
    'period_01': {
        'long_name': 'Period of ???',
        'units': 'seconds???',
    }
}
