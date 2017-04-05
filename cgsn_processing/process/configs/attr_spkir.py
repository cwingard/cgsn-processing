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
        'title': 'Downwelling Spectral Irradiance at 7 meters',
        'summary': 'Downwelling spectral irradiance measured over 7 wavelengths at 7 meter depth',
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
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
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
    'serial_number': {},
    'timer': {},
    'sample_delay': {},
    'raw_channel1': {
        'units': 'counts'
    },
    'raw_channel2': {
        'units': 'counts'
    },
    'raw_channel3': {
        'units': 'counts'
    },
    'raw_channel4': {
        'units': 'counts'
    },
    'raw_channel5': {
        'units': 'counts'
    },
    'raw_channel6': {
        'units': 'counts'
    },
    'raw_channel7': {
        'units': 'counts'
    },
    'irradiance1': {
        'units': 'microW cm-2 nm-1'
    },
    'irradiance2': {
        'units': 'microW cm-2 nm-1'
    },
    'irradiance3': {
        'units': 'microW cm-2 nm-1'
    },
    'irradiance4': {
        'units': 'microW cm-2 nm-1'
    },
    'irradiance5': {
        'units': 'microW cm-2 nm-1'
    },
    'irradiance6': {
        'units': 'microW cm-2 nm-1'
    },
    'irradiance7': {
        'units': 'microW cm-2 nm-1'
    },
    'input_voltage': {
        'units': 'Volts'
    },
    'analog_rail_voltage': {
        'units': 'Volts'
    },
    'frame_counter': {
        'units': '1'
    },
    'internal_temperature': {
        'units': 'degree_Celsius'
    }
}
