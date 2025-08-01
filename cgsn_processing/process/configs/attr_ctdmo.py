#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_imm
@file cgsn_processing/process/configs/attr_ctdmo.py
@author Christopher Wingard
@brief Attributes for dataset variables for instruments that are hosted via the inductive modem (IMM)
"""
import numpy as np
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_common import CTD

CTDMO = {
    'global': {
        'title': 'Conductivity, Temperature and Depth (CTD) Data',
        'summary': 'Inductive modem CTD time series data sets from the Global Moorings.'
    },
    # data from the status header
    'status_time': {
        'long_name': 'Status Update Time',
        '_FillValue': np.nan,
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'calendar': 'gregorian',
        'comment': 'Date and time the CTD status was queried.'
    },
    'serial_number': {
        'long_name': 'Serial Number',
        '_FillValue': -9999999,
        # 'units': '',    deliberately left blank, no units for this value
    },
    'main_battery_voltage': {
        'long_name': 'Main Battery Voltage',
        'units': 'V',
        '_FillValue': np.nan
    },
    'lithium_battery_voltage': {
        'long_name': 'Lithium Battery Voltage',
        'units': 'V',
        '_FillValue': np.nan
    },
    'samples_recorded': {
        'long_name': 'Number of Samples Recorded',
        'comment': 'Number of samples recorded during the deployment',
        'units': 'count',
        '_FillValue': -9999999,
    },
    'sample_slots_free': {
        'long_name': 'Number of Free Sample Slots Remaining',
        'comment': 'Number of free samples available for recording, representing the memory available in the unit',
        'units': 'count',
        '_FillValue': -9999999,
    },
    'pressure_range': {
        'long_name': 'Pressure Range',
        'comment': 'Pressure sensor range reported as the absolute pressure (atmospheric + in situ pressure)',
        'units': 'psi',
        '_FillValue': -9999999,
    },

    # Raw values reported by the SBE37, units are all in counts
    'raw_conductivity': {
        'long_name': 'Raw Conductivity',
        'units': 'count',
        'comment': 'Raw conductivity measurement reported in counts.',
        'data_product_identifier': 'CONDWAT_L0',
        '_FillValue': -9999999,
    },
    'raw_temperature': {
        'long_name': 'Raw Temperature',
        'units': 'count',
        'comment': 'Raw temperature measurement reported in counts.',
        'data_product_identifier': 'TEMPWAT_L0',
        '_FillValue': -9999999,
    },
    'raw_pressure': {
        'long_name': 'Raw Pressure',
        'units': 'count',
        'comment': 'Raw pressure measurement reported in counts.',
        'data_product_identifier': 'PRESWAT_L0',
        '_FillValue': -9999999,
    }
}

# add the standard CTD variables to the CTDMO dictionary
CTDMO = dict_update(CTDMO, CTD)
