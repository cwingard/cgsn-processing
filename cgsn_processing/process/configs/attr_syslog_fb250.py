#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_fb250
@file cgsn_processing/process/configs/attr_fb250.py
@author Joe Futrelle
@brief Attributes for the FB250 variables
"""

FB250 = {
    'global': {
        'title': 'Sailor 250 FleetBroadband Telemetry Statistics',
        'summary': 'Summary statistics on telemetry success, duration and signal strengths',
    },
    'link_state': {'units': '1'},
    'rssi': {'units': '1'},
    'temperature': {},
    'precise_lat': {
        'long_name': 'Precise Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'comment': ('Mooring location measured by a GPS sensor located atop the mooring masthead inside the Sailor '
                    '250 antenna dome. Provides a precise measurement of the mooring location, compared to the '
                    'nominal location determined after mooring deployment from an anchor survey.')
    },
    'precise_lon': {
        'long_name': 'Precise Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'comment': ('Mooring location measured by a GPS sensor located atop the mooring masthead inside the Sailor '
                    '250 antenna dome. Provides a precise measurement of the mooring location, compared to the '
                    'nominal location determined after mooring deployment from an anchor survey.')
    },
    'fb250_device_id': {'units': '1'},
    'link_attempts': {'units': 'count'},
    'elapsed_time': {'units': 's'}
}
