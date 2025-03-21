#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_xeos
@file cgsn_processing/process/configs/attr_xeos.py
@author Paul Whelan
@brief Attributes for the XEOS message variables
"""
import numpy as np

XEOS = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Xeos Technologies GPS Beacon Data',
        'summary': ('XEOS Technologies GPS Beacons used to track the location of '
                    'moorings and instruments deployed in the ocean.'),
    },
    'momsn': {
        'long_name': 'Message sequence number',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Message sequence number from the ISU'
    },
    'date_time_email': {
        'long_name': 'Email date time',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Date and time of the ISU session'
    },
    'status_code': {
        'long_name': 'Status code',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Session status of the iridium session'
    },
    'transfer_status': {
        'long_name': 'Transfer status',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Transfer status of the iridium message'
    },
    'transfer_bytes': {
        'long_name': 'Transfer bytes',
        'units': 'bytes',
        'comment': 'Size of the iridium message in bytes'
    },
    'estimated_latitude': {
        'long_name': 'Estimated latitude',
        'units': 'degrees_north',
        'comment': 'Iridium estimated latitude of message source'
    },
    'estimated_longitude': {
        'long_name': 'Estimated longitude',
        'units': 'degrees_east',
        'comment': 'Iridium estimated longitude of message source'
    },
    'cep_radius': {
        'long_name': 'Watch circle radius',
        'units': 'km',
        'comment': 'Estimated 80% probability radius around center of message source'
    },
    'date_time_xeos': {
        'long_name': 'Date time at beacon',
        'units': 'unix time',
        'comment': 'Date and time in UTC of the latest position reading'
    },
    'watch_circle_status': {
        'long_name': 'Watch circle status',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Enabled (1) or disabled (0)'
    },
    'subsurface_beacon': {
        'long_name': 'Subsurface flag',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Flag indicating if beacon is deployed below the sea surface (1)'
    },
    'latitude_xeos': {
        'long_name': 'Xeos Latitude',
        'units': 'degrees_north',
        'comment': 'Latitude as reported by the Xeos beacon'
    },
    'longitude_xeos': {
        'long_name': 'Xeos Longitude',
        'units': 'degrees_east',
        'comment': 'Longitude as reported by the Xeos beacon'
    },
    'distance_from_center': {
        'long_name': 'Distance from center of watch circle',
        'units': 'km',
        'comment': 'Distance from the center of the watch circle'
    },
    'time_in_circle': {
        'long_name': 'Time in circle',
        'units': 'seconds',
        'comment': 'Time continuously spent in watch circle'
    },
    'signal_strength': {
        'long_name': 'Signal strength',
        'units': '1',
        'comment': 'Signal to noise ratio of GPS fix'
    },
    'battery_voltage': {
        'long_name': 'Unpowered battery voltage',
        'units': 'V',
        'comment': 'Voltage measurement taken before powering the iridium modem'
    },
    'loaded_voltage': {
        'long_name': 'Powered battery voltage',
        'units': 'V',
        'comment': 'Voltage measurement taken with iridium modem powered on'
    },
    'schedule_timer': {
        'long_name': 'Timer in use',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Timer in the scheduler used when the message was transmitted'
    },
    'altitude': {
        'long_name': 'Altitude',
        'units': 'm',
        'comment': 'Instrument altitude as reported by the XEOS beacon'
    },
    'num_satellites': {
        'long_name': 'Number of satellites',
        'units': 'counts',
        'comment': 'Number of satellites used during the fix'
    },
    'bearing': {
        'long_name': 'Bearing of satellite',
        'units': 'Degrees north',
        'comment': 'Bearing to the nearest 22.5 degrees'
    },
    'measurement_speed': {
        'long_name': 'Speed of measurement',
        'units': 'm s-1',
        'comment': 'Speed measurement'
    },
    'time_to_fix': {
        'long_name': 'Time to fix',
        'units': 'seconds',
        'comment': 'Time to fix'
    },
    'highest_hdop': {
        'long_name': 'Highest HDOP',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Highest HDOP used during the fix'
    }
}
