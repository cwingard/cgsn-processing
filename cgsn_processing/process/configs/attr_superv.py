#!/usr/bin/env python
# _*_ coding: utf_8 _*_
"""
@package cgsn_processing.process.configs.attr_superv_cpm
@file cgsn_processing/process/configs/attr_superv.py
@author Christopher Wingard
@brief Attributes for the CPM Supervisor variables
"""

SUPERV = {
    'cpm': {
        # global and coordinate attributes
        'global': {
            'title': 'Communications and Power Module (CPM) Supervisor Data',
            'summary': (
                'Measures the status of the CPM based on the voltage levels, current draws, leak detects and the '
                'state of attached communication devices.'
            ),
            'project': 'Ocean Observatories Initiative',
            'institution': 'Coastal and Global Scale Nodes (CGSN)',
            'acknowledgement': 'National Science Foundation',
            'references': 'http://oceanobservatories.org',
            'creator_name': 'Ocean Observatories Initiative',
            'creator_email': 'helpdesk@oceanobservatories.org',
            'creator_url': 'http://oceanobservatories.org',
            'featureType': 'timeSeries',
            'cdm_data_type': 'Station',
            'Conventions': 'CF-1.7'
        },
        'deploy_id': {
            'long_name': 'Deployment ID',
            'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                        'allowing for overlapping deployments in the data sets.')
        },
        'station': {
            'cf_role': 'timeseries_id',
            'long_name': 'Station Name',
        },
        'time': {
            'long_name': 'Time',
            'standard_name': 'time',
            'units': 'seconds since 1970-01-01 00:00:00.00',
            'axis': 'T',
            'calendar': 'gregorian',
            'comment': 'Derived from the GPS referenced clock used by the CPM system.'
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
        # dataset attributes --> parsed data
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
        'backup_battery_voltage': {
            'standard_name': 'backup_battery_voltage',
            'units': 'V'
        },
        'backup_battery_current': {
            'standard_name': 'backup_battery_current',
            'units': 'mA'
        },
        'error_flags': {
            'standard_name': 'error_flags',
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
            'units': 'psi'
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
        'dcl_power_state': {
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
        }
    },
    'dcl': {
        # global and coordinate attributes
        'global': {
            'title': 'Data Concentrator Logger (DCL) Supervisor Data',
            'summary': (
                'Measures the status of the DCL based on the voltage levels, current draws, leak detects and the '
                'state of instrument ports.'
            ),
            'project': 'Ocean Observatories Initiative',
            'institution': 'Coastal and Global Scale Nodes (CGSN)',
            'acknowledgement': 'National Science Foundation',
            'references': 'http://oceanobservatories.org',
            'creator_name': 'Ocean Observatories Initiative',
            'creator_email': 'helpdesk@oceanobservatories.org',
            'creator_url': 'http://oceanobservatories.org',
            'featureType': 'timeSeries',
            'cdm_data_type': 'Station',
            'Conventions': 'CF-1.7'
        },
        'deploy_id': {
            'long_name': 'Deployment ID',
            'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                        'allowing for overlapping deployments in the data sets.')
        },
        'station': {
            'cf_role': 'timeseries_id',
            'long_name': 'Station Name',
        },
        'time': {
            'long_name': 'Time',
            'standard_name': 'time',
            'units': 'seconds since 1970-01-01 00:00:00.00',
            'axis': 'T',
            'calendar': 'gregorian',
            'comment': 'Derived from the GPS referenced clock used by the DCL data logger'
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
        # dataset attributes --> parsed data
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
        'error_flags': {},
        'temperature1': {},
        'temperature2': {},
        'temperature3': {},
        'temperature4': {},
        'temperature5': {},
        'humidity': {},
        'pressure': {},
        'ground_fault_enable': {},
        'ground_fault_isov3': {},
        'ground_fault_main': {},
        'ground_fault_sensors': {},
        'leak_detect_enable': {},
        'leak_detect_voltage1': {},
        'leak_detect_voltage2': {},
        'port1_power_state': {},
        'port1_voltage': {},
        'port1_current': {},
        'port1_error_flag': {},
        'port2_power_state': {},
        'port2_voltage': {},
        'port2_current': {},
        'port2_error_flag': {},
        'port3_power_state': {},
        'port3_voltage': {},
        'port3_current': {},
        'port3_error_flag': {},
        'port4_power_state': {},
        'port4_voltage': {},
        'port4_current': {},
        'port4_error_flag': {},
        'port5_power_state': {},
        'port5_voltage': {},
        'port5_current': {},
        'port5_error_flag': {},
        'port6_power_state': {},
        'port6_voltage': {},
        'port6_current': {},
        'port6_error_flag': {},
        'port7_power_state': {},
        'port7_voltage': {},
        'port7_current': {},
        'port7_error_flag': {},
        'port8_power_state': {},
        'port8_voltage': {},
        'port8_current': {},
        'port8_error_flag': {},
        'heartbeat_enable': {},
        'heartbeat_delta': {},
        'heartbeat_threshold': {},
        'wake_code': {},
        'wake_time_count': {},
        'wake_power_count': {},
        'power_state': {},
        'power_board_mode': {},
        'power_voltage_select': {},
        'power_voltage_main': {},
        'power_current_main': {},
        'power_voltage_12': {},
        'power_current_12': {},
        'power_voltage_24': {},
        'power_current_24': {},
    },
    'stc': {
        # global and coordinate attributes
        'global': {
            'title': 'Simple Telemetry Controller (STC) Supervisor Data',
            'summary': (
                'Measures the status of the STC based on the voltage levels, current draws, leak detects and the '
                'state of attached communication devices and instrument ports.'
            ),
            'project': 'Ocean Observatories Initiative',
            'institution': 'Coastal and Global Scale Nodes (CGSN)',
            'acknowledgement': 'National Science Foundation',
            'references': 'http://oceanobservatories.org',
            'creator_name': 'Ocean Observatories Initiative',
            'creator_email': 'helpdesk@oceanobservatories.org',
            'creator_url': 'http://oceanobservatories.org',
            'featureType': 'timeSeries',
            'cdm_data_type': 'Station',
            'Conventions': 'CF-1.7'
        },
        'deploy_id': {
            'long_name': 'Deployment ID',
            'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                        'allowing for overlapping deployments in the data sets.')
        },
        'station': {
            'cf_role': 'timeseries_id',
            'long_name': 'Station Name',
        },
        'time': {
            'long_name': 'Time',
            'standard_name': 'time',
            'units': 'seconds since 1970-01-01 00:00:00.00',
            'axis': 'T',
            'calendar': 'gregorian',
            'comment': 'Derived from the GPS referenced clock used by the STC data logger'
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
        # dataset attributes --> parsed data
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
}
