#!/usr/bin/env python
# _*_ coding: utf_8 _*_
"""
@package cgsn_processing.process.configs.attr_superv
@file cgsn_processing/process/configs/attr_superv.py
@author Christopher Wingard
@brief Attributes for the CPM, DCL and STC supervisor logs
"""
import numpy as np

SUPERV = {
    # attributes found in all the supervisor data sets
    'common': {
        # used for CF compliance and dimensioning
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
        # dataset attributes from the parsed data
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
        'temperature1': {
            'long_name': 'Temperature Sensor 1',
            'units': 'degrees_Celsius',
            'comment': 'Computational Element (CE) temperature sensor 1.'
        },
        'temperature2': {
            'long_name': 'Temperature Sensor 2',
            'units': 'degrees_Celsius',
            'comment': 'Computational Element (CE) temperature sensor 2.'
        },
        'humidity': {
            'long_name': 'Internal Humidity',
            'units': 'percent',
            'comment': ('Percent relative humidity inside the platcon or pressure housing. With the installation '
                       'of dessicant packs in the platcon or pressure housing, this value should be very low ('
                        'less than 25 percent).')
        },
        'pressure': {
            'long_name': 'Internal Pressure',
            'units': 'psi',
            'comment': ('Absolute pressure inside the platcon or pressure housing. For all pressure housings '
                        'operators will pull a vacuum to provide early indications of a leak prior to deployment '
                        'at sea.')
        },
        'ground_fault_enable': {
        },
        'leak_detect_enable': {
            'long_name': 'Leak Detects Enabled',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': ('Status flag indicating which, if any, of the leak detects are enabled. Valid values '
                        'are 0: leak detects disabled, 1: leak detect 1 enabled, 2: leak detect 2 enabled, '
                        'and 3: leak detects 1 and 2 enabled.'),
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': ('leak_detects_disabled leak_detect_1_enabled leak_detect_2_enabled '
                              'leak_detects_1_and_2_enabled')
        },
        'leak_detect_voltage1': {
            'long_name': 'Leak Detect 1 Voltage',
            'units': 'mV',
            'comment': ('Measures resistance voltage across the sensor, which decreases in the presence of a '
                        'leak. Values less than 100 mV indicate a leak condition, values around 1250 mV indicate '
                        'normal conditions, and values greater than 2000 mV indicate an open circuit.')
        },
        'leak_detect_voltage2': {
            'long_name': 'Leak Detect 2 Voltage',
            'units': 'mV',
            'comment': ('Measures resistance voltage across the sensor, which decreases in the presence of a '
                        'leak. Values less than 100 mV indicate a leak condition, values around 1250 mV indicate '
                        'normal conditions, and values greater than 2000 mV indicate an open circuit.')
        },
        'heartbeat_enable': {},
        'heartbeat_delta': {},
        'heartbeat_threshold': {},
        'wake_code': {
            'long_name': 'Wake Code',
            'standard_name': 'status_flag',
            'flag_masks': (2 ** np.array(range(0, 8))).astype(np.int8),
            'flag_meanings': ('cold_start alarm_wakeup_from_ce wakeup_from_sbd wakeup_from_dcl mpic_watchdog '
                              'psc_error wakeup_from_imm hbeat_error')
        },
        'wake_time_count': {},
        'wake_power_count': {},
    },
    'cpm': {
        # global and coordinate attributes
        'global': {
            'title': 'Communications and Power Module (CPM) Supervisor Data',
            'summary': ('Measures the status of the CPM based on the voltage levels, current draws, '
                        'leak detects and the state of attached communication devices.'),
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
        'backup_battery_voltage': {
            'units': 'V'
        },
        'backup_battery_current': {
            'units': 'mA'
        },
        'error_flags': {
            'long_name': 'CPM Error Flags',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': '',
            'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))])).astype(np.uintc),
            'flag_meanings': ('no_errors sbd_hardware_failure sbd_antenna_fault sbd_no_comms sbd_timeout_exceeded '
                              'sbd_bad_message_received main_v_out_of_range main_c_out_of_range bbatt_v_out_of_range '
                              'bbatt_c_out_of_range seascan_pps_fault gps_pps_fault wake_from_unknown_source '
                              'no_psc_data psc_main_v_and_main_v_disagree psc_main_c_and_main_c_disagree '
                              'no_cpm_heartbeat heartbeat_threshold_exceeded_power_cycling_cpm '
                              'iseawater_gflt_sbd_pos_out_of_allowable_range '
                              'iseawater_gflt_sbd_gnd_out_of_allowable_range '
                              'iseawater_gflt_gps_pos_out_of_allowable_range '
                              'iseawater_gflt_gps_gnd_out_of_allowable_range '
                              'iseawater_gflt_main_pos_out_of_allowable_range '
                              'iseawater_gflt_main_gnd_out_of_allowable_range '
                              'iseawater_gflt_9522_fw_pos_out_of_allowable_range '
                              'iseawater_gflt_9522_fw_gnd_out_of_allowable_range leak_det1_exceeded_limit '
                              'leak_det2_exceeded_limit i2c_communication_error uart_communication_error '
                              'cpm_dead_recommend_switchover channel_pic_over_current mpic_brown-out_reset')
        },
        'ground_fault_sbd': {
            'units': 'uA'
        },
        'ground_fault_gps': {
            'units': 'uA'
        },
        'ground_fault_main': {
            'units': 'uA'
        },
        'ground_fault_9522_fw': {
            'units': 'uA'
        },
        'iridium_power_state': {
        },
        'iridium_voltage': {
            'units': 'mV'
        },
        'iridium_current': {
            'units': 'mA'
        },
        'iridium_error_flag': {
        },
        'fwwf_power_state': {
        },
        'fwwf_voltage': {
            'units': 'mV'
        },
        'fwwf_current': {
            'units': 'mA'
        },
        'fwwf_power_flag': {
        },
        'gps_power_state': {
        },
        'sbd_power_state': {
        },
        'sbd_message_pending': {
        },
        'pps_source': {
        },
        'dcl_power_state': {
        },
        'esw_power_state': {
        },
        'dsl_power_state': {
        }
    },
    'dcl': {
        # global and coordinate attributes
        'global': {
            'title': 'Data Concentrator Logger (DCL) Supervisor Data',
            'summary': ('Measures the status of the DCL based on the voltage levels, current draws, '
                        'leak detects and the state of the instrument ports.'),
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
        'error_flags': {
            'long_name': 'DCL Error Flags',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': '',
            'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))])).astype(np.uintc),
            'flag_meanings': ('no_errors vmain_out_of_normal_range imain_out_of_normal_range '
                              'iseawater_gflt_iso3v3_pos_out_of_allowable_range '
                              'iseawater_gflt_iso3v3_gnd_out_of_allowable_range '
                              'iseawater_gflt_vmain_pos_out_of_allowable_range '
                              'iseawater_gflt_vmain_gnd_out_of_allowawble_range '
                              'iseawater_gflt_inst_pos_out_of_allowable_range '
                              'iseawater_gflt_inst_gnd_out_of_allowable_range '
                              'iseawater_out_of_allowable_range_for_voltage_src_4_v '
                              'iseawater_out_of_allowable_range_for_voltage_src_4_gnd leak_0_voltage_exceeded_limit '
                              'leak_1_voltage_exceeded_limit chpic_overcurrent_fault_exists '
                              'chpic_addr_1_not_responding chpic_addr_2_not_responding chpic_addr_3_not_responding '
                              'chpic_addr_4_not_responding chpic_addr_5_not_responding chpic_addr_6_not_responding '
                              'chpic_addr_7_not_responding chpic_addr_8_not_responding i2c_error uart_error '
                              'undefined undefined undefined undefined undefined undefined undefined '
                              'mpic_brown-out_reset')
        },
        'temperature3': {
            'long_name': 'Temperature Sensor 3',
            'units': 'degrees_Celsius',
            'comment': 'Computational Element (CE) temperature sensor 3.'
        },
        'temperature4': {
            'long_name': 'Temperature Sensor 4',
            'units': 'degrees_Celsius',
            'comment': 'Computational Element (CE) temperature sensor 4.'
        },
        'temperature5': {
            'long_name': 'Temperature Sensor 5',
            'units': 'degrees_Celsius',
            'comment': 'Computational Element (CE) temperature sensor 5.'
        },
        'ground_fault_isov3': {},
        'ground_fault_main': {},
        'ground_fault_sensors': {},
        'port1_power_state': {
            'long_name': 'Port 1 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port1_voltage': {
            'long_name': 'Port 1 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port1_current': {
            'long_name': 'Port 1 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port1_error_flag': {
            'long_name': 'Port 1 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port2_power_state': {
            'long_name': 'Port 2 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port2_voltage': {
            'long_name': 'Port 2 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port2_current': {
            'long_name': 'Port 2 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port2_error_flag': {
            'long_name': 'Port 2 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port3_power_state': {
            'long_name': 'Port 3 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port3_voltage': {
            'long_name': 'Port 3 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port3_current': {
            'long_name': 'Port 3 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port3_error_flag': {
            'long_name': 'Port 3 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port4_power_state': {
            'long_name': 'Port 4 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port4_voltage': {
            'long_name': 'Port 4 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port4_current': {
            'long_name': 'Port 4 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port4_error_flag': {
            'long_name': 'Port 4 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port5_power_state': {
            'long_name': 'Port 5 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port5_voltage': {
            'long_name': 'Port 5 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port5_current': {
            'long_name': 'Port 5 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port5_error_flag': {
            'long_name': 'Port 5 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port6_power_state': {
            'long_name': 'Port 6 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port6_voltage': {
            'long_name': 'Port 6 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port6_current': {
            'long_name': 'Port 6 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port6_error_flag': {
            'long_name': 'Port 6 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port7_power_state': {
            'long_name': 'Port 7 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port7_voltage': {
            'long_name': 'Port 7 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port7_current': {
            'long_name': 'Port 7 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port7_error_flag': {
            'long_name': 'Port 7 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port8_power_state': {
            'long_name': 'Port 8 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port8_voltage': {
            'long_name': 'Port 8 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port8_current': {
            'long_name': 'Port 8 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port8_error_flag': {
            'long_name': 'Port 8 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
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
            'summary': ('Measures the status of the STC based on the voltage levels, current draws, '
                        'leak detects and the state of attached communication devices and instrument ports.'),
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
        'error_flags1': {},
        'error_flags2': {},
        'ground_fault_sbd': {
            'units': 'uA'
        },
        'ground_fault_gps': {
            'units': 'uA'
        },
        'ground_fault_main': {
            'units': 'uA'
        },
        'ground_fault_9522_fw': {
            'units': 'uA'
        },
        'iridium_power_state': {
            'long_name': 'Iridium Modem Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the Iridium modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'iridium_voltage': {
            'long_name': 'Iridium Modem Voltage',
            'units': 'mV',
            'comment': 'Voltage supplied to power on the Iridium modem (approximately 12 VDC).'
        },
        'iridium_current': {
            'long_name': 'Iridium Modem Current',
            'units': 'mA',
            'comments': 'Current supplied to the Iridium modem.'
        },
        'iridium_error_flag': {
            'units': '1'
        },
        'fwwf_power_state': {
        },
        'fwwf_voltage': {
            'units': 'mV'
        },
        'fwwf_current': {
            'units': 'mA'
        },
        'fwwf_power_flag': {
        },
        'gps_power_state': {
            'long_name': 'GPS Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the GPS sensor.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'sbd_power_state': {
            'long_name': 'SBD Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the SBD modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'sbd_message_pending': {
        },
        'pps_source': {
        },
        'imm_power_state': {
            'long_name': 'IMM Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the inductive modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'esw_power_state': {
        },
        'dsl_power_state': {
            'long_name': 'DSL Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the DSL modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port1_power_state': {
            'long_name': 'Port 1 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port1_voltage': {
            'long_name': 'Port 1 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port1_current': {
            'long_name': 'Port 1 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port1_error_flag': {
            'long_name': 'Port 1 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port2_power_state': {
            'long_name': 'Port 2 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port2_voltage': {
            'long_name': 'Port 2 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port2_current': {
            'long_name': 'Port 2 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port2_error_flag': {
            'long_name': 'Port 2 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port3_power_state': {
            'long_name': 'Port 3 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port3_voltage': {
            'long_name': 'Port 3 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port3_current': {
            'long_name': 'Port 3 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port3_error_flag': {
            'long_name': 'Port 3 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port5_power_state': {
            'long_name': 'Port 5 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port5_voltage': {
            'long_name': 'Port 5 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port5_current': {
            'long_name': 'Port 5 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port5_error_flag': {
            'long_name': 'Port 5 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        },
        'port7_power_state': {
            'long_name': 'Port 7 Power State',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'port7_voltage': {
            'long_name': 'Port 7 Voltage',
            'units': 'V',
            'comment': 'Port power voltage level'
        },
        'port7_current': {
            'long_name': 'Port 7 Current',
            'units': 'mA',
            'comment': 'Port power current draw'
        },
        'port7_error_flag': {
            'long_name': 'Port 7 Error Flag',
            'standard_name': 'status_flag',
            #'units': ''    # deliberately left blank, no units for this value,
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists'
        }
    }
}
