#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_RDA
@file cgsn_processing/process/configs/attr_RDA.py
@author Joe Futrelle
@brief Attributes for the RDA variables
"""
import numpy as np

RDA = {
    'global': {
        'title': 'RDA Status',
        'summary': 'Current and Voltage Levels for the RDA',
    },
    'main_voltage': {
        'long_name': 'Main Voltage',
        'units': 'V',
        'comment': 'Input voltage supplied to the system.'
    },
    'main_current': {
        'long_name': 'Main Current',
        'units': 'mA',
        'comment': 'Electrical current used by the system.'
    },
    'error_flags': {
        'long_name': 'RDA Error Flags',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value,
        'comment': 'Error flags for the RDA PIC data.',
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('no_errors undefined undefined undefined undefined undefined undefined undefined undefined '
                          'undefined undefined undefined undefined undefined undefined undefined undefined undefined '
                          'undefined undefined undefined undefined undefined undefined undefined undefined undefined '
                          'undefined undefined undefined undefined undefined undefined'),
        'ancillary_variables': 'main_voltage main_current'
    },
    'rda_type': {
        'long_name': 'RDA Board Type',
        # 'units': '',    deliberately left blank, no units for this value,
        'comment': 'Type of RDA board, where 0 == CI, 1 == NSIF and 2 == MFN.',
        'flag_values': np.intc([0, 1, 2]),
        'flag_meanings': 'CI NSIF MFN'
    }
}
