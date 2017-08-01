#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2w
@file cgsn_processing/process/configs/attr_pco2w.py
@author Christopher Wingard
@brief Attributes for the PCO2W variables
"""
import numpy as np

PCO2W = {
    'global': {
        'title': 'Partial Pressure of CO2 in Sea Water',
        'summary': 'Partial pressure of CO2 in sea water measured using the Sunburst Sensors SAMI2-pCO2 unit.',
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
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000',
    },
    'collect_date_time': {
        'long_name': 'Sample Collection Date and Time Stamp',
        'units': '1',
    },
    'process_date_time': {
        'long_name': 'Sample Processing Date and Time Stamp',
        'units': '1',
    },
    'unique_id': {
        'long_name': 'Unique ID',
        'units': '1'
    },
    'record_length': {
        'long_name': 'Record Length',
        'units': '1'
    },
    'record_type': {
        'long_name': 'Record Type',
        'units': '1'
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'units': 'seconds since 1904-01-01',
    },
    'measurements': {
        'long_name': 'Measurements Array Index',
        'units': '1',
    },
    'light_measurements': {
        'long_name': 'Light Measurements',
        'units': 'counts',
    },
    'voltage_battery': {
        'long_name': 'Battery Voltage',
        'units': 'V'
    },
    'thermistor_raw': {
        'long_name': 'Raw Thermistor',
        'units': 'counts'
    },
    'thermistor': {
        'long_name': 'Temperature',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celsius'
    },
    'blank_434': {
        'long_name': 'Blank Intensity 434 nm',
        'units': 'counts',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
    },
    'blank_620': {
        'long_name': 'Blank Intensity 620 nm',
        'units': 'counts',
        'fill_value': np.int32(-999999999),
        'missing_value': np.int32(-999999999),
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'units': 'seconds'
    },
    'pCO2': {
        'long_name': 'Seawater pCO2',
        'standard_name': 'partial_pressure_of_carbon_dioxide_in_sea_water',
        'units': 'uatm'
    }
}
