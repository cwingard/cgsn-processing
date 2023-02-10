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
