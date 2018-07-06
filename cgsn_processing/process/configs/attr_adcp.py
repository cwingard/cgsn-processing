#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_adcp
@file cgsn_processing/process/configs/attr_adcp.py
@author Christopher Wingard
@brief Attributes for the common ADCP and specific PD0, PD8 and PD12 data set variables
"""
ADCP = {
    'global': {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
        'feature_type': 'timeSeries',
        'Conventions': 'CF-1.6'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data per deployment, ' +
                    'allowing for overlapping deployments in the data sets.')
    },
    'timeSeries': {
        'long_name': 'Unique identifier for each feature instance',
        'cf_role': 'timeseries_id'
    },
    'time': {
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'axis': 'T',
        'comment': 'Derived from the data logger''s GPS conditioned, real-time clock'
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': 'Mooring deployment location, surveyed after deployment to determine center of watch circle.'
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': 'Mooring deployment location, surveyed after deployment to determine center of watch circle.'
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Instrument deployment depth',
        'positive': 'down',
        'axis': 'Z'
    }
}

ADCP_PD0 = {
    'global': {
        'title': 'Acoustic Doppler Current Profiler (ADCP) Data -- PD0 Formatted',
        'summary': ('Velocity Profiler using acoustics to measure 3D water-current velocity for a profile of' +
                    'the water column above or below the sensor. High frequency sound waves (75- to 600-kHz)' +
                    'emitted by the profiler scatter off suspended particles and back to the sensor (range is a' +
                    'function of frequency). The sensor calculates velocity by measuring changes in these sound' +
                    'waves (i.e., Doppler shifts). This instrument is also referred to as an Acoustic Doppler' +
                    'Current Profiler (ADCP).'),
        'comment': 'Teledyne RDI Workhorse ADCP'
    },
    # header
    'num_bytes': {
        'long_name': '',
        'comment': ''
    },
    'num_data_types': {
        'long_name': '',
        'comment': ''
    },

    # fixed leader
    'firmware_version': {
        'long_name': '',
        'comment': ''
    },
    'firmware_revision': {
        'long_name': '',
        'comment': ''
    },
    'sysconfig_frequency': {
        'long_name': '',
        'comment': ''
    },
    'sysconfig_beam_pattern': {
        'long_name': '',
        'comment': ''
    },
    'sysconfig_sensor_config': {
        'long_name': '',
        'comment': ''
    },
    'sysconfig_head_attached': {
        'long_name': '',
        'comment': ''
    },
    'sysconfig_vertical_orientation': {
        'long_name': '',
        'comment': ''
    },
    'data_flag': {
        'long_name': '',
        'comment': ''
    },
    'lag_length': {
        'long_name': '',
        'comment': ''
    },
    'num_beams': {
        'long_name': '',
        'comment': ''
    },
    'num_cells': {
        'long_name': '',
        'comment': ''
    },
    'pings_per_ensemble': {
        'long_name': '',
        'comment': ''
    },
    'depth_cell_length': {
        'long_name': '',
        'comment': ''
    },
    'blank_after_transmit': {
        'long_name': '',
        'comment': ''
    },
    'signal_processing_mode': {
        'long_name': '',
        'comment': ''
    },
    'low_corr_threshold': {
        'long_name': '',
        'comment': ''
    },
    'num_code_repetitions': {
        'long_name': '',
        'comment': ''
    },
    'percent_good_min': {
        'long_name': '',
        'comment': ''
    },
    'error_vel_threshold': {
        'long_name': '',
        'comment': ''
    },
    'time_per_ping_minutes': {
        'long_name': '',
        'comment': ''
    },
    'time_per_ping_seconds': {
        'long_name': '',
        'comment': ''
    },
    'coord_transform_type': {
        'long_name': '',
        'comment': ''
    },
    'coord_transform_tilts': {
        'long_name': '',
        'comment': ''
    },
    'coord_transform_beams': {
        'long_name': '',
        'comment': ''
    },
    'coord_transform_mapping': {
        'long_name': '',
        'comment': ''
    },
    'heading_alignment': {
        'long_name': '',
        'comment': ''
    },
    'heading_bias': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_speed': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_depth': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_heading': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_pitch': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_roll': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_conductivity': {
        'long_name': '',
        'comment': ''
    },
    'sensor_source_temperature': {
        'long_name': '',
        'comment': ''
    },
    'sensor_available_depth': {
        'long_name': '',
        'comment': ''
    },
    'sensor_available_heading': {
        'long_name': '',
        'comment': ''
    },
    'sensor_available_pitch': {
        'long_name': '',
        'comment': ''
    },
    'sensor_available_roll': {
        'long_name': '',
        'comment': ''
    },
    'sensor_available_conductivity': {
        'long_name': '',
        'comment': ''
    },
    'sensor_available_temperature': {
        'long_name': '',
        'comment': ''
    },
    'bin_1_distance': {
        'long_name': '',
        'comment': ''
    },
    'transmit_pulse_length': {
        'long_name': '',
        'comment': ''
    },
    'reference_layer_start': {
        'long_name': '',
        'comment': ''
    },
    'reference_layer_stop': {
        'long_name': '',
        'comment': ''
    },
    'false_target_threshold': {
        'long_name': '',
        'comment': ''
    },
    'transmit_lag_distance': {
        'long_name': '',
        'comment': ''
    },
    'system_bandwidth': {
        'long_name': '',
        'comment': ''
    },
    'serial_number': {
        'long_name': '',
        'comment': ''
    },
    'beam_angle': {
        'long_name': '',
        'comment': ''
    },

    # variable leader
    'ensemble_number': {},
    'ensemble_number_increment': {},
    'real_time_clock1': {},
    'bit_result_demod_1': {},
    'bit_result_demod_2': {},
    'bit_result_timing': {},
    'speed_of_sound': {},
    'transducer_depth': {},
    'heading': {},
    'pitch': {},
    'roll': {},
    'salinity': {},
    'temperature': {},
    'mpt_minutes': {},
    'mpt_seconds': {},
    'heading_stdev': {},
    'pitch_stdev': {},
    'roll_stdev': {},
    'adc_transmit_current': {},
    'adc_transmit_voltage': {},
    'adc_ambient_temp': {},
    'adc_pressure_plus': {},
    'adc_pressure_minus': {},
    'adc_attitude_temp': {},
    'adc_attitude': {},
    'adc_contamination_sensor': {},
    'bus_error_exception': {},
    'address_error_exception': {},
    'illegal_instruction_exception': {},
    'zero_divide_instruction': {},
    'emulator_exception': {},
    'unassigned_exception': {},
    'watchdog_restart_occurred': {},
    'battery_saver_power': {},
    'pinging': {},
    'cold_wakeup_occurred': {},
    'unknown_wakeup_occurred': {},
    'clock_read_error': {},
    'unexpected_alarm': {},
    'clock_jump_forward': {},
    'clock_jump_backward': {},
    'power_fail': {},
    'spurious_dsp_interrupt': {},
    'spurious_uart_interrupt': {},
    'spurious_clock_interrupt': {},
    'level_7_interrupt': {},
    'pressure': {},
    'pressure_variance': {},
    'real_time_clock': {},

    # velocity packets
    'eastward': {},
    'northward': {},
    'vertical': {},
    'error': {},

    # correlation magnitudes
    'magnitude_beam1': {},
    'magnitude_beam2': {},
    'magnitude_beam3': {},
    'magnitude_beam4': {},

    # echo intensities
    'intensity_beam1': {},
    'intensity_beam2': {},
    'intensity_beam3': {},
    'intensity_beam4': {},

    # percent good
    'good_3beam': {},
    'transforms_reject': {},
    'bad_beams': {},
    'good_4beam': {}
}