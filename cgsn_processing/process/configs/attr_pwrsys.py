#!/usr/bin/env python
# _*_ coding: utf_8 _*_
"""
@package cgsn_processing.process.configs.attr_pwrsys
@file cgsn_processing/process/configs/attr_pwrsys.py
@author Christopher Wingard
@brief Attributes for the PWRSYS variables
"""
PWRSYS = {
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
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
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
    'percent_charge': {
        'long_name': 'Percent Charge',
        'standard_name': 'percent_charge',
        'units': 'percent'
    },
    'override_flag': {
        'long_name': 'Override Flag',
        'standard_name': 'override_flag',
        'units': '1'
    },
    'error_flag1': {
        'long_name': 'Error Flag 1',
        'standard_name': 'error_flag_1',
        'units': '1'
    },
    'error_flag2': {
        'long_name': 'Error Flag 2',
        'standard_name': 'error_flag_2',
        'units': '1'
    },
    'solar_panel1_state': {
        'long_name': 'Solar Panel 1 State',
        'standard_name': 'solar_panel_1_state',
        'units': '1'
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
        'units': '1'
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
        'units': '1'
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
        'units': '1'
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
        'units': '1'
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
        'units': '1'
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
        'units': '1'
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
        'units': '1'
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
        'units': 'degree_Celsius'
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
        'units': 'degree_Celsius'
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
        'units': 'degree_Celsius'
    },
    'battery_bank3_voltage': {
        'long_name': 'Battery Bank 3 Voltage',
        'standard_name': 'battery_bank_3_voltage',
        'units': 'V'
    },
    'battery_bank3_current': {
        'long_name': 'Battery Bank 3 Current',
        'standard_name': 'battery_bank_3_current',
        'units': 'mA'
    },
    'battery_bank4_temperature': {
        'long_name': 'Battery Bank 4 Temperature',
        'standard_name': 'battery_bank_4_temperature',
        'units': 'degree_Celsius'
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
        'units': 'degree_Celsius'
    },
    'fuel_cell_volume': {
        'long_name': 'Fuel Cell Volume',
        'standard_name': 'fuel_cell_volume',
        'units': 'mL'
    },
    'seawater_ground_state': {
        'long_name': 'Sea Water Ground State',
        'standard_name': 'seawater_ground_state',
        'units': '1'
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
        'units': '1'
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
        'units': '1'
    },
    'cvt_temperature': {
        'long_name': 'CVT Temperature',
        'standard_name': 'cvt_temperature',
        'units': 'degree_Celsius'
    },
    'error_flag3': {
        'long_name': 'Error Flag 3',
        'standard_name': 'error_flag_3',
        'units': '1'
    },
    'efo_no_override': {'units': '1'},
    'efo_wt1_connect': {'units': '1'},
    'efo_wt2_connect': {'units': '1'},
    'efo_pv1_connect': {'units': '1'},
    'efo_pv2_connect': {'units': '1'},
    'efo_pv3_connect': {'units': '1'},
    'efo_pv4_connect': {'units': '1'},
    'efo_fc1_connect': {'units': '1'},
    'efo_fc2_connect': {'units': '1'},
    'efo_hipwr_control': {'units': '1'},
    'efo_hipwr_reset': {'units': '1'},
    'efo_external_power': {'units': '1'},
    
    'ef1_no_error': {'units': '1'},
    'ef1_battery1_of_string1_overtemp': {'units': '1'},
    'ef1_battery2_of_string1_overtemp': {'units': '1'},
    'ef1_battery1_of_string2_overtemp': {'units': '1'},
    'ef1_battery2_of_string2_overtemp': {'units': '1'},
    'ef1_battery1_of_string3_overtemp': {'units': '1'},
    'ef1_battery2_of_string3_overtemp': {'units': '1'},
    'ef1_battery1_of_string4_overtemp': {'units': '1'},
    'ef1_battery2_of_string4_overtemp': {'units': '1'},
    'ef1_battery_string_1_fuse_blown': {'units': '1'},
    'ef1_battery_string_2_fuse_blown': {'units': '1'},
    'ef1_battery_string_3_fuse_blown': {'units': '1'},
    'ef1_battery_string_4_fuse_blown': {'units': '1'},
    'ef1_battery_string_1_charging_sensor_fault': {'units': '1'},
    'ef1_battery_string_1_discharging_sensor_fault': {'units': '1'},
    'ef1_battery_string_2_charging_sensor_fault': {'units': '1'},
    'ef1_battery_string_2_discharging_sensor_fault': {'units': '1'},
    'ef1_battery_string_3_charging_sensor_fault': {'units': '1'},
    'ef1_battery_string_3_discharging_sensor_fault': {'units': '1'},
    'ef1_battery_string_4_charging_sensor_fault': {'units': '1'},
    'ef1_battery_string_4_discharging_sensor_fault': {'units': '1'},
    'ef1_pv1_sensor_fault': {'units': '1'},
    'ef1_pv2_sensor_fault': {'units': '1'},
    'ef1_pv3_sensor_fault': {'units': '1'},
    'ef1_pv4_sensor_fault': {'units': '1'},
    'ef1_wt1_sensor_fault': {'units': '1'},
    'ef1_wt2_sensor_fault': {'units': '1'},
    'ef1_eeprom_access_fault': {'units': '1'},
    'ef1_rtclk_access_fault': {'units': '1'},
    'ef1_external_power_sensor_fault': {'units': '1'},
    'ef1_psc_hotel_power_sensor_fault': {'units': '1'},
    'ef1_psc_internal_overtemp_fault': {'units': '1'},
    'ef1_hipwr_dc_dc_converter_fuse_blown': {'units': '1'},

    'ef2_no_error': {'units': '1'},
    'ef2_buoy_24v_power_sensor_fault': {'units': '1'},
    'ef2_buoy_24v_power_over_voltage_fault': {'units': '1'},
    'ef2_buoy_24v_power_under_voltage_fault': {'units': '1'},
    'ef2_fuse_5v_blown_non_critical': {'units': '1'},
    'ef2_wt1_control_relay_fault': {'units': '1'},
    'ef2_wt2_control_relay_fault': {'units': '1'},
    'ef2_pv1_control_relay_fault': {'units': '1'},
    'ef2_pv2_control_relay_fault': {'units': '1'},
    'ef2_pv3_control_relay_fault': {'units': '1'},
    'ef2_pv4_control_relay_fault': {'units': '1'},
    'ef2_fc1_control_relay_fault': {'units': '1'},
    'ef2_fc2_control_relay_fault': {'units': '1'},
    'ef2_cvt_swg_fault': {'units': '1'},
    'ef2_cvt_general_fault': {'units': '1'},
    'ef2_psc_hard_reset_flag': {'units': '1'},
    'ef2_psc_power_on_reset_flag': {'units': '1'},
    'ef2_wt1_fuse_blown': {'units': '1'},
    'ef2_wt2_fuse_blown': {'units': '1'},
    'ef2_pv1_fuse_blown': {'units': '1'},
    'ef2_pv2_fuse_blown': {'units': '1'},
    'ef2_pv3_fuse_blown': {'units': '1'},
    'ef2_pv4_fuse_blown': {'units': '1'},
    'ef2_cvt_shut_down_due_to_low_input_voltage': {'units': '1'},

    'ef3_no_error': {'units': '1'},
    'ef3_cvt_board_temp_over_100C': {'units': '1'},
    'ef3_interlock_output_supply_fuse_blown': {'units': '1'},
    'ef3_interlock_status_1_supply_fuse_blown': {'units': '1'},
    'ef3_interlock_status_2_supply_fuse_blown': {'units': '1'},
    'ef3_input_1_fuse_blown': {'units': '1'},
    'ef3_input_2_fuse_blown': {'units': '1'},
    'ef3_input_3_fuse_blown': {'units': '1'},
    'ef3_input_4_fuse_blown': {'units': '1'},
    'ef3_over_5v_voltage': {'units': '1'},
    'ef3_under_5v_voltage': {'units': '1'},
    'ef3_output_sensor_circuit_power_over_voltage': {'units': '1'},
    'ef3_output_sensor_circuit_power_under_voltage': {'units': '1'},
    'ef3_p_swgf_sensor_circuit_power_over_voltage': {'units': '1'},
    'ef3_p_swgf_sensor_circuit_power_under_voltage': {'units': '1'},
    'ef3_n_swgf_sensor_circuit_power_over_voltage': {'units': '1'},
    'ef3_n_swgf_sensor_circuit_power_under_voltage': {'units': '1'},
    'ef3_raw_24v_input_power_sensor_fault': {'units': '1'},
    'ef3_cvt_24v_hotel_power_sensor_fault': {'units': '1'},
    'ef3_interlock_supply_output_sensor_fault': {'units': '1'},
    'ef3_interlock_status_1_sensor_fault': {'units': '1'},
    'ef3_interlock_status_2_sensor_fault': {'units': '1'},
    'ef3_interlock_input_sensor_fault': {'units': '1'},
    'ef3_p_swgf_occured': {'units': '1'},
    'ef3_n_swgf_occured': {'units': '1'},
    'ef3_input_1_sensor_fault': {'units': '1'},
    'ef3_input_2_sensor_fault': {'units': '1'},
    'ef3_input_3_sensor_fault': {'units': '1'},
    'ef3_input_4_sensor_fault': {'units': '1'},
    'ef3_high_voltage_output_current_sensor_fault': {'units': '1'},
    'ef3_high_voltage_output_voltage_sensor_fault': {'units': '1'},
    'ef3_p_swgf_sensor_fault': {'units': '1'},
    'ef3_n_swgf_sensor_fault': {'units': '1'}
}
