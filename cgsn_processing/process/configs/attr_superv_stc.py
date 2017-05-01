#!/usr/bin/env python
# _*_ coding: utf_8 _*_
"""
@package cgsn_processing.process.configs.attr_superv_stc
@file cgsn_processing/process/configs/attr_superv_stc.py
@author Christopher Wingard
@brief Attributes for the STC Supervisor variables
"""
SUPERV = {
    'deploy_id': {
        'long_name': 'Deployment ID',
        'standard_name': 'deployment_id',
        'units': '1',
        'coordinates': 'time z latitude longitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'stc_date_time_string': {
        'long_name': 'STC Date and Time Stamp',
        'standard_name': 'stc_date_time_string',
        'units': '1',
        'coordinates': 'time z latitude longitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'main_voltage': {
        'long_name': 'Main Voltage',
        'standard_name': 'main_voltage',
        'units': 'V'
         },
    'main_current': {
        'long_name': 'Main Current',
        'standard_name': 'main_current',
        'units': 'mA'
    },
    'error_flags1': {
        'standard_name': 'error_flags1',
        'units': '1'
    },
    'error_flags2': {
        'standard_name': 'error_flags2',
        'units': '1'
    },
    'temperature1': {
        'standard_name': 'temperature1',
        'units': 'degrees_Celsius'
    },
    'temperature2': {
        'standard_name': 'temperature2',
        'units': 'degrees_Celsius'
    },
    'humidity': {
        'long_name': 'Relative Humidity',
        'standard_name': 'relative_humidity',
        'units': '%'
    },
    'pressure': {
        'long_name': 'Absolute Pressure',
        'standard_name': 'absolute_pressure',
        'units': 'dbar'
    },
    'ground_fault_enable': {
        'standard_name': 'ground_fault_enable',
        'units': '1'
    },
    'ground_fault_sbd': {
        'standard_name': 'ground_fault_sbd',
        'units': 'uA'
    },
    'ground_fault_gps': {
        'standard_name': 'ground_fault_gps',
        'units': 'uA'
    },
    'ground_fault_main': {
        'standard_name': 'ground_fault_main',
        'units': 'uA'
    },
    'ground_fault_9522_fw': {
        'standard_name': 'ground_fault_9522_fw',
        'units': 'uA'
    },
    'leak_detect_enable': {
        'standard_name': 'leak_detect_enable',
        'units': '1'
    },
    'leak_detect_voltage1': {
        'standard_name': 'leak_detect_voltage1',
        'units': 'mV'
    },
    'leak_detect_voltage2': {
        'standard_name': 'leak_detect_voltage2',
        'units': 'mV'
    },
    'heartbeat_enable': {
        'standard_name': 'heartbeat_enable',
        'units': '1'
    },
    'heartbeat_delta': {
        'standard_name': 'heartbeat_delta',
        'units': '1'
    },
    'heartbeat_threshold': {
        'standard_name': 'heartbeat_threshold',
        'units': '1'
    },
    'wake_code': {
        'standard_name': 'wake_code',
        'units': '1'
    },
    'iridium_power_state': {
        'standard_name': 'iridium_power_state',
        'units': '1'
    },
    'iridium_voltage': {
        'standard_name': 'iridium_voltage',
        'units': 'mV'
    },
    'iridium_current': {
        'standard_name': 'iridium_current',
        'units': 'mA'
    },
    'iridium_error_flag': {
        'standard_name': 'iridium_error_flag',
        'units': '1'
    },
    'fwwf_power_state': {
        'standard_name': 'fwwf_power_state',
        'units': '1'
    },
    'fwwf_voltage': {
        'standard_name': 'fwwf_voltage',
        'units': 'mV'
    },
    'fwwf_current': {
        'standard_name': 'fwwf_current',
        'units': 'mA'
    },
    'fwwf_power_flag': {
        'standard_name': 'fwwf_power_flag',
        'units': '1'
    },
    'gps_power_state': {
        'standard_name': 'gps_power_state',
        'units': '1'
    },
    'sbd_power_state': {
        'standard_name': 'sbd_power_state',
        'units': '1'
    },
    'sbd_message_pending': {
        'standard_name': 'sbd_message_pending',
        'units': '1'
    },
    'pps_source': {
        'standard_name': 'pps_source',
        'units': '1'
    },
    'imm_power_state': {
        'standard_name': 'dcl_power_state',
        'units': '1'
    },
    'wake_time_count': {
        'standard_name': 'wake_time_count',
        'units': '1'
    },
    'wake_power_count': {
        'standard_name': 'wake_power_count',
        'units': '1'
    },
    'esw_power_state': {
        'standard_name': 'esw_power_state',
        'units': '1'
    },
    'dsl_power_state': {
        'standard_name': 'dsl_power_state',
        'units': '1'
    },
    'port1_power_state': {},
    'port1_voltage': {
        'units': 'mV'
    },
    'port1_current': {
        'units': 'mA'
    },
    'port1_error_flag': {},
    'port2_power_state': {},
    'port2_voltage': {
        'units': 'mV'
    },
    'port2_current': {
        'units': 'mA'
    },
    'port2_error_flag': {},
    'port3_power_state': {},
    'port3_voltage': {
        'units': 'mV'
    },
    'port3_current': {
        'units': 'mA'
    },
    'port3_error_flag': {},
    'port5_power_state': {},
    'port5_voltage': {
        'units': 'mV'
    },
    'port5_current': {
        'units': 'mA'
    },
    'port5_error_flag': {},
    'port7_power_state': {},
    'port7_voltage': {
        'units': 'mV'
    },
    'port7_current': {
        'units': 'mA'
    },
    'port7_error_flag': {}
}
