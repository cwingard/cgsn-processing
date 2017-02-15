#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pwrsys
@file cgsn_processing/process/configs/attr_pwrsys.py
@author Christopher Wingard
@brief Attributes for the PWRSYS variables
"""
PWRSYS = {
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'main_voltage': {
        'long_name': 'Main Voltage',
        'standard_name': 'main_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'main_current': {
        'long_name': 'Main Current',
        'standard_name': 'main_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'percent_charge': {
        'long_name': 'Percent Charge',
        'standard_name': 'percent_charge',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'override_flag': {
        'long_name': 'Override Flag',
        'standard_name': 'override_flag',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'error_flag1': {
        'long_name': 'Error Flag 1',
        'standard_name': 'error_flag_1',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'error_flag2': {
        'long_name': 'Error Flag 2',
        'standard_name': 'error_flag_2',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel1_state': {
        'long_name': 'Solar Panel 1 State',
        'standard_name': 'solar_panel_1_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel1_voltage': {
        'long_name': 'Solar Panel 1 Voltage',
        'standard_name': 'solar_panel_1_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel1_current': {
        'long_name': 'Solar Panel 1 Current',
        'standard_name': 'solar_panel_1_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel2_state': {
        'long_name': 'Solar Panel 2 State',
        'standard_name': 'solar_panel_2_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel2_voltage': {
        'long_name': 'Solar Panel 2 Voltage',
        'standard_name': 'solar_panel_2_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel2_current': {
        'long_name': 'Solar Panel 2 Current',
        'standard_name': 'solar_panel_2_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel3_state': {
        'long_name': 'Solar Panel 3 State',
        'standard_name': 'solar_panel_3_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel3_voltage': {
        'long_name': 'Solar Panel 3 Voltage',
        'standard_name': 'solar_panel_3_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel3_current': {
        'long_name': 'Solar Panel 3 Current',
        'standard_name': 'solar_panel_3_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel4_state': {
        'long_name': 'Solar Panel 4 State',
        'standard_name': 'solar_panel_4_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel4_voltage': {
        'long_name': 'Solar Panel 4 Voltage',
        'standard_name': 'solar_panel_4_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'solar_panel4_current': {
        'long_name': 'Solar Panel 4 Current',
        'standard_name': 'solar_panel_4_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'wind_turbine1_state': {
        'long_name': 'Wind Turbine 1 State',
        'standard_name': 'wind_turbine_1_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'wind_turbine1_voltage': {
        'long_name': 'Wind Turbine 1 Voltage',
        'standard_name': 'wind_turbine_1_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'wind_turbine1_current': {
        'long_name': 'Wind Turbine 1 Current',
        'standard_name': 'wind_turbine_1_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'wind_turbine2_state': {
        'long_name': 'Wind Turbine 2 State',
        'standard_name': 'wind_turbine_2_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'wind_turbine2_voltage': {
        'long_name': 'Wind Turbine 2 Voltage',
        'standard_name': 'wind_turbine_2_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'wind_turbine2_current': {
        'long_name': 'Wind Turbine 2 Current',
        'standard_name': 'wind_turbine_2_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell1_state': {
        'long_name': 'Fuel Cell 1 State',
        'standard_name': 'fuel_cell_1_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell1_voltage': {
        'long_name': 'Fuel Cell 1 Voltage',
        'standard_name': 'fuel_cell_1_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell1_current': {
        'long_name': 'Fuel Cell 1 Current',
        'standard_name': 'fuel_cell_1_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell2_state': {
        'long_name': 'Fuel Cell 2 State',
        'standard_name': 'fuel_cell_2_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell2_voltage': {
        'long_name': 'Fuel Cell 2 Voltage',
        'standard_name': 'fuel_cell_2_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell2_current': {
        'long_name': 'Fuel Cell 2 Current',
        'standard_name': 'fuel_cell_2_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank1_temperature': {
        'long_name': 'Battery Bank 1 Temperature',
        'standard_name': 'battery_bank_1_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank1_voltage': {
        'long_name': 'Battery Bank 1 Voltage',
        'standard_name': 'battery_bank_1_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank1_current': {
        'long_name': 'Battery Bank 1 Current',
        'standard_name': 'battery_bank_1_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank2_temperature': {
        'long_name': 'Battery Bank 2 Temperature',
        'standard_name': 'battery_bank_2_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank2_voltage': {
        'long_name': 'Battery Bank 2 Voltage',
        'standard_name': 'battery_bank_2_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank2_current': {
        'long_name': 'Battery Bank 2 Current',
        'standard_name': 'battery_bank_2_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank3_temperature': {
        'long_name': 'Battery Bank 3 Temperature',
        'standard_name': 'battery_bank_2_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank3_voltage': {
        'long_name': 'Battery Bank 3 Voltage',
        'standard_name': 'battery_bank_3_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank3_current': {
        'long_name': 'Battery Bank 3 Current',
        'standard_name': '',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank4_temperature': {
        'long_name': 'Battery Bank 4 Temperature',
        'standard_name': 'battery_bank_4_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank4_voltage': {
        'long_name': 'Battery Bank 4 Voltage',
        'standard_name': 'battery_bank_4_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'battery_bank4_current': {
        'long_name': 'Battery Bank 4 Current',
        'standard_name': 'battery_bank_4_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'external_voltage': {
        'long_name': 'External Voltage',
        'standard_name': 'external_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'external_current': {
        'long_name': 'External Current',
        'standard_name': 'external_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'internal_voltage': {
        'long_name': 'Internal Voltage',
        'standard_name': 'internal_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'internal_current': {
        'long_name': 'Internal Current',
        'standard_name': 'internal_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'internal_temperature': {
        'long_name': 'Internal Temperature',
        'standard_name': 'Internal Temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'fuel_cell_volume': {
        'long_name': 'Fuel Cell Volume',
        'standard_name': 'fuel_cell_volume',
        'units': 'mL',
        'coordinates': 'time z longitude latitude'
    },
    'seawater_ground_state': {
        'long_name': 'Sea Water Ground State',
        'standard_name': 'seawater_ground_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'seawater_ground_positve': {
        'long_name': 'Sea Water Ground Positive',
        'standard_name': 'seawater_ground_positive',
        'units': 'uA',
        'coordinates': 'time z longitude latitude'
    },
    'seawater_ground_negative': {
        'long_name': 'Sea Water Ground Negative',
        'standard_name': 'seawater_ground_Negative',
        'units': 'uA',
        'coordinates': 'time z longitude latitude'
    },
    'cvt_state': {
        'long_name': 'CVT State',
        'standard_name': 'cvt_state',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'cvt_voltage': {
        'long_name': 'CVT Voltage',
        'standard_name': 'cvt_voltage',
        'units': 'V',
        'coordinates': 'time z longitude latitude'
    },
    'cvt_current': {
        'long_name': 'CVT Current',
        'standard_name': 'cvt_current',
        'units': 'mA',
        'coordinates': 'time z longitude latitude'
    },
    'cvt_interlock': {
        'long_name': 'CVT Interlock',
        'standard_name': 'cvt_interlock',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    },
    'cvt_temperature': {
        'long_name': 'CVT Temperature',
        'standard_name': 'cvt_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time z longitude latitude'
    },
    'error_flag3': {
        'long_name': 'Error Flag 3',
        'standard_name': 'error_flag_3',
        'units': '1',
        'coordinates': 'time z longitude latitude'
    }
}
