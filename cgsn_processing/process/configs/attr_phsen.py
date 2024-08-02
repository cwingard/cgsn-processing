#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""
import numpy as np
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_common import CO_LOCATED

PHSEN = {
    'global': {
        'title': 'Seawater pH',
        'summary': 'Measurements of the seawater pH using the Sunburst Sensors SAMI2-pH Instrument.',
    },
    'unique_id': {
        'long_name': 'Instrument Unique ID',
        'comment': ('One byte checksum summary of the instrument serial number, name, calibration date and firmware '
                    'version serving as a proxy for a unique ID. While identified as the instrument unique ID, it is '
                    'possible for more than one instrument to have the same checksum summary. Thus, the uniqueness '
                    'of this value should be considered with a certain degree of caution.'),
        # 'units': '',    deliberately left blank, no units for this value
    },
    'measurements': {
        'long_name': 'Measurements Array',
        'comment': 'Dimensional indexing array created for the reference and light measurements.',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'blank_refrnc_434': {
        'long_name': 'DI Blank Reference Intensity at 434 nm',
        'comment': ('Optical absorbance reference intensity at 434 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'count',
        '_FillValue': -9999999,
    },
    'blank_signal_434': {
        'long_name': 'DI Blank Signal Intensity at 434 nm',
        'comment': ('Optical absorbance signal intensity at 434 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'count',
        '_FillValue': -9999999,
    },
    'blank_refrnc_578': {
        'long_name': 'DI Blank Reference Intensity at 578 nm',
        'comment': ('Optical absorbance reference intensity at 578 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'count',
        '_FillValue': -9999999,
    },
    'blank_signal_578': {
        'long_name': 'DI Blank Signal Intensity at 578 nm',
        'comment': ('Optical absorbance signal intensity at 578 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'count',
        '_FillValue': -9999999,
    },
    'reference_434': {
        'long_name': 'Reference Intensity at 434 nm',
        'comment': ('Optical absorbance reference intensity at 434 nm. Reference and signal intensities range '
                    'between 0 and 4096. Values should be greater than ~1500. Lower intensities will result in '
                    'higher noise in the absorbance and pH measurements.'),
        'units': 'count'
    },
    'signal_434': {
        'long_name': 'Signal Intensity at 434 nm',
        'comment': ('Optical absorbance signal intensity at 434 nm. Reference and signal intensities range between 0 '
                    'and 4096. Values should be greater than ~1500. Lower intensities will result in higher noise in '
                    'the absorbance and pH measurements.'),
        'data_product_identifier': 'PH434SI_L0',
        'units': 'count'
    },
    'reference_578': {
        'long_name': 'Reference Intensity at 578 nm',
        'comment': ('Optical absorbance reference intensity at 578 nm. Reference and signal intensities range '
                    'between 0 and 4096. Values should be greater than ~1500. Lower intensities will result in '
                    'higher noise in the absorbance and pH measurements.'),
        'units': 'count'
    },
    'signal_578': {
        'long_name': 'Signal Intensity at 578 nm',
        'comment': ('Optical absorbance signal intensity at 578 nm. Reference and signal intensities range between 0 ' +
                    'and 4096. Values should be greater than ~1500. Lower intensities will result in higher noise in ' +
                    'the absorbance and pH measurements.'),
        'data_product_identifier': 'PH578SI_L0',
        'units': 'count'
    },
    'record_number': {
        'long_name': 'IMM Record Number',
        'comment': 'Inductive modem record number',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'record_length': {
        'long_name': 'Record Length',
        'comment': 'Number of bytes in the record.',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'record_type': {
        'long_name': 'Record Type',
        'comment': 'Data and control record type. For the SAMI2-pH sensor, the record type is 10',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'comment': 'Derived from the SAMI-pH internal clock.',
        'units': 'seconds since 1970-01-01',
        'calendar': 'gregorian'
    },
    'raw_thermistor_start': {
        'long_name': 'Raw Thermistor Temperature, Measurement Start',
        'comment': 'Thermistor resistivity measured in counts at the start of the measurement cycle.',
        'units': 'count'
    },
    'raw_thermistor_end': {
        'long_name': 'Raw Thermistor Temperature, Measurement End',
        'comment': 'Thermistor resistivity measured in counts at the end of the measurement cycle.',
        'units': 'count'
    },
    'raw_battery_voltage': {
        'long_name': 'Raw Battery Voltage',
        'comment': ('Raw internal battery voltage measured in counts. May actually reflect external voltage if ' +
                    'external power is applied'),
        'units': 'count'
    },
    'thermistor_temperature_start': {
        'long_name': 'Thermistor Temperature, Measurement Start',
        'comment': ('Thermistor temperature refers to the internal instrument temperature of the pH sensor, as ' +
                    'measured by the thermistor. It is used to determine salinity and temperature dependent molar ' +
                    'absorptivities in the seawater sample in order to make an accurate pH estimation. This ' +
                    'variable represents the thermistor temperature measured at the beginning of the measurement ' +
                    'cycle'),
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius',
        'ancillary_variables': 'raw_thermistor_start'
    },
    'thermistor_temperature_end': {
        'long_name': 'Thermistor Temperature, Measurement End',
        'comment': ('Thermistor temperature refers to the internal instrument temperature of the pH sensor, as ' +
                    'measured by the thermistor. It is used to determine salinity and temperature dependent molar ' +
                    'absorptivities in the seawater sample in order to make an accurate pH estimation. This ' +
                    'variable represents the thermistor temperature measured at the end of the measurement cycle'),
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius',
        'ancillary_variables': 'raw_thermistor_end'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': ('Voltage of the internal battery pack. May actually reflect external voltage if ' +
                    'external power is applied'),
        'units': 'V',
        'ancillary_variables': 'raw_battery_voltage'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'comment': ('Difference between the internal clock and the external GPS-based data logger clock. Offset ' +
                    'can be used to determine instrument clock offset and drift over the course of a deployment'),
        'units': 'seconds',
        'ancillary_variables': 'record_time, time'
    },
    'pH': {
        'long_name': 'Seawater pH',
        'comment': ('pH is a measurement of the concentration of hydrogen ions in a solution. pH ranges from acidic ' +
                    'to basic on a scale from 0 to 14 with 7 being neutral.'),
        'standard_name': 'sea_water_ph_reported_on_total_scale',
        'data_product_identifier': 'PHWATER_L2',
        'units': '1',
        '_FillValue': np.nan,
        'ancillary_variables': ('blank_refrnc_434, blank_signal_434, blank_refrnc_578, blank_signal_578, ' +
                                'reference_434, signal_434, reference_578, signal_578, thermistor_temperature_start, ' +
                                'thermistor_temperature_end, salinity')
    }
}

# add the co-located CTD attributes to the PHSEN attributes
PHSEN = dict_update(PHSEN, CO_LOCATED)
