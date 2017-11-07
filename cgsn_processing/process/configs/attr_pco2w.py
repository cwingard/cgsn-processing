#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2w
@file cgsn_processing/process/configs/attr_pco2w.py
@author Christopher Wingard
@brief Attributes for the PCO2W variables
"""
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
        'long_name': 'Sample Collection Date and Time Stamp'
    },
    'process_date_time': {
        'long_name': 'Sample Processing Date and Time Stamp'
    },
    'unique_id': {
        'long_name': 'Unique ID'
    },
    'record_length': {
        'long_name': 'Record Length'
    },
    'record_type': {
        'long_name': 'Record Type'
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'units': 'seconds since 1904-01-01',
    },
    'dark_reference_a': {
        'long_name': 'Dark LED Reference, 1st',
        'units': 'counts'
    },
    'dark_signal_a': {
        'long_name': 'Dark LED Signal, 1st',
        'units': 'counts'
    },
    'reference_434_a': {
        'long_name': 'Reference 434 nm, 1st',
        'units': 'counts'
    },
    'signal_434_a': {
        'long_name': 'Signal 434 nm, 1st',
        'units': 'counts'
    },
    'reference_620_a': {
        'long_name': 'Reference 620 nm, 1st',
        'units': 'counts'
    },
    'signal_620_a': {
        'long_name': 'Signal 620 nm, 1st',
        'units': 'counts'
    },
    'ratio_434': {
        'long_name': 'Absorbance Ratio 434 nm',
        'units': 'counts'
    },
    'ratio_620': {
        'long_name': 'Absorbance Ratio 620 nm',
        'units': 'counts'
    },
    'dark_reference_b': {
        'long_name': 'Dark LED Reference, 2nd',
        'units': 'counts'
    },
    'dark_signal_b': {
        'long_name': 'Dark LED Signal, 2nd',
        'units': 'counts'
    },
    'reference_434_b': {
        'long_name': 'Reference 434 nm, 2nd',
        'units': 'counts'
    },
    'signal_434_b': {
        'long_name': 'Signal 434 nm, 2nd',
        'units': 'counts'
    },
    'reference_620_b': {
        'long_name': 'Reference 620 nm, 2nd',
        'units': 'counts'
    },
    'signal_620_b': {
        'long_name': 'Signal 620 nm, 2nd',
        'units': 'counts'
    },
    'voltage_raw': {
        'long_name': 'Raw Battery Voltage',
        'units': 'counts'
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
    'k434': {
        'long_name': 'Blank Intensity 434 nm',
        'units': '1'
    },
    'k620': {
        'long_name': 'Blank Intensity 620 nm',
        'units': '1'
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
