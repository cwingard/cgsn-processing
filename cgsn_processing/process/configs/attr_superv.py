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
        # common dataset attributes from the parsed data
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
            'comment': ('Absolute pressure inside the platcon or pressure housing. Operators will pull a vacuum to '
                        'provide early indications of a leak prior to deployment '
                        'at sea.')
        },
        'leak_detect_enable': {
            'long_name': 'Leak Detects Enabled',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Status flag indicating which, if any, of the leak detects are enabled. Valid values '
                        'are 0: leak detects disabled, 1: leak detect 1 enabled, 2: leak detect 2 enabled, '
                        'and 3: leak detects 1 and 2 enabled.'),
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': ('leak_detects_disabled leak_detect_1_enabled leak_detect_2_enabled '
                              'leak_detects_1_and_2_enabled'),
            'ancillary_variables': 'leak_detect_voltage1 leak_detect_voltage2'
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
        'heartbeat_enable': {
            'long_name': 'Heartbeat Enabled',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Status flag indicating whether the heartbeat is enabled or not. Valid values are '
                        '0: heartbeat disabled, 1: heartbeat enabled'),
            'flag_values': np.intc([0, 1]),
            'flag_meanings': ('heartbeat_disabled heartbeat_enabled'),
            'ancillary_variables': 'heartbeat_delta heartbeat_threshold'
        },
        'heartbeat_delta': {
            'long_name': 'Heartbeat Delta',
            'units': 's',
            'comment': 'The time, in seconds, between heartbeats'
        },
        'heartbeat_threshold': {
            'long_name': 'Heartbeat Threshold',
            'units': 'count',
            'comment': 'The max number of heartbeats that can be missed before the system will force a reboot.'
        },
        'wake_code': {
            'long_name': 'Wake Code',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Wake code indicating what caused the CE to turn on.',
            'flag_values': np.intc([0, 1, 2, 4, 8, 16, 32, 64, 128]),
            'flag_meanings': ('no_wake_code cold_start alarm_wakeup_from_ce wakeup_from_sbd wakeup_from_dcl '
                              'mpic_watchdog psc_error wakeup_from_imm hbeat_error'),
            'ancillary_variables': 'wake_time_count wake_power_count'
        },
        'wake_time_count': {
            'long_name': 'Wake Time Count',
            'units': 'hours',
            'comment': 'Time between power cycles. Note, this value does not seem to be set in the data file.'
        },
        'wake_power_count': {
            'long_name': 'Wake Power Count',
            'units': 'count',
            'comment': 'The number of times the computational element has been power cycled.'
        }
    },
    # attributes found in the CPM supervisor logs
    'cpm': {
        'global': {
            'title': 'Communications and Power Module (CPM) Supervisor Data',
            'summary': ('Measures the status of the CPM based on the voltage levels, current draws, '
                        'leak detects and the state of attached communication devices.')
        },
        'backup_battery_voltage': {
            'long_name': 'Backup Battery Voltage',
            'units': 'V',
            'comment': 'Voltage of the backup battery.'
        },
        'backup_battery_current': {
            'long_name': 'Backup Battery Current',
            'units': 'mA',
            'comment': 'Current draw from the backup battery.'
        },
        'error_flags': {
            'long_name': 'CPM Error Flags',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Error flags for the CPM supervisor data. The flags are tied to the main voltage and current '
                        'variables for the purposes of this data set, however they are independently applicable to '
                        'multiple variables in the supervisor data set.'),
            'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
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
                              'cpm_dead_recommend_switchover channel_pic_over_current mpic_brown-out_reset'),
            'ancillary_variables': 'main_voltage main_current'
        },
        'ground_fault_enable': {
            'long_name': 'Ground Faults Enabled',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'List of enabled ground fault detection systems for the CPM.',
            'flag_masks': np.hstack(np.array([0, 2 ** np.array(range(0, 4))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('not_enabled sbd_enabled gps_enabled main_voltage_enabled fwwf_enabled'),
            'ancillary_variables': 'ground_fault_sbd ground_fault_gps ground_fault_main ground_fault_9522_fw'
        },
        'ground_fault_sbd': {
            'long_name': 'Ground Fault SBD',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_gps': {
            'long_name': 'Ground Fault GPS',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_main': {
            'long_name': 'Ground Fault Main',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_9522_fw': {
            'long_name': 'Ground Fault Iridium and Freewave',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'iridium_power_state': {
            'long_name': 'Iridium Modem Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the Iridium modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'iridium_voltage iridium_current iridium_error_flag'
        },
        'iridium_voltage': {
            'long_name': 'Iridium Modem Voltage',
            'units': 'V',
            'comment': 'Voltage supplied to power on the Iridium modem (approximately 12 VDC).'
        },
        'iridium_current': {
            'long_name': 'Iridium Modem Current',
            'units': 'mA',
            'comments': 'Current supplied to the Iridium modem.'
        },
        'iridium_error_flag': {
            'long_name': 'Iridium Error Flag',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists',
            'ancillary_variables': 'iridium_power_state iridium_voltage iridium_current'
        },
        'fwwf_power_state': {
            'long_name': 'Freewave and WiFi Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Status flag indicating which, if any, of the freewave and WiFi power ports are enabled. '
                        'Valid values are 0: power disabled, 1: freewave power enabled, 2: WiFi power enabled, '
                        'and 3: freewave and WiFI power enabled.'),
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': 'freewave_and_wifi_disabled freewave_enabled wifi_enabled freewave_and_wifi_enabled',
            'ancillary_variables': 'fwwf_voltage fwwf_current fwwf_power_flag'
        },
        'fwwf_voltage': {
            'long_name': 'Freewave and WiFi Voltage',
            'units': 'V',
            'comment': 'Voltage supplied to the Freewave and WiFi power ports.'
        },
        'fwwf_current': {
            'long_name': 'Freewave and WiFi Current',
            'units': 'mA',
            'comment': 'Current draw from the Freewave and WiFi power ports.'
        },
        'fwwf_power_flag': {
            'long_name': 'Freewave and WiFi Error Flag',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Indicates whether there is an error condition (0: no error, 1: error) with power to the '
                        'freewave or WiFi modems.'),
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists',
            'ancillary_variables': 'fwwf_power_state fwwf_voltage fwwf_current'
        },
        'gps_power_state': {
            'long_name': 'GPS Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the GPS sensor.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'main_voltage main_current'
        },
        'sbd_power_state': {
            'long_name': 'SBD Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the SBD modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'main_voltage main_current'
        },
        'sbd_message_pending': {
            'long_name': 'Pending SBD Messages',
            'units': 'count',
            'comment': 'Number of pending SBD messages to download and process.'
        },
        'pps_source': {
            'long_name': 'PPS Source',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the source for the pulse per second (PPS) signal used to manage the CE clocks.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'GPS seascan_oscillator',
            'ancillary_variables': 'gps_power_state'
        },
        'dcl_power_state': {
            'long_name': 'DCL Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Flags indicating which of the 7 DCL ports are powered on/off',
            'flag_masks': np.hstack(np.array([0, 2 ** np.array(range(0, 7))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('all_dcls_powered_off dcl_1_powered_on dcl_2_powered_on dcl_3_powered_on'
                              'dcl_4_powered_on dcl_5_powered_on dcl_6_powered_on dcl_7_powered_on'),
            'ancillary_variables': 'main_voltage main_current'
        },
        'esw_power_state': {
            'long_name': 'Ethernet Switch Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Status flag indicating which, if any, of the ethernet switches are enabled. Valid values '
                        'are 0: power disabled, 1: ethernet switch 1 enabled, 2: ethernet switch 2 enabled, and '
                        '3: both ethernet switches enabled.'),
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': 'ethernet_switches_disabled ethernet_switch_1_enabled ethernet_switch_2_enabled '
                             'ethernet_switch_1_and_2_enabled',
            'ancillary_variables': 'main_voltage main_current'
        },
        'dsl_power_state': {
            'long_name': 'DSL Modem Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the DSL modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'main_voltage main_current'
        }
    },
    'dcl': {
        # global and coordinate attributes
        'global': {
            'title': 'Data Concentrator Logger (DCL) Supervisor Data',
            'summary': ('Measures the status of the DCL based on the voltage levels, current draws, '
                        'leak detects and the state of the instrument ports.')
        },
        'error_flags': {
            'long_name': 'DCL Error Flags',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Error flags for the DCL supervisor data. The flags are tied to the main voltage and current '
                        'variables for the purposes of this data set, however they are independently applicable to '
                        'multiple variables in the supervisor data set.'),
            'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('no_errors vmain_out_of_normal_range imain_out_of_normal_range '
                              'iseawater_gflt_iso3v3_pos_out_of_allowable_range '
                              'iseawater_gflt_iso3v3_gnd_out_of_allowable_range '
                              'iseawater_gflt_vmain_pos_out_of_allowable_range '
                              'iseawater_gflt_vmain_gnd_out_of_allowawble_range '
                              'iseawater_gflt_inst_pos_out_of_allowable_range '
                              'iseawater_gflt_inst_gnd_out_of_allowable_range '
                              'iseawater_out_of_allowable_range_for_voltage_src_4_v '
                              'iseawater_out_of_allowable_range_for_voltage_src_4_gnd '
                              'leak_0_voltage_exceeded_limit '
                              'leak_1_voltage_exceeded_limit chpic_overcurrent_fault_exists '
                              'chpic_addr_1_not_responding chpic_addr_2_not_responding chpic_addr_3_not_responding '
                              'chpic_addr_4_not_responding chpic_addr_5_not_responding chpic_addr_6_not_responding '
                              'chpic_addr_7_not_responding chpic_addr_8_not_responding i2c_error uart_error '
                              'undefined undefined undefined undefined undefined undefined undefined '
                              'mpic_brown-out_reset'),
            'ancillary_variables': 'main_voltage main_current'
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
        'ground_fault_enable': {
            'long_name': 'Ground Faults Enabled',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'List of enabled ground fault detection systems for the DCL.',
            'flag_masks': np.hstack(np.array([0, 2 ** np.array(range(0, 3))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('not_enabled iso_voltage_3.3v_enabled main_voltage_enabled sensors_enabled'),
            'ancillary_variables': 'ground_fault_isov3 ground_fault_main ground_fault_sensors'
        },
        'ground_fault_isov3': {
            'long_name': 'Ground Fault Isolated Voltage',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_main': {
            'long_name': 'Ground Fault Main',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_sensors': {
            'long_name': 'Ground Fault Sensors',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'port1_power_state': {
            'long_name': 'Port 1 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port1_voltage port1_current port1_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port1_power_state port1_voltage port1_current'
        },
        'port2_power_state': {
            'long_name': 'Port 2 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port2_voltage port2_current port2_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port2_power_state port2_voltage port2_current'
        },
        'port3_power_state': {
            'long_name': 'Port 3 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port3_voltage port3_current port3_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port3_power_state port3_voltage port3_current'
        },
        'port4_power_state': {
            'long_name': 'Port 4 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port4_voltage port4_current port4_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port4_power_state port4_voltage port4_current'
        },
        'port5_power_state': {
            'long_name': 'Port 5 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port5_voltage port5_current port5_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port5_power_state port5_voltage port5_current'
        },
        'port6_power_state': {
            'long_name': 'Port 6 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port6_voltage port6_current port6_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port6_power_state port6_voltage port6_current'
        },
        'port7_power_state': {
            'long_name': 'Port 7 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port7_voltage port7_current port7_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port7_power_state port7_voltage port7_current'
        },
        'port8_power_state': {
            'long_name': 'Port 8 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port8_voltage port8_current port8_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port8_power_state port8_voltage port8_current'
        },
        'power_state': {
            'long_name': 'Power Board State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'State of the DCL dual power boards indicating use of the low and/or high power boards.',
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': 'power_board_off low_power high_power low_and_high_power',
            'ancillary_variables': ('power_board_mode power_voltage_select power_voltage_main power_current_main '
                                    'power_voltage_12 power_current_12 power_voltage_24 power_current_24')
        },
        'power_board_mode': {
            'long_name': 'Dual Power Board Mode',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Dual power board mode. Default is I2C mode (2).',
            'flag_values': np.intc([0, 1, 2]),
            'flag_meanings': 'power_board_off legacy_gio_mode i2c_mode',
            'ancillary_variables': ('power_state power_voltage_select power_voltage_main power_current_main '
                                    'power_voltage_12 power_current_12 power_voltage_24 power_current_24')
        },
        'power_voltage_select': {
            'long_name': 'Dual Power Board Voltage Selected',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Voltage source selected by the power board',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'power_board_off low_power lower_power high_power undefined',
            'ancillary_variables': ('power_state power_board_mode power_voltage_main power_current_main '
                                    'power_voltage_12 power_current_12 power_voltage_24 power_current_24')
        },
        'power_voltage_main': {
            'long_name': 'Dual Power Board Main Voltage',
            'units': 'V',
            'comment': 'Voltage supplied to the dual power board.'
        },
        'power_current_main': {
            'long_name': 'Dual Power Board Main Current',
            'units': 'mA',
            'comment': 'Current draw by the dual power board.'
        },
        'power_voltage_12': {
            'long_name': '12 V Power Supply Voltage',
            'units': 'V',
            'comment': 'Voltage supplied by the 12 V power supply.'
        },
        'power_current_12': {
            'long_name': '12 V Power Supply Current',
            'units': 'mA',
            'comment': 'Current draw from the 12 V power supply.'
        },
        'power_voltage_24': {
            'long_name': '24 V Power Supply Voltage',
            'units': 'V',
            'comment': 'Voltage supplied by the 24 V power supply.'
        },
        'power_current_24': {
            'long_name': '24 V Power Supply Current',
            'units': 'mA',
            'comment': 'Current draw from the 24 V power supply.'
        }
    },
    'stc': {
        # global and coordinate attributes
        'global': {
            'title': 'Simple Telemetry Controller (STC) Supervisor Data',
            'summary': ('Measures the status of the STC based on the voltage levels, current draws, '
                        'leak detects and the state of attached communication devices and instrument ports.')
        },
        'error_flags1': {
            'long_name': 'STC Error Flags Set 1',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('First set of error flags for the STC supervisor data. The flags are tied to the main voltage '
                        'and current variables for the purposes of this data set, however they are independently '
                        'applicable to multiple variables in the supervisor data set.'),
            'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('no_errors undefined undefined undefined undefined undefined undefined undefined '
                              'undefined undefined undefined undefined undefined undefined undefined undefined '
                              'undefined undefined undefined undefined undefined undefined undefined undefined '
                              'undefined undefined undefined undefined undefined undefined undefined undefined '
                              'undefined'),
            'ancillary_variables': 'main_voltage main_current'
        },
        'error_flags2': {
            'long_name': 'STC Error Flags Set 2',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Second set of error flags for the STC supervisor data. The flags are tied to the main '
                        'voltage and current variables for the purposes of this data set, however they are '
                        'independently applicable to multiple variables in the supervisor data set.'),
            'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('no_errors undefined undefined undefined undefined undefined undefined undefined '
                              'undefined undefined undefined undefined undefined undefined undefined undefined '
                              'undefined undefined undefined undefined undefined undefined undefined undefined '
                              'undefined undefined undefined undefined undefined undefined undefined undefined '
                              'undefined'),
            'ancillary_variables': 'main_voltage main_current'
        },
        'ground_fault_enable': {
            'long_name': 'Ground Faults Enabled',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'List of enabled ground fault detection systems for the STC.',
            'flag_masks': np.hstack(np.array([0, 2 ** np.array(range(0, 4))], dtype=object)).astype(np.uintc),
            'flag_meanings': ('not_enabled sbd_enabled gps_enabled sensors_enabled telemetry_enabled'),
            'ancillary_variables': 'ground_fault_sbd ground_fault_gps ground_fault_main ground_fault_9522_fw'
        },
        'ground_fault_sbd': {
            'long_name': 'Ground Fault SBD',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_gps': {
            'long_name': 'Ground Fault GPS',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_main': {
            'long_name': 'Ground Fault Main',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'ground_fault_9522_fw': {
            'long_name': 'Ground Fault Iridium and Freewave',
            'units': 'uA',
            'comment': 'Measured ground fault in uA. Absolute values less than 400 uA are considered normal.'
        },
        'iridium_power_state': {
            'long_name': 'Iridium Modem Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the Iridium modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'iridium_voltage iridium_current iridium_error_flag'
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
            'long_name': 'Iridium Error Flag',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates whether there is an error condition (0: no error, 1: error) with the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists',
            'ancillary_variables': 'iridium_power_state iridium_voltage iridium_current'
        },
        'fwwf_power_state': {
            'long_name': 'Freewave and WiFi Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Status flag indicating which, if any, of the freewave and WiFi power ports are enabled. '
                        'Valid values are 0: power disabled, 1: freewave power enabled, 2: WiFi power enabled, '
                        'and 3: freewave and WiFI power enabled.'),
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': 'freewave_and_wifi_disabled freewave_enabled wifi_enabled freewave_and_wifi_enabled',
            'ancillary_variables': 'fwwf_voltage fwwf_current fwwf_power_flag'
        },
        'fwwf_voltage': {
            'long_name': 'Freewave and WiFi Voltage',
            'units': 'V',
            'comment': 'Voltage supplied to the Freewave and WiFi power ports.'
        },
        'fwwf_current': {
            'long_name': 'Freewave and WiFi Current',
            'units': 'mA',
            'comment': 'Current draw from the Freewave and WiFi power ports.'
        },
        'fwwf_power_flag': {
            'long_name': 'Freewave and WiFi Error Flag',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Indicates whether there is an error condition (0: no error, 1: error) with power to the '
                        'freewave or WiFi modems.'),
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'no_error error_exists',
            'ancillary_variables': 'fwwf_power_state fwwf_voltage fwwf_current'
        },
        'gps_power_state': {
            'long_name': 'GPS Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the GPS sensor.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'main_voltage main_current'
        },
        'sbd_power_state': {
            'long_name': 'SBD Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the SBD modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'main_voltage main_current'
        },
        'sbd_message_pending': {
            'long_name': 'Pending SBD Messages',
            'units': 'count',
            'comment': 'Number of pending SBD messages to download and process.'
        },
        'pps_source': {
            'long_name': 'PPS Source',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the source for the pulse per second (PPS) signal used to manage the CE clocks.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'GPS seascan_oscillator',
            'ancillary_variables': 'gps_power_state'
        },
        'imm_power_state': {
            'long_name': 'IMM Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the inductive modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on'
        },
        'esw_power_state': {
            'long_name': 'Ethernet Switch Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': ('Status flag indicating which, if any, of the ethernet switches are enabled. Valid values '
                        'are 0: power disabled, 1: ethernet switch 1 enabled, 2: ethernet switch 2 enabled, and '
                        '3: both ethernet switches enabled.'),
            'flag_values': np.intc([0, 1, 2, 3]),
            'flag_meanings': 'ethernet_switches_disabled ethernet_switch_1_enabled ethernet_switch_2_enabled '
                             'ethernet_switch_1_and_2_enabled',
            'ancillary_variables': 'main_voltage main_current'
        },
        'dsl_power_state': {
            'long_name': 'DSL Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the DSL modem.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'main_voltage main_current'
        },
        'port1_power_state': {
            'long_name': 'Port 1 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port1_voltage port1_current port1_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port1_power_state port1_voltage port1_current'
        },
        'port2_power_state': {
            'long_name': 'Port 2 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port2_voltage port2_current port2_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port2_power_state port2_voltage port2_current'
        },
        'port3_power_state': {
            'long_name': 'Port 3 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port3_voltage port3_current port3_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port3_power_state port3_voltage port3_current'
        },
        'port5_power_state': {
            'long_name': 'Port 5 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port5_voltage port5_current port5_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port5_power_state port5_voltage port5_current'
        },
        'port7_power_state': {
            'long_name': 'Port 7 Power State',
            'standard_name': 'status_flag',
            'units': '1',
            'comment': 'Indicates the power state (0: off, 1: on) of the port.',
            'flag_values': np.intc([0, 1]),
            'flag_meanings': 'off on',
            'ancillary_variables': 'port7_voltage port7_current port7_error_flag'
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
            'units': '1',
            'comment': 'Indicates whether there is an error condition with the port.',
            'flag_values': np.intc([0, 1, 2, 3, 4]),
            'flag_meanings': 'no_error over_current no_comms not_configured serial_only',
            'ancillary_variables': 'port7_power_state port7_voltage port7_current'
        }
    }
}
