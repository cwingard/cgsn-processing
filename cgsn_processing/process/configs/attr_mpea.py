#!/usr/bin/env python
# _*_ coding: utf_8 _*_
"""
@package cgsn_processing.process.configs.attr_mpea
@file cgsn_processing/process/configs/attr_mpea.py
@author Christopher Wingard
@brief Attributes for the MPEA variables
"""
import numpy as np

MPEA = {
    'global': {
        'title': 'MFN Power Electronics Assembly (MPEA) Status Data',
        'summary': ('Measures the status of the power converters that supply 24 VDC to the different systems on the '
                    'MFN from the 380 VDC supplied by the PSC.'),
    },
    'main_voltage': {
        'long_name': 'Main Voltage',
        'standard_name': 'main_voltage',
        'comment': 'Input voltage supplied by the mooring PSC to the MPEA.'
    },
    'main_current': {
        'long_name': 'Main Current',
        'units': 'mA',
        'comment': 'Current draw of the MPEA from the power supplied by the mooring PSC.'
    },
    'error_flag1': {
        'long_name': 'Error Flag 1',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Error flags reported by the power system controller.',
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('no_error high_voltage_input_undervoltage high_voltage_input_overvoltage '
                          'high_voltage_input_power_sensor_fault mpm_internal_over_temp '
                          'mpea_hotel_power_coverter_over_temp 5v_hotel_power_undervoltage 5v_hotel_power_overvoltage '
                          'microcontroller_core_undervoltage microcontroller_core_overvoltage '
                          'hotel_power_status_sensor_fault mpea_reset_flag converter_1_input_overcurrent '
                          'converter_1_output_overvoltage converter_1_output_undervoltage '
                          'converter_1_output_overcurent converter_1_dc_converter_fault converter_1_input_sensor_fault '
                          'converter_1_output_sensor_fault converter_2_input_overcurrent '
                          'converter_2_output_overvoltage converter_2_output_undervoltage '
                          'converter_2_output_overcurrent converter_2_dc_converter_fault '
                          'converter_2_input_sensor_fault converter_2_output_sensor_fault '
                          'converter_3_input_overcurrent converter_3_output_overvoltage '
                          'converter_3_output_undervoltage converter_3_output_overcurrent '
                          'converter_3_dc_converter_fault converter_3_input_sensor_fault '
                          'converter_3_output_sensor_fault')
    },
    'error_flag2': {
        'long_name': 'Error Flag 2',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Error flags reported by the power system controller.',
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 7))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('no_error converter_4_input_overcurrent converter_4_output_overvoltage '
                          'converter_4_output_undervoltage converter_4_output_overcurrent '
                          'converter_4_dc_converter_fault converter_4_input_sensor_fault '
                          'converter_4_output_sensor_fault')
    },
    'cv1_state': {
        'long_name': 'Converter 1 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Indicates the power state (0: off, 1: on) of the converter.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'off on',
    },
    'cv1_voltage': {
        'long_name': 'Converter 1 Voltage',
        'units': 'V',
        'comment': 'Output voltage from the the converter.'
    },
    'cv1_current': {
        'long_name': 'Converter 1 Current',
        'units': 'mA',
        'comment': 'Current draw from the the converter.'
    },
    'cv2_state': {
        'long_name': 'Converter 1 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Indicates the power state (0: off, 1: on) of the converter.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'off on',
    },
    'cv2_voltage': {
        'long_name': 'Converter 2 Voltage',
        'units': 'V',
        'comment': 'Output voltage from the the converter.'
    },
    'cv2_current': {
        'long_name': 'Converter 2 Current',
        'units': 'mA',
        'comment': 'Current draw from the the converter.'
    },
    'auxiliary_state': {
        'long_name': 'Auxiliary Channel State',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Indicates the power state (0: off, 1: on) of the auxiliary channel.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'off on',
    },
    'auxiliary_voltage': {
        'long_name': 'Auxiliary Channel Voltage',
        'units': 'V',
        'comment': 'Auxiliary channel voltage.'
    },
    'auxiliary_current': {
        'long_name': 'Auxiliary Channel Current',
        'units': 'mA',
        'comment': 'Auxiliary current draw.'
    },
    'hotel_5v_voltage': {
        'long_name': '',
        'units': 'V',
        'comment': ''
    },
    'hotel_5v_current': {
        'long_name': '',
        'units': 'mA',
        'comment': ''
    },
    'temperature': {
        'long_name': 'Internal Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Temperature measured inside the MPEA pressure housing.'
    },
    'relative_humidity': {
        'long_name': 'Relative Humidity',
        'units': 'percent',
        'comment': ('Humidity measured inside the MPEA pressure housing. This value should be very low and should '
                    'remain stable for the duration of the deployment. Steadily rising humidity represents a leak.')
    },
    'leak_detect': {
        'long_name': 'Leak Detect Voltage',
        'units': 'mV',
        'comment': ('Measures resistance voltage across the sensor, which decreases in the presence of a '
                    'leak. Values less than 100 mV indicate a leak condition, values around 1250 mV indicate '
                    'normal conditions, and values greater than 2000 mV indicate an open circuit.')
    },
    'internal_pressure': {
        'long_name': 'Internal Pressure',
        'units': 'psi',
        'comment': ('Pressure measured inside the MPEA pressure housing. This value should be less than standard '
                    'pressure (assuming a vacuum was pulled while sealing the housing) and should remain stable for '
                    'the duration of the deployment. Steadily rising humidity represents a leak.')
    }
}
