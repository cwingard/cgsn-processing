#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.error_flags
@file cgsn_processing/process/error_flags.py
@author Christopher Wingard
@brief Adds variables to a pandas DataFrame for the various error flags produced by the systems
"""
from enum import IntEnum


# Setup the various error flag enumeration classes for the PSC
class PwrsysOverrideFlag(IntEnum):
    no_override     = 0x0000
    wt1_connect     = 0x0001
    wt2_connect     = 0x0002
    pv1_connect     = 0x0004
    pv2_connect     = 0x0008
    pv3_connect     = 0x0010
    pv4_connect     = 0x0020
    fc1_connect     = 0x0040
    fc2_connect     = 0x0080
    hipwr_control   = 0x0100
    hipwr_reset     = 0x0200
    external_power  = 0x0400


class PwrsysErrorFlag1(IntEnum):
    no_error                                    = 0x00000000
    battery1_of_string1_overtemp                = 0x00000001
    battery2_of_string1_overtemp                = 0x00000002
    battery1_of_string2_overtemp                = 0x00000004
    battery2_of_string2_overtemp                = 0x00000008
    battery1_of_string3_overtemp                = 0x00000010
    battery2_of_string3_overtemp                = 0x00000020
    battery1_of_string4_overtemp                = 0x00000040
    battery2_of_string4_overtemp                = 0x00000080
    battery_string_1_fuse_blown                 = 0x00000100
    battery_string_2_fuse_blown                 = 0x00000200
    battery_string_3_fuse_blown                 = 0x00000400
    battery_string_4_fuse_blown                 = 0x00000800
    battery_string_1_charging_sensor_fault      = 0x00001000
    battery_string_1_discharging_sensor_fault   = 0x00002000
    battery_string_2_charging_sensor_fault      = 0x00004000
    battery_string_2_discharging_sensor_fault   = 0x00008000
    battery_string_3_charging_sensor_fault      = 0x00010000
    battery_string_3_discharging_sensor_fault   = 0x00020000
    battery_string_4_charging_sensor_fault      = 0x00040000
    battery_string_4_discharging_sensor_fault   = 0x00080000
    pv1_sensor_fault                            = 0x00100000
    pv2_sensor_fault                            = 0x00200000
    pv3_sensor_fault                            = 0x00400000
    pv4_sensor_fault                            = 0x00800000
    wt1_sensor_fault                            = 0x01000000
    wt2_sensor_fault                            = 0x02000000
    eeprom_access_fault                         = 0x04000000
    rtclk_access_fault                          = 0x08000000
    external_power_sensor_fault                 = 0x10000000
    psc_hotel_power_sensor_fault                = 0x20000000
    psc_internal_overtemp_fault                 = 0x40000000
    hipwr_dc_dc_converter_fuse_blown            = 0x80000000


class PwrsysErrorFlag2(IntEnum):
    no_error                                    = 0x00000000
    buoy_24v_power_sensor_fault                 = 0x00000001
    buoy_24v_power_over_voltage_fault           = 0x00000002
    buoy_24v_power_under_voltage_fault          = 0x00000004
    fuse_5v_blown_non_critical                  = 0x00000008
    wt1_control_relay_fault                     = 0x00000010
    wt2_control_relay_fault                     = 0x00000020
    pv1_control_relay_fault                     = 0x00000040
    pv2_control_relay_fault                     = 0x00000080
    pv3_control_relay_fault                     = 0x00000100
    pv4_control_relay_fault                     = 0x00000200
    fc1_control_relay_fault                     = 0x00000400
    fc2_control_relay_fault                     = 0x00000800
    cvt_swg_fault                               = 0x00001000
    cvt_general_fault                           = 0x00002000
    psc_hard_reset_flag                         = 0x00004000
    psc_power_on_reset_flag                     = 0x00008000
    wt1_fuse_blown                              = 0x00010000
    wt2_fuse_blown                              = 0x00020000
    pv1_fuse_blown                              = 0x00040000
    pv2_fuse_blown                              = 0x00080000
    pv3_fuse_blown                              = 0x00100000
    pv4_fuse_blown                              = 0x00200000
    cvt_shut_down_due_to_low_input_voltage      = 0x00400000


class PwrsysErrorFlag3(IntEnum):
    no_error                                    = 0x00000000
    cvt_board_temp_over_100C                    = 0x00000001
    interlock_output_supply_fuse_blown          = 0x00000002
    interlock_status_1_supply_fuse_blown        = 0x00000004
    interlock_status_2_supply_fuse_blown        = 0x00000008
    input_1_fuse_blown                          = 0x00000010
    input_2_fuse_blown                          = 0x00000020
    input_3_fuse_blown                          = 0x00000040
    input_4_fuse_blown                          = 0x00000080
    over_5v_voltage                             = 0x00000100
    under_5v_voltage                            = 0x00000200
    output_sensor_circuit_power_over_voltage    = 0x00000400
    output_sensor_circuit_power_under_voltage   = 0x00000800
    p_swgf_sensor_circuit_power_over_voltage    = 0x00001000
    p_swgf_sensor_circuit_power_under_voltage   = 0x00002000
    n_swgf_sensor_circuit_power_over_voltage    = 0x00004000
    n_swgf_sensor_circuit_power_under_voltage   = 0x00008000
    raw_24v_input_power_sensor_fault            = 0x00010000
    cvt_24v_hotel_power_sensor_fault            = 0x00020000
    interlock_supply_output_sensor_fault        = 0x00040000
    interlock_status_1_sensor_fault             = 0x00080000
    interlock_status_2_sensor_fault             = 0x00100000
    interlock_input_sensor_fault                = 0x00200000
    p_swgf_occured                              = 0x00400000
    n_swgf_occured                              = 0x00800000
    input_1_sensor_fault                        = 0x01000000
    input_2_sensor_fault                        = 0x02000000
    input_3_sensor_fault                        = 0x04000000
    input_4_sensor_fault                        = 0x08000000
    high_voltage_output_current_sensor_fault    = 0x10000000
    high_voltage_output_voltage_sensor_fault    = 0x20000000
    p_swgf_sensor_fault                         = 0x40000000
    n_swgf_sensor_fault                         = 0x80000000


def derive_multi_flags(flag_class, value):
    """
    Uses the enumeration flag class from above to quickly set values for the flag values
    in the DataFrame. Returns the DataFrame with the newly created variables. 
    """
    for name, member in flag_class.__members__.items():
        if not flag_class[name] & value:
            return 0
        else:
            return 1


def derive_single_flags(flag_class, value, df):
    """
    Uses the enumeration flag class from above to quickly set values for the flag values in the DataFrame. Returns 
    the DataFrame with the newly created variables. 
    """
    for name, member in flag_class.__members__.items():
        if not flag_class[name] | value:
            df[name] = 0
        else:
            df[name] = 1

    return df
