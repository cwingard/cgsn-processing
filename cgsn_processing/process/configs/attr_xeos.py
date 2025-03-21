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
        'title': 'Message data from the XEOS beacons used on OOI moorings',
        'summary': (
            'XEOS Beacons independently telemeter position data via Iridium emails '
            'to validate mooring location in real-time.'
        ),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.6'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'Derived from the GPS referenced clock used by DCL data logger'
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Instrument deployment depth',
        'positive': 'down',
        'axis': 'Z'
    },
    'momsn': {
        'long_name': 'Message sequence number',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Message sequence number from the ISU')
    },
    'date_time_email': {
        'long_name': 'Email date time',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Date and time of the ISU session')
    },
    'status_code': {
        'long_name': 'Status code',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Session status of the iridium session')
    },
    'transfer_status': {
        'long_name': 'Transfer status',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Transfer status of the iridium message')
    },
    'transfer_bytes': {
        'long_name': 'Transfer bytes',
        'units': 'bytes',
        'comment': ('Size of the iridium message in bytes')
    },
    'estimated_latitude': {
        'long_name': 'Estimated latitude',
        'units': 'degrees north',
        'comment': ('Iridium estimated latitude of message source')
    },
    'estimated_longitude': {
        'long_name': 'Estimated longitude',
        'units': 'degrees east',
        'comment': ('Iridium estimated longitude of message source')
    },
    'cep_radius': {
        'long_name': 'Watch circle radius',
        'units': 'km',
        'comment': ('Estimated 80% probability radius around center of message source')
    },
    'date_time_xeos': {
        'long_name': 'Date time at beacon',
        'units': 'unix time',
        'comment': ('Date and time in UTC of the latest position reading')
    },
    'watch_circle_status': {
        'long_name': 'Watch circle status',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Enabled (1) or disabled (0)')
    },
    'subsurface_beacon': {
        'long_name': 'Subsurface flag',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Flag indicating if beacon is deployed below the sea surface (1)')
    },
    'latitude_xeos': {
        'long_name': 'Xeos Latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('Latitude as reported by the Xeos beacon')
    },
    'longitude_xeos': {
        'long_name': 'Xeos Longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Longitude as reported by the Xeos beacon')
    },
    'distance_from_center': {
        'long_name': 'Distance from center of watch circle',
        'units': 'km',
        'comment': ('Distance from the center of the watch circle')
    },
    'time_in_circle': {
        'long_name': 'Time in circle',
        'units': 'seconds',
        'comment': ('Time continuously spent in watch circle')
    },
    'signal_strength': {
        'long_name': 'Signal strength',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Signal to noise ratio of GPS fix')
    },
    'battery_voltage': {
        'long_name': 'Unpowered battery voltage',
        'units': 'V',
        'comment': ('Voltage measurement taken before powering the iridium modem')
    },
    'loaded_voltage': {
        'long_name': 'Powered battery voltage',
        'units': 'V',
        'comment': ('Voltage measurement taken with iridium modem powered on')
    },
    'sched_timer': {
        'long_name': 'Timer in use',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Timer in the scheduler used when the message was transmitted')
    },
    'altitude': {
        'long_name': 'Altitude',
        'units': 'm',
        'comment': 'Instrument altitude as reported by the XEOS beacon'
    },
    'num_satellites': {
        'long_name': 'Number of satellites',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Number of satellites used during the fix')
    },
    'bearing': {
        'long_name': 'Bearing of satellite',
        'units': 'Degrees north',
        'comment': ('Bearing to the nearest 22.5 degrees')
    },
    'measurement_speed': {
        'long_name': 'Speed of measurement',
        'units': 'm s-1',
        'comment': ('Speed measurement')
    },
    'time_to_fix': {
        'long_name': 'Time to fix',
        'units': 'seconds',
        'comment': ('Time to fix')
    },
    'highest_hdop': {
        'long_name': 'Highest HDOP',
#        'units': '', deliberately left blank, no units for this value
        'comment': ('Highest HDOP used during the fix')
    }
}
