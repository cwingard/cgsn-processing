#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_zplsc
@file cgsn_processing/process/configs/attr_zplsc.py
@author Christopher Wingard
@brief Attributes for the ZPLSC variables
"""
from cgsn_processing.process.common import FILL_INT

ZPLSC = {
    'global': {
        'title': 'Acoustic Profiles of Fish and Zooplankton.',
        'summary': 'Acoustic profiles of fish and zooplankton at four frequencies using the ASL AZFP sensor.',
    },
    'transmission_time': {
        'long_name': 'Condensed Profile Transmission Time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'calendar': 'gregorian',
        'comment': ('Date and time from the sensor''s internal clock. It is expected that this value will drift from '
                    'the true time by some amount over the course of a deployment. Cross-comparisons to the DCL''s '
                    'GPS based clock will be required to account for any offset and drift in the sensor.'),
    },
    'burst_time': {
        'long_name': 'Condensed Profile Sample Time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'calendar': 'gregorian',
        'comment': ('Date and time of the first profile in the burst. Should align closely with when the instrument '
                    'is programmed to sample. Can be used to track drift in the sampling time over the course of a '
                    'deployment.'),
    },
    'clock_offset': {
        'long_name': 'Internal Clock Offset',
        'units': 's',
        'comment': ('Cross-compares the instrument clock, specifically the condensed profile transmission time, to the '
                    'GPS-based timestamp applied by the DCL upon receipt of the data string. Allows for a '
                    'determination of the internal clock offset and drift over the course of a deployment.')
    },
    'sampling_offset': {
        'long_name': 'Sampling Time Offset',
        'units': 's',
        'comment': ('Tracks the potential offset and drift between when the first condensed profile in the burst was '
                    'recorded compared to when the instrument was actually programmed to record a burst. Like the '
                    'clock_offset, allows for a determination of the drift in the sampling schedule over the course '
                    'of a deployment.')
    },
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': ''    # deliberately left blank, no units for this value,
        'comment': 'Instrument serial number.'
    },
    'burst_number': {
        'long_name': 'Burst Number',
        'units': 'count',
        'comment': 'Sequential number counting the bursts recorded during a deployment.'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'units': 'V',
        'comment': 'Internal battery voltage'
    },
    'temperature': {
        'long_name': 'Internal Temperature',
        'units': 'degrees_Celsius',
        'comment': ('Temperature recorded internal to the pressure housing. Will be slightly warmer than the in-situ '
                    'temperature due to heating by the electronics.')
    },
    'channel_1_freq': {
        'long_name': 'Frequency Channel 1',
        'units': 'kHz',
        'comment': 'Frequency of the transducer assigned to channel 1.'
    },
    'channel_2_freq': {
        'long_name': 'Frequency Channel 2',
        'units': 'kHz',
        'comment': 'Frequency of the transducer assigned to channel 2.'
    },
    'channel_3_freq': {
        'long_name': 'Frequency Channel 3',
        'units': 'kHz',
        'comment': 'Frequency of the transducer assigned to channel 3.'
    },
    'channel_4_freq': {
        'long_name': 'Frequency Channel 4',
        'units': 'kHz',
        'comment': 'Frequency of the transducer assigned to channel 4.'
    },
    'bin_depth': {
        'long_name': 'Estimated Depth',
        'units': 'm',
        'comment': 'Estimate of depth based on range to surface corrected for 15 degree tilt'
    },
    'profiles_channel_1': {
        'long_name': 'Raw Echo Intensity Channel 1',
        'units': 'count',
        'comment': 'Raw acoustic backscatter measurements for channel 1, reported in counts.',
        '_FillValue': FILL_INT
    },
    'profiles_channel_2': {
        'long_name': 'Raw Echo Intensity Channel 2',
        'units': 'count',
        'comment': 'Raw acoustic backscatter measurements for channel 2, reported in counts.',
        '_FillValue': FILL_INT
    },
    'profiles_channel_3': {
        'long_name': 'Raw Echo Intensity Channel 3',
        'units': 'count',
        'comment': 'Raw acoustic backscatter measurements for channel 3, reported in counts.',
        '_FillValue': FILL_INT
    },
    'profiles_channel_4': {
        'long_name': 'Raw Echo Intensity Channel 4',
        'units': 'count',
        'comment': 'Raw acoustic backscatter measurements for channel 4, reported in counts.',
        '_FillValue': FILL_INT
    }
}
