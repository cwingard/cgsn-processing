#!/usr/bin/env python
# _*_ coding: utf_8 _*_
"""
@package cgsn_processing.process.configs.attr_pwrsys
@file cgsn_processing/process/configs/attr_psc.py
@author Christopher Wingard
@brief Attributes for the PSC variables
"""
import numpy as np

PSC = {
    'global': {
        'title': 'Mooring Power System Controller (PSC) Status Data',
        'summary': ('Measures the status of the mooring power system controller, encompassing the '
                    'batteries, recharging sources (wind and solar), and outputs.'),
    },
    'main_voltage': {
        'long_name': 'Main Voltage',
        'units': 'V',
        'comment': 'Output voltage supplied by the power system to the mooring.'
    },
    'main_current': {
        'long_name': 'Main Current',
        'units': 'mA',
        'comment': 'Electrical current supplied by the power system to the mooring.'
    },
    'percent_charge': {
        'long_name': 'Percent Charge',
        'units': 'percent',
        'comment': ('Estimated percent charge of the batteries. This value is often times incorrect and '
                    'should be used with some degree of caution, if not entirely ignored.')
    },
    'override_flag': {
        'long_name': 'Override Flag',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': ('List of power supply (CVT) or charging sources (e.g. solar panel 1) manually '
                    'connected directly either by the user or through the CPM1 mission file.'),
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 12))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('override_off wt1_connected wt2_connected sp1_connected sp2_connected sp3_connected '
                          'sp4_connected fc1_connected fc2_connected cvt_connected cvt_reset external_charger'),
        'ancillary_variables': ('main_voltage main_current wind_turbine1_current wind_turbine2_current '
                                'solar_panel1_current solar_panel2_current solar_panel3_current '
                                'solar_panel4_current cvt_voltage cvt_current external_current')
    },
    'error_flag1': {
        'long_name': 'Error Flag 1',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Error flags reported by the power system controller.',
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('no_error battery1_of_string1_overtemp battery2_of_string1_overtemp '
                          'battery1_of_string2_overtemp battery2_of_string2_overtemp '
                          'battery1_of_string3_overtemp battery2_of_string3_overtemp '
                          'battery1_of_string4_overtemp battery2_of_string4_overtemp '
                          'battery_string_1_fuse_blown battery_string_2_fuse_blown battery_string_3_fuse_blown '
                          'battery_string_4_fuse_blown battery_string_1_charging_sensor_fault '
                          'battery_string_1_discharging_sensor_fault battery_string_2_charging_sensor_fault '
                          'battery_string_2_discharging_sensor_fault battery_string_3_charging_sensor_fault '
                          'battery_string_3_discharging_sensor_fault battery_string_4_charging_sensor_fault '
                          'battery_string_4_discharging_sensor_fault pv1_sensor_fault pv2_sensor_fault '
                          'pv3_sensor_fault pv4_sensor_fault wt1_sensor_fault wt2_sensor_fault eeprom_access_fault '
                          'rtclk_access_fault external_power_sensor_fault psc_hotel_power_sensor_fault '
                          'psc_internal_overtemp_fault hipwr_dc_dc_converter_fuse_blown'),
        'ancillary_variables': 'main_voltage main_current'
    },
    'error_flag2': {
        'long_name': 'Error Flag 2',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Error flags reported by the power system controller.',
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('no_error buoy_24v_power_sensor_fault buoy_24v_power_over_voltage_fault '
                          'buoy_24v_power_under_voltage_fault fuse_5v_blown_non_critical wt1_control_relay_fault '
                          'wt2_control_relay_fault pv1_control_relay_fault pv2_control_relay_fault '
                          'pv3_control_relay_fault pv4_control_relay_fault fc1_control_relay_fault '
                          'fc2_control_relay_fault cvt_swg_fault cvt_general_fault psc_hard_reset_flag '
                          'psc_power_on_reset_flag wt1_fuse_blown wt2_fuse_blown pv1_fuse_blown pv2_fuse_blown '
                          'pv3_fuse_blown pv4_fuse_blown cvt_shut_down_due_to_low_input_voltage undefined '
                          'undefined undefined undefined undefined undefined undefined undefined undefined'),
        'ancillary_variables': 'main_voltage main_current'
    },
    'solar_panel1_state': {
        'long_name': 'Solar Panel 1 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State, either connected (1) or disconnected (0), of the charging source.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'solar_panel1_voltage solar_panel1_current'
    },
    'solar_panel1_voltage': {
        'long_name': 'Solar Panel 1 Voltage',
        'units': 'V',
        'comment': 'Charging source operating voltage.'
    },
    'solar_panel1_current': {
        'long_name': 'Solar Panel 1 Current',
        'units': 'mA',
        'comment': 'Charging source operating current.'
    },
    'solar_panel2_state': {
        'long_name': 'Solar Panel 2 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State, either connected (1) or disconnected (0), of the charging source.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'solar_panel2_voltage solar_panel2_current'
    },
    'solar_panel2_voltage': {
        'long_name': 'Solar Panel 2 Voltage',
        'units': 'V',
        'comment': 'Charging source operating voltage.'
    },
    'solar_panel2_current': {
        'long_name': 'Solar Panel 2 Current',
        'units': 'mA',
        'comment': 'Charging source operating current.'
    },
    'solar_panel3_state': {
        'long_name': 'Solar Panel 3 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State, either connected (1) or disconnected (0), of the charging source.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'solar_panel3_voltage solar_panel3_current'
    },
    'solar_panel3_voltage': {
        'long_name': 'Solar Panel 3 Voltage',
        'units': 'V',
        'comment': 'Charging source operating voltage.'
    },
    'solar_panel3_current': {
        'long_name': 'Solar Panel 3 Current',
        'units': 'mA',
        'comment': 'Charging source operating current.'
    },
    'solar_panel4_state': {
        'long_name': 'Solar Panel 4 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State, either connected (1) or disconnected (0), of the charging source.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'solar_panel4_voltage solar_panel4_current'
    },
    'solar_panel4_voltage': {
        'long_name': 'Solar Panel 4 Voltage',
        'units': 'V',
        'comment': 'Charging source operating voltage.'
    },
    'solar_panel4_current': {
        'long_name': 'Solar Panel 4 Current',
        'units': 'mA',
        'comment': 'Charging source operating current.'
    },
    'wind_turbine1_state': {
        'long_name': 'Wind Turbine 1 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State, either connected (1) or disconnected (0), of the charging source.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'wind_turbine1_voltage wind_turbine1_current'
    },
    'wind_turbine1_voltage': {
        'long_name': 'Wind Turbine 1 Voltage',
        'units': 'V',
        'comment': 'Charging source operating voltage.'
    },
    'wind_turbine1_current': {
        'long_name': 'Wind Turbine 1 Current',
        'units': 'mA',
        'comment': 'Charging source operating current.'
    },
    'wind_turbine2_state': {
        'long_name': 'Wind Turbine 2 State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State, either connected (1) or disconnected (0), of the charging source.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'wind_turbine2_voltage wind_turbine2_current'
    },
    'wind_turbine2_voltage': {
        'long_name': 'Wind Turbine 2 Voltage',
        'units': 'V',
        'comment': 'Charging source operating voltage.'
    },
    'wind_turbine2_current': {
        'long_name': 'Wind Turbine 2 Current',
        'units': 'mA',
        'comment': 'Charging source operating current.'
    },
    'battery_bank1_temperature': {
        'long_name': 'Battery Bank 1 Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Thermistor connected to battery terminal 1 in the base of the mooring well.'
    },
    'battery_bank1_voltage': {
        'long_name': 'Battery Bank 1 Voltage',
        'units': 'V',
        'comment': 'Battery bank 1 voltage supplied to the power system controller.'
    },
    'battery_bank1_current': {
        'long_name': 'Battery Bank 1 Current',
        'units': 'mA',
        'comment': ('Current draw from battery bank 1 by the power system controller. Negative current '
                    'indicates a charging current.')
    },
    'battery_bank2_temperature': {
        'long_name': 'Battery Bank 2 Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Thermistor connected to battery terminal 2 in the base of the mooring well.'
    },
    'battery_bank2_voltage': {
        'long_name': 'Battery Bank 2 Voltage',
        'units': 'V',
        'comment': 'Battery bank 2 voltage supplied to the power system controller.'
    },
    'battery_bank2_current': {
        'long_name': 'Battery Bank 2 Current',
        'units': 'mA',
        'comment': ('Current draw from battery bank 2 by the power system controller. Negative current '
                    'indicates a charging current.')
    },
    'battery_bank3_temperature': {
        'long_name': 'Battery Bank 3 Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Thermistor connected to battery terminal 3 in the base of the mooring well.'
    },
    'battery_bank3_voltage': {
        'long_name': 'Battery Bank 3 Voltage',
        'units': 'V',
        'comment': 'Battery bank 3 voltage supplied to the power system controller.'
    },
    'battery_bank3_current': {
        'long_name': 'Battery Bank 3 Current',
        'units': 'mA',
        'comment': ('Current draw from battery bank 3 by the power system controller. Negative current '
                    'indicates a charging current.')
    },
    'battery_bank4_temperature': {
        'long_name': 'Battery Bank 4 Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Thermistor connected to battery terminal 4 in the base of the mooring well.'
    },
    'battery_bank4_voltage': {
        'long_name': 'Battery Bank 4 Voltage',
        'units': 'V',
        'comment': 'Battery bank 4 voltage supplied to the power system controller.'
    },
    'battery_bank4_current': {
        'long_name': 'Battery Bank 4 Current',
        'units': 'mA',
        'comment': ('Current draw from battery bank 4 by the power system controller. Negative current '
                    'indicates a charging current.')
    },
    'external_voltage': {
        'long_name': 'External Voltage',
        'units': 'V',
        'comment': 'External charger operating voltage.'
    },
    'external_current': {
        'long_name': 'External Current',
        'units': 'mA',
        'comment': 'Charging current supplied by the external battery charger.'
    },
    'internal_voltage': {
        'long_name': 'Internal Voltage',
        'units': 'V',
        'comment': 'Voltage level used by the power system controller.'
    },
    'internal_current': {
        'long_name': 'Internal Current',
        'units': 'mA',
        'comment': 'Current draw used by the power system controller.'
    },
    'internal_temperature': {
        'long_name': 'Internal Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Temperature inside the power system controller enclosure.'
    },
    'seawater_ground_state': {
        'long_name': 'Sea Water Ground State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'seawater ground monitoring, either enabled (1) or disabled (0).',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disabled enabled',
        'ancillary_variables': 'main_voltage main_current'
    },
    'seawater_ground_positve': {
        'long_name': 'Sea Water Ground Positive',
        'units': 'uA',
        'comment': 'Measured positive seawater ground.'
    },
    'seawater_ground_negative': {
        'long_name': 'Sea Water Ground Negative',
        'units': 'uA',
        'comment': 'Measured negative seawater ground.'
    },
    'cvt_state': {
        'long_name': 'CVT State',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'State of the CVT, either connected (1) or disconnected (0).',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'cvt_voltage cvt_current cvt_interlock cvt_temperature'
    },
    'cvt_voltage': {
        'long_name': 'CVT Voltage',
        'units': 'V',
        'comment': 'CVT voltage supplied to the MFN by the power system controller, nominally 380 VDC.'
    },
    'cvt_current': {
        'long_name': 'CVT Current',
        'units': 'mA',
        'comment': 'Current draw from the CVT by the MFN.'
    },
    'cvt_interlock': {
        'long_name': 'CVT Interlock',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'CVT interlock is connected (1) or disconnected (0) by the shorting plug.',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'disconnected connected',
        'ancillary_variables': 'cvt_state cvt_voltage cvt_current cvt_temperature'
    },
    'cvt_temperature': {
        'long_name': 'CVT Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Temperature measured on the CVT board.'
    },
    'error_flag3': {
        'long_name': 'Error Flag 3',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Error flags reported by the power system controller.',
        'flag_mask': np.hstack(np.array([0, 2 ** np.array(range(0, 32))], dtype=object)).astype(np.uintc),
        'flag_meanings': ('no_error cvt_board_temp_over_100C interlock_output_supply_fuse_blown '
                          'interlock_status_1_supply_fuse_blown interlock_status_2_supply_fuse_blown '
                          'input_1_fuse_blown input_2_fuse_blown input_3_fuse_blown input_4_fuse_blown '
                          'over_5v_voltage under_5v_voltage output_sensor_circuit_power_over_voltage '
                          'output_sensor_circuit_power_under_voltage p_swgf_sensor_circuit_power_over_voltage '
                          'p_swgf_sensor_circuit_power_under_voltage n_swgf_sensor_circuit_power_over_voltage '
                          'n_swgf_sensor_circuit_power_under_voltage raw_24v_input_power_sensor_fault '
                          'cvt_24v_hotel_power_sensor_fault interlock_supply_output_sensor_fault '
                          'interlock_status_1_sensor_fault interlock_status_2_sensor_fault '
                          'interlock_input_sensor_fault p_swgf_occured n_swgf_occured input_1_sensor_fault '
                          'input_2_sensor_fault input_3_sensor_fault input_4_sensor_fault '
                          'high_voltage_output_current_sensor_fault high_voltage_output_voltage_sensor_fault '
                          'p_swgf_sensor_fault n_swgf_sensor_fault'),
        'ancillary_variables': 'main_voltage main_current'
    }
}
