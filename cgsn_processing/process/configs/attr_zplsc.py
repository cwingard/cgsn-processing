#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_zplsc
@file cgsn_processing/process/configs/attr_zplsc.py
@author Christopher Wingard
@brief Attributes for the ZPLSC variables
"""

ZPLSC = {
    'global': {
        'title': 'Acoustic Profiles of Fish and Zooplankton.',
        'summary': 'Acoustic profiles of fish and zooplankton at four frequencies using the ASL AZFP sensor.',
    },
    'clock_drift': {
        'long_name': 'Internal Clock Drift',
        'units': 'seconds'
    },
    'sampling_drift': {
        'long_name': 'Sampling Time Drift',
        'units': 'seconds'
    },
    'serial_number': {
        'long_name': 'Unit Serial Number',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'burst_number': {
        'long_name': 'Burst Number',
        'units': 'count'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'units': 'V'
    },
    'temperature': {
        'long_name': 'Internal Temperature',
        'units': 'degrees_Celsius'
    },
    'channel_1_freq': {
        'long_name': 'Frequency Channel 1',
        'units': 'kHz'
    },
    'channel_2_freq': {
        'long_name': 'Frequency Channel 2',
        'units': 'kHz'
    },
    'channel_3_freq': {
        'long_name': 'Frequency Channel 3',
        'units': 'kHz'
    },
    'channel_4_freq': {
        'long_name': 'Frequency Channel 4',
        'units': 'kHz'
    },
    'bin_depth': {
        'long_name': 'Estimated Depth',
        'comment': 'Estimate of depth based on range to surface corrected for 15 degree tilt',
        'units': 'm'
    },
    'profiles_channel_1': {
        'long_name': 'Raw Echo Intensity Channel 1',
        'units': 'count'
    },
    'profiles_channel_2': {
        'long_name': 'Raw Echo Intensity Channel 2',
        'units': 'count'
    },
    'profiles_channel_3': {
        'long_name': 'Raw Echo Intensity Channel 3',
        'units': 'count'
    },
    'profiles_channel_4': {
        'long_name': 'Raw Echo Intensity Channel 4',
        'units': 'count'
    }
}
