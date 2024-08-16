#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ctdbp
@file cgsn_processing/process/configs/attr_ctdbp.py
@author Christopher Wingard
@brief Attributes for the CTDBP variables
"""
import numpy as np
from cgsn_processing.process.common import FILL_INT
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_common import CTD
from cgsn_processing.process.configs.attr_dosta import DOSTA
from cgsn_processing.process.configs.attr_flort import FLORT

# Note, common CTD attributes used by all the CTD configurations are defined in attr_common.py. The attributes
# specific to the DOSTA and FLORT sensors are defined in attr_dosta.py and attr_flort.py, respectively.
CTDBP = {
    'global': {
        'title': 'Conductivity, Temperature and Depth (CTD) Data',
        'summary': 'Moored CTD time series data sets.'
    },
    # attributes associated with the status message output from a CTDBP connected to an inductive modem (IMM)
    'status_time': {
        'long_name': 'Status Update Time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'comment': 'Date and time the CTD status was queried.',
        'calendar': 'gregorian',
        '_FillValue': np.nan
    },
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Instrument serial number.',
        '_FillValue': FILL_INT,
    },
    'main_battery_voltage': {
        'long_name': 'Main Battery Voltage',
        'units': 'V',
        'comment': 'Voltage of either the internal battery pack or externally supplied power, whichever is greater.',
        '_FillValue': np.nan
    },
    'lithium_battery_voltage': {
        'long_name': 'Lithium Battery Voltage',
        'units': 'V',
        'comment': 'Voltage of the internal battery cell, used to maintain the clock and firmware settings.',
        '_FillValue': np.nan
    },
    'samples_recorded': {
        'long_name': 'Number of Samples Recorded',
        'units': 'count',
        'comment': 'Number of samples recorded during the deployment',
        '_FillValue': FILL_INT
    },
    'sample_slots_free': {
        'long_name': 'Number of Free Sample Slots Remaining',
        'units': 'count',
        'comment': 'Number of free samples available for recording, representing the memory available in the unit',
        '_FillValue': FILL_INT
    },
    'main_current': {
        'long_name': 'Main Current',
        'units': 'mA',
        'comment': 'Total current draw on the system, encompassing all functions and external sensors.',
        '_FillValue': np.nan
    },
    'pump_current': {
        'long_name': 'Pump Current',
        'units': 'mA',
        'comment': 'Current draw from the system by the external pump.',
        '_FillValue': np.nan
    },
    'oxy_current': {
        'long_name': 'Oxygen Sensor Current',
        'units': 'mA',
        'comment': 'Current draw from the system by the external optode oxygen (DOSTA) sensor.',
        '_FillValue': np.nan
    },
    'flr_current': {
        'long_name': 'Fluorometer Sensor Current',
        'units': 'mA',
        'comment': 'Current draw from the system by the external two-channel fluorometer (FLORD) sensor.',
        '_FillValue': np.nan
    },

    # less common values recorded by the different CTDBP configurations
    # --> equipped with an optode (DOSTA) sensor reporting analog voltages
    'raw_calibrated_phase': {
        'long_name': 'Raw Calibrated Phase Difference',
        'units': 'V',
        'comment': ('The optode measures oxygen by exciting a special platinum porphyrin complex embedded in a '
                    'gas permeable foil with modulated blue light. The Optode measures the phase shift of a '
                    'returned red light. To convert the raw calibrated phase difference reported in V to degrees, '
                    'This value is recorded by the CTD as an analog voltage signal.'),
        'data_product_identifier': 'DOCONCS-VLT_L0',
        '_FillValue': np.nan
    },
    'raw_optode_thermistor': {
        'long_name': 'Raw Optode Thermistor',
        'units': 'V',
        'comment': ('The optode includes an integrated internal thermistor to measure the temperature at '
                    'the sensing foil. This value is recorded by the CTD as an analog voltage signal.'),
        '_FillValue': np.nan
    }
}

# add the standard CTD variables and the DOSTA and FLORT attributes to the CTDBP attributes
CTDBP = dict_update(CTDBP, CTD)
CTDBP = dict_update(CTDBP, DOSTA)
CTDBP = dict_update(CTDBP, FLORT)
