#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_irid
@file cgsn_processing/process/configs/attr_irid.py
@author Joe Futrelle
@brief Attributes for the IRID variables
"""

IRID = {
    'global': {
        'title': 'Iridium RUDICS Telemetry Statistics',
        'summary': 'Summary statistics on telemetry success, duration and signal strengths',
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
    'date_time_string': {
        'long_name': 'Date and Time Stamp',
        'standard_name': 'date_time_string',
        'units': '1',
    },
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Sensor depth below sea surface',
        'positive': 'down',
        'axis': 'Z'
    },
    'files_sent': {},
    'files_received': {},
    'bytes_sent': {},
    'bytes_received': {},
    'average_tx_rate': {},
    'average_rx_rate': {},
    'login_time': {},
    'connection_time': {}
}
