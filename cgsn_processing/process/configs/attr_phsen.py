#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""
PHSEN = {
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'record_length': {
        'long_name': 'Record Length',
        'standard_name': 'record_length',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'record_type': {
        'long_name': 'Record Type',
        'standard_name': 'record_type',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'standard_name': 'instrument_time',
        'units': 'seconds since 1904-01-01',
        'coordinates': 'time z longitude latitude'
    },
    'thermistor_start': {
        'long_name': 'Temperature Start',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'reference_measurements': {
        'long_name': 'Reference Measurements Array',
        'standard_name': 'reference_measurements',
        'units': 'counts',
        'coordinates': 'time z longitude latitude'
    },
    'light_measurements': {
        'long_name': 'Light Measurements Array',
        'standard_name': 'light_measurements',
        'units': 'counts',
        'coordinates': 'time z longitude latitude'
    },
    'voltage_battery': {
        'long_name': 'Battery Voltage',
        'standard_name': 'battery_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'thermistor_end': {
        'long_name': 'Temperature End',
        'standard_name': 'seawater_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'standard_name': 'internal_clock_offset',
        'units': 'seconds',
        'coordinates': 'time z longitude latitude'
    },
    'pH': {
        'long_name': 'Seawater pH',
        'standard_name': 'seawater_ph',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    }
}
