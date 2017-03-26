#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.error_flags
@file cgsn_processing/process/error_flags.py
@author Christopher Wingard
@brief Adds variables to a pandas DataFrame for the various error flags produced by the systems
"""
import numpy as np
from enum import IntEnum


# Setup the error flag enumeration class for the CPM Supervisor
class SupervErrorFlagCPM(IntEnum):
    efc_no_errors = 0x00000000
    efc_sbd_hardware_failure = 0x00000001
    efc_sbd_antenna_fault = 0x00000002
    efc_sbd_no_comms = 0x00000004
    efc_sbd_timeout_exceeded = 0x00000008
    efc_sbd_bad_message_received = 0x00000010
    efc_main_v_out_of_range = 0x00000020
    efc_main_c_out_of_range = 0x00000040
    efc_bbatt_v_out_of_range = 0x00000080
    efc_bbatt_c_out_of_range = 0x00000100
    efc_seascan_pps_fault = 0x00000200
    efc_gps_pps_fault = 0x00000400
    efc_wake_from_unknown_source = 0x00000800
    efc_no_psc_data = 0x00001000
    efc_efc_psc_main_v_and_main_v_disagree = 0x00002000
    efc_psc_main_c_and_main_c_disagree = 0x00004000
    efc_no_cpm_heartbeat = 0x00008000
    efc_heartbeat_threshold_exceeded_power_cycling_cpm = 0x00010000
    efc_iseawater_gflt_sbd_pos_out_of_allowable_range = 0x00020000
    efc_iseawater_gflt_sbd_gnd_out_of_allowable_range = 0x00040000
    efc_iseawater_gflt_gps_pos_out_of_allowable_range = 0x00080000
    efc_iseawater_gflt_gps_gnd_out_of_allowable_range = 0x00100000
    efc_iseawater_gflt_main_pos_out_of_allowable_range = 0x00200000
    efc_iseawater_gflt_main_gnd_out_of_allowable_range = 0x00400000
    efc_iseawater_gflt_9522_fw_pos_out_of_allowable_range = 0x00800000
    efc_iseawater_gflt_9522_fw_gnd_out_of_allowable_range = 0x01000000
    efc_leak_det1_exceeded_limit = 0x02000000
    efc_leak_det2_exceeded_limit = 0x04000000
    efc_i2c_communication_error = 0x08000000
    efc_uart_communication_error = 0x10000000
    efc_cpm_dead_recommend_switchover = 0x20000000
    efc_channel_pic_over_current = 0x40000000
    efc_mpic_brown_out_reset = 0x80000000


class SupervErrorFlagDCL(IntEnum):
    efd_no_errors = 0x00000000
    efd_vmain_out_of_normal_range = 0x00000001
    efd_imain_out_of_normal_range = 0x00000002
    efd_iseawater_gflt_iso3v3_pos_out_of_allowable_range = 0x00000004
    efd_iseawater_gflt_iso3v3_gnd_out_of_allowable_range = 0x00000008
    efd_iseawater_gflt_vmain_pos_out_of_allowable_range = 0x00000010
    efd_iseawater_gflt_vmain_gnd_out_of_allowawble_range = 0x00000020
    efd_iseawater_gflt_inst_pos_out_of_allowable_range = 0x00000040
    efd_iseawater_gflt_inst_gnd_out_of_allowable_range = 0x00000080
    efd_iseawater_volt_src_4_v_out_of_allowable_range = 0x00000100
    efd_iseawater_volt_src_4_gnd_out_of_allowable_range = 0x00000200
    efd_leak_0_voltage_exceeded_limit = 0x00000400
    efd_leak_1_voltage_exceeded_limit = 0x00000800
    efd_chpic_overcurrent_fault_exists = 0x00001000
    efd_chpic_addr_1_not_responding = 0x00002000
    efd_chpic_addr_2_not_responding = 0x00004000
    efd_chpic_addr_3_not_responding = 0x00008000
    efd_chpic_addr_4_not_responding = 0x00010000
    efd_chpic_addr_5_not_responding = 0x00020000
    efd_chpic_addr_6_not_responding = 0x00040000
    efd_chpic_addr_7_not_responding = 0x00080000
    efd_chpic_addr_8_not_responding = 0x00100000
    efd_i2c_error = 0x00200000
    efd_uart_error = 0x00400000
    efd_mpic_brown_out_reset = 0x00800000


# Setup the various error flag enumeration classes for the PSC
class PwrsysOverrideFlag(IntEnum):
    efo_no_override = 0x0000
    efo_wt1_connect = 0x0001
    efo_wt2_connect = 0x0002
    efo_pv1_connect = 0x0004
    efo_pv2_connect = 0x0008
    efo_pv3_connect = 0x0010
    efo_pv4_connect = 0x0020
    efo_fc1_connect = 0x0040
    efo_fc2_connect = 0x0080
    efo_hipwr_control = 0x0100
    efo_hipwr_reset = 0x0200
    efo_external_power = 0x0400


class PwrsysErrorFlag1(IntEnum):
    ef1_no_error = 0x00000000
    ef1_battery1_of_string1_overtemp = 0x00000001
    ef1_battery2_of_string1_overtemp = 0x00000002
    ef1_battery1_of_string2_overtemp = 0x00000004
    ef1_battery2_of_string2_overtemp = 0x00000008
    ef1_battery1_of_string3_overtemp = 0x00000010
    ef1_battery2_of_string3_overtemp = 0x00000020
    ef1_battery1_of_string4_overtemp = 0x00000040
    ef1_battery2_of_string4_overtemp = 0x00000080
    ef1_battery_string_1_fuse_blown = 0x00000100
    ef1_battery_string_2_fuse_blown = 0x00000200
    ef1_battery_string_3_fuse_blown = 0x00000400
    ef1_battery_string_4_fuse_blown = 0x00000800
    ef1_battery_string_1_charging_sensor_fault = 0x00001000
    ef1_battery_string_1_discharging_sensor_fault = 0x00002000
    ef1_battery_string_2_charging_sensor_fault = 0x00004000
    ef1_battery_string_2_discharging_sensor_fault = 0x00008000
    ef1_battery_string_3_charging_sensor_fault = 0x00010000
    ef1_battery_string_3_discharging_sensor_fault = 0x00020000
    ef1_battery_string_4_charging_sensor_fault = 0x00040000
    ef1_battery_string_4_discharging_sensor_fault = 0x00080000
    ef1_pv1_sensor_fault = 0x00100000
    ef1_pv2_sensor_fault = 0x00200000
    ef1_pv3_sensor_fault = 0x00400000
    ef1_pv4_sensor_fault = 0x00800000
    ef1_wt1_sensor_fault = 0x01000000
    ef1_wt2_sensor_fault = 0x02000000
    ef1_eeprom_access_fault = 0x04000000
    ef1_rtclk_access_fault = 0x08000000
    ef1_external_power_sensor_fault = 0x10000000
    ef1_psc_hotel_power_sensor_fault = 0x20000000
    ef1_psc_internal_overtemp_fault = 0x40000000
    ef1_hipwr_dc_dc_converter_fuse_blown = 0x80000000


class PwrsysErrorFlag2(IntEnum):
    ef2_no_error = 0x00000000
    ef2_buoy_24v_power_sensor_fault = 0x00000001
    ef2_buoy_24v_power_over_voltage_fault = 0x00000002
    ef2_buoy_24v_power_under_voltage_fault = 0x00000004
    ef2_fuse_5v_blown_non_critical = 0x00000008
    ef2_wt1_control_relay_fault = 0x00000010
    ef2_wt2_control_relay_fault = 0x00000020
    ef2_pv1_control_relay_fault = 0x00000040
    ef2_pv2_control_relay_fault = 0x00000080
    ef2_pv3_control_relay_fault = 0x00000100
    ef2_pv4_control_relay_fault = 0x00000200
    ef2_fc1_control_relay_fault = 0x00000400
    ef2_fc2_control_relay_fault = 0x00000800
    ef2_cvt_swg_fault = 0x00001000
    ef2_cvt_general_fault = 0x00002000
    ef2_psc_hard_reset_flag = 0x00004000
    ef2_psc_power_on_reset_flag = 0x00008000
    ef2_wt1_fuse_blown = 0x00010000
    ef2_wt2_fuse_blown = 0x00020000
    ef2_pv1_fuse_blown = 0x00040000
    ef2_pv2_fuse_blown = 0x00080000
    ef2_pv3_fuse_blown = 0x00100000
    ef2_pv4_fuse_blown = 0x00200000
    ef2_cvt_shut_down_due_to_low_input_voltage = 0x00400000


class PwrsysErrorFlag3(IntEnum):
    ef3_no_error = 0x00000000
    ef3_cvt_board_temp_over_100C = 0x00000001
    ef3_interlock_output_supply_fuse_blown = 0x00000002
    ef3_interlock_status_1_supply_fuse_blown = 0x00000004
    ef3_interlock_status_2_supply_fuse_blown = 0x00000008
    ef3_input_1_fuse_blown = 0x00000010
    ef3_input_2_fuse_blown = 0x00000020
    ef3_input_3_fuse_blown = 0x00000040
    ef3_input_4_fuse_blown = 0x00000080
    ef3_over_5v_voltage = 0x00000100
    ef3_under_5v_voltage = 0x00000200
    ef3_output_sensor_circuit_power_over_voltage = 0x00000400
    ef3_output_sensor_circuit_power_under_voltage = 0x00000800
    ef3_p_swgf_sensor_circuit_power_over_voltage = 0x00001000
    ef3_p_swgf_sensor_circuit_power_under_voltage = 0x00002000
    ef3_n_swgf_sensor_circuit_power_over_voltage = 0x00004000
    ef3_n_swgf_sensor_circuit_power_under_voltage = 0x00008000
    ef3_raw_24v_input_power_sensor_fault = 0x00010000
    ef3_cvt_24v_hotel_power_sensor_fault = 0x00020000
    ef3_interlock_supply_output_sensor_fault = 0x00040000
    ef3_interlock_status_1_sensor_fault = 0x00080000
    ef3_interlock_status_2_sensor_fault = 0x00100000
    ef3_interlock_input_sensor_fault = 0x00200000
    ef3_p_swgf_occured = 0x00400000
    ef3_n_swgf_occured = 0x00800000
    ef3_input_1_sensor_fault = 0x01000000
    ef3_input_2_sensor_fault = 0x02000000
    ef3_input_3_sensor_fault = 0x04000000
    ef3_input_4_sensor_fault = 0x08000000
    ef3_high_voltage_output_current_sensor_fault = 0x10000000
    ef3_high_voltage_output_voltage_sensor_fault = 0x20000000
    ef3_p_swgf_sensor_fault = 0x40000000
    ef3_n_swgf_sensor_fault= 0x80000000


def derive_multi_flags(flag_class, flag_name, df):
    """
    Uses the enumeration flag classes from above to quickly set values for the flag values
    in the DataFrame. Returns the DataFrame with the newly created variables. 
    """
    for name, member in flag_class.__members__.items():
        flag = []
        for row in df.itertuples():
            # grab the flag value
            x = row._asdict()[flag_name]
            if not isinstance(x, (np.int, np.int64)):
                # convert it to an integer if still a string
                x = int(x, 16)
            # compare via a logical AND bitwise operation to the flags
            if not flag_class[name] & x:
                # set the flag to "false", or 0, if the bitwise operation is 0
                flag.append(0)
            else:
                # set to 1, or "true" for this flag condition
                flag.append(1)
        # add the flag variable to the data frame
        df[name] = flag

    return df


def derive_single_flags(flag_class, value, df):
    """
    Uses the enumeration flag class from above to quickly set values for the flag values in the DataFrame. Returns 
    the DataFrame with the newly created variables. 
    """
    for name, member in flag_class.__members__.items():
        flag = []
        for row in df.itertuples():
            # grab the flag value
            x = row._asdict()[flag_name]
            if not isinstance(x, (np.int, np.int64)):
                # convert it to an integer if still a string
                x = int(x, 16)
            # compare via a logical OR bitwise operation to the flags
            if not flag_class[name] | x:
                # set the flag to "false", or 0, if the bitwise operation is 0
                flag.append(0)
            else:
                # set to 1, or "true" for this flag condition
                flag.append(1)
        # add the flag variable to the data frame
        df[name] = flag

    return df

