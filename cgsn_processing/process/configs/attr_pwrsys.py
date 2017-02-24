#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pwrsys
@file cgsn_processing/process/configs/attr_pwrsys.py
@author Christopher Wingard
@brief Attributes for the PWRSYS variables
"""

PWRSYS = {
    'deployment': {
        'long_name': 'Deployment Index',
        'standard_name': 'deployment_index',
        'units': '1',
        'coordinates': ''
    },
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude'
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
    'percent_charge': {
        'long_name': 'Percent Charge',
        'standard_name': 'percent_charge',
        'units': 'percent'
    },
    'override_flag': {
        'long_name': 'Override Flag',
        'standard_name': 'override_flag',
        'units': '1',
        'flag_masks': '0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024',
        'flag_meanings': 'no_override wt1 wt2 pv1 pv2 pv3 pv4 fc1 fc2 300v_control 300v_reset external_power'
    },
    'error_flag1': {
        'long_name': 'Error Flag 1',
        'standard_name': 'error_flag_1',
        'units': '1',
        'flag_masks': (
            '0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, '
            '131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, '
            '134217728, 268435456, 536870912, 1073741824, 2147483648'
        ),
        'flag_meanings': (
            'no_error '
            'battery1_of_string1_overtemp '
            'battery2_of_string1_overtemp '
            'battery1_of_string2_overtemp '
            'battery2_of_string2_overtemp '
            'battery1_of_string3_overtemp '
            'battery2_of_string3_overtemp '
            'battery1_of_string4_overtemp '
            'battery2_of_string4_overtemp '
            'battery_string_1_fuse_blown '
            'battery_string_2_fuse_blown '
            'battery_string_3_fuse_blown '
            'battery_string_4_fuse_blown '
            'battery_string_1_charging_sensor_fault '
            'battery_string_1_discharging_sensor_fault '
            'battery_string_2_charging_sensor_fault '
            'battery_string_2_discharging_sensor_fault '
            'battery_string_3_charging_sensor_fault '
            'battery_string_3_discharging_sensor_fault '
            'battery_string_4_charging_sensor_fault '
            'battery_string_4_discharging_sensor_fault '
            'pv1_sensor_fault '
            'pv2_sensor_fault '
            'pv3_sensor_fault '
            'pv4_sensor_fault '
            'wt1_sensor_fault '
            'wt2_sensor_fault '
            'eeprom_access_fault '
            'rtclk_access_fault '
            'external_power_sensor_fault '
            'psc_hotel_power_sensor_fault '
            'psc_internal_oververtemp_fault '
            '24v-300v_dc-dc_converter_fuse_blown'
        )
    },
    'error_flag2': {
        'long_name': 'Error Flag 2',
        'standard_name': 'error_flag_2',
        'units': '1',
        'flag_masks': (
            '0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, '
            '131072, 262144, 524288, 1048576, 2097152, 4194304'
        ),
        'flag_meanings': (
            'no_error '
            '24v_buoy_power_sensor_fault '
            '24v_buoy_power_over-voltage_fault '
            '24v_buoy_power_under-voltage_fault '
            '5v_fuse_blown_(non-critical) '
            'wt1_control_relay_fault '
            'wt2_control_relay_fault '
            'pv1_control_relay_fault '
            'pv2_control_relay_fault '
            'pv3_control_relay_fault '
            'pv4_control_relay_fault '
            'fc1_control_relay_fault '
            'fc2_control_relay_fault '
            'cvt_swg_fault '
            'cvt_general_fault '
            'psc_hard_reset_flag '
            'psc_power_on_reset_flag '
            'wt1_fuse_blown '
            'wt2_fuse_blown '
            'pv1_fuse_blown '
            'pv2_fuse_blown '
            'pv3_fuse_blown '
            'pv4_fuse_blown '
            'cvt_shut_down_due_to_low_input_voltage'
        )
    },
    'solar_panel1_state': {
        'long_name': 'Solar Panel 1 State',
        'standard_name': 'solar_panel_1_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'solar_panel1_voltage': {
        'long_name': 'Solar Panel 1 Voltage',
        'standard_name': 'solar_panel_1_voltage',
        'units': 'V'
    },
    'solar_panel1_current': {
        'long_name': 'Solar Panel 1 Current',
        'standard_name': 'solar_panel_1_current',
        'units': 'mA'
    },
    'solar_panel2_state': {
        'long_name': 'Solar Panel 2 State',
        'standard_name': 'solar_panel_2_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'solar_panel2_voltage': {
        'long_name': 'Solar Panel 2 Voltage',
        'standard_name': 'solar_panel_2_voltage',
        'units': 'V'
    },
    'solar_panel2_current': {
        'long_name': 'Solar Panel 2 Current',
        'standard_name': 'solar_panel_2_current',
        'units': 'mA'
    },
    'solar_panel3_state': {
        'long_name': 'Solar Panel 3 State',
        'standard_name': 'solar_panel_3_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'solar_panel3_voltage': {
        'long_name': 'Solar Panel 3 Voltage',
        'standard_name': 'solar_panel_3_voltage',
        'units': 'V'
    },
    'solar_panel3_current': {
        'long_name': 'Solar Panel 3 Current',
        'standard_name': 'solar_panel_3_current',
        'units': 'mA'
    },
    'solar_panel4_state': {
        'long_name': 'Solar Panel 4 State',
        'standard_name': 'solar_panel_4_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'solar_panel4_voltage': {
        'long_name': 'Solar Panel 4 Voltage',
        'standard_name': 'solar_panel_4_voltage',
        'units': 'V'
    },
    'solar_panel4_current': {
        'long_name': 'Solar Panel 4 Current',
        'standard_name': 'solar_panel_4_current',
        'units': 'mA'
    },
    'wind_turbine1_state': {
        'long_name': 'Wind Turbine 1 State',
        'standard_name': 'wind_turbine_1_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'wind_turbine1_voltage': {
        'long_name': 'Wind Turbine 1 Voltage',
        'standard_name': 'wind_turbine_1_voltage',
        'units': 'V'
    },
    'wind_turbine1_current': {
        'long_name': 'Wind Turbine 1 Current',
        'standard_name': 'wind_turbine_1_current',
        'units': 'mA'
    },
    'wind_turbine2_state': {
        'long_name': 'Wind Turbine 2 State',
        'standard_name': 'wind_turbine_2_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'wind_turbine2_voltage': {
        'long_name': 'Wind Turbine 2 Voltage',
        'standard_name': 'wind_turbine_2_voltage',
        'units': 'V'
    },
    'wind_turbine2_current': {
        'long_name': 'Wind Turbine 2 Current',
        'standard_name': 'wind_turbine_2_current',
        'units': 'mA'
    },
    'fuel_cell1_state': {
        'long_name': 'Fuel Cell 1 State',
        'standard_name': 'fuel_cell_1_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'fuel_cell1_voltage': {
        'long_name': 'Fuel Cell 1 Voltage',
        'standard_name': 'fuel_cell_1_voltage',
        'units': 'V'
    },
    'fuel_cell1_current': {
        'long_name': 'Fuel Cell 1 Current',
        'standard_name': 'fuel_cell_1_current',
        'units': 'mA'
    },
    'fuel_cell2_state': {
        'long_name': 'Fuel Cell 2 State',
        'standard_name': 'fuel_cell_2_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'fuel_cell2_voltage': {
        'long_name': 'Fuel Cell 2 Voltage',
        'standard_name': 'fuel_cell_2_voltage',
        'units': 'V'
    },
    'fuel_cell2_current': {
        'long_name': 'Fuel Cell 2 Current',
        'standard_name': 'fuel_cell_2_current',
        'units': 'mA'
    },
    'battery_bank1_temperature': {
        'long_name': 'Battery Bank 1 Temperature',
        'standard_name': 'battery_bank_1_temperature',
        'units': 'degree_Celcius'
    },
    'battery_bank1_voltage': {
        'long_name': 'Battery Bank 1 Voltage',
        'standard_name': 'battery_bank_1_voltage',
        'units': 'V'
    },
    'battery_bank1_current': {
        'long_name': 'Battery Bank 1 Current',
        'standard_name': 'battery_bank_1_current',
        'units': 'mA'
    },
    'battery_bank2_temperature': {
        'long_name': 'Battery Bank 2 Temperature',
        'standard_name': 'battery_bank_2_temperature',
        'units': 'degree_Celcius'
    },
    'battery_bank2_voltage': {
        'long_name': 'Battery Bank 2 Voltage',
        'standard_name': 'battery_bank_2_voltage',
        'units': 'V'
    },
    'battery_bank2_current': {
        'long_name': 'Battery Bank 2 Current',
        'standard_name': 'battery_bank_2_current',
        'units': 'mA'
    },
    'battery_bank3_temperature': {
        'long_name': 'Battery Bank 3 Temperature',
        'standard_name': 'battery_bank_2_temperature',
        'units': 'degree_Celcius'
    },
    'battery_bank3_voltage': {
        'long_name': 'Battery Bank 3 Voltage',
        'standard_name': 'battery_bank_3_voltage',
        'units': 'V'
    },
    'battery_bank3_current': {
        'long_name': 'Battery Bank 3 Current',
        'standard_name': '',
        'units': 'mA'
    },
    'battery_bank4_temperature': {
        'long_name': 'Battery Bank 4 Temperature',
        'standard_name': 'battery_bank_4_temperature',
        'units': 'degree_Celcius'
    },
    'battery_bank4_voltage': {
        'long_name': 'Battery Bank 4 Voltage',
        'standard_name': 'battery_bank_4_voltage',
        'units': 'V'
    },
    'battery_bank4_current': {
        'long_name': 'Battery Bank 4 Current',
        'standard_name': 'battery_bank_4_current',
        'units': 'mA'
    },
    'external_voltage': {
        'long_name': 'External Voltage',
        'standard_name': 'external_voltage',
        'units': 'V'
    },
    'external_current': {
        'long_name': 'External Current',
        'standard_name': 'external_current',
        'units': 'mA'
    },
    'internal_voltage': {
        'long_name': 'Internal Voltage',
        'standard_name': 'internal_voltage',
        'units': 'V'
    },
    'internal_current': {
        'long_name': 'Internal Current',
        'standard_name': 'internal_current',
        'units': 'mA'
    },
    'internal_temperature': {
        'long_name': 'Internal Temperature',
        'standard_name': 'Internal Temperature',
        'units': 'degree_Celcius'
    },
    'fuel_cell_volume': {
        'long_name': 'Fuel Cell Volume',
        'standard_name': 'fuel_cell_volume',
        'units': 'mL'
    },
    'seawater_ground_state': {
        'long_name': 'Sea Water Ground State',
        'standard_name': 'seawater_ground_state',
        'units': '1',
        'flag_masks': '0',
        'flag_meanings': 'undefined'
    },
    'seawater_ground_positve': {
        'long_name': 'Sea Water Ground Positive',
        'standard_name': 'seawater_ground_positive',
        'units': 'uA'
    },
    'seawater_ground_negative': {
        'long_name': 'Sea Water Ground Negative',
        'standard_name': 'seawater_ground_Negative',
        'units': 'uA'
    },
    'cvt_state': {
        'long_name': 'CVT State',
        'standard_name': 'cvt_state',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'cvt_voltage': {
        'long_name': 'CVT Voltage',
        'standard_name': 'cvt_voltage',
        'units': 'V'
    },
    'cvt_current': {
        'long_name': 'CVT Current',
        'standard_name': 'cvt_current',
        'units': 'mA'
    },
    'cvt_interlock': {
        'long_name': 'CVT Interlock',
        'standard_name': 'cvt_interlock',
        'units': '1',
        'flag_masks': '0, 1',
        'flag_meanings': 'disabled enabled'
    },
    'cvt_temperature': {
        'long_name': 'CVT Temperature',
        'standard_name': 'cvt_temperature',
        'units': 'degree_Celcius'
    },
    'error_flag3': {
        'long_name': 'Error Flag 3',
        'standard_name': 'error_flag_3',
        'units': '1',
        'flag_masks': (
            '0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, '
            '131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, '
            '134217728, 268435456, 536870912, 1073741824, 2147483648'
        ),
        'flag_meanings': (
            'no_error '
            'cvtr_board_overtemp_(>100_c) '
            'interlock_output_supply_fuse_blown '
            'interlock_status_1_supply_fuse_blown '
            'interlock_status_2_supply_fuse_blown '
            'input_1_fuse_blown '
            'input_2_fuse_blown '
            'input_3_fuse_blown '
            'input_4_fuse_blown '
            '+5v_over-voltage_(>5.5v) '
            '+5v_under-voltage_(<4.5v) '
            'output_sensor_circuit_power_over-voltage_(>9.45v) '
            'output_sensor_circuit_power_under-voltage_(<4.5v) '
            'p_swgf_sensor_circuit_power_over-voltage_(>9.45v) '
            'p_swgf_sensor_circuit_power_under-voltage_(<8.64v) '
            'n_swgf_sensor_circuit_power_over-voltage_(>9.45v) '
            'n_swgf_sensor_circuit_power_under-voltage_(<8.64v) '
            'raw_24v_input_power_sensor_fault '
            'cvtr_24v_hotel_power_sensor_fault '
            'interlock_supply_output_sensor_fault '
            'interlock_status_1_sensor_fault '
            'interlock_status_2_sensor_fault '
            'interlock_input_sensor_fault '
            'p_swgf_occured n_swgf_occured '
            'input_1_sensor_fault '
            'input_2_sensor_fault '
            'input_3_sensor_fault '
            'input_4_sensor_fault '
            'high_voltage_output_current_sensor_fault '
            'high_voltage_output_voltage_sensor_fault '
            'p_swgf_sensor_fault n_swgf_sensor_fault'
        )
    }
}
