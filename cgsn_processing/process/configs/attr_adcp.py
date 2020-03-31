#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_adcp
@file cgsn_processing/process/configs/attr_adcp.py
@author Christopher Wingard
@brief Attributes for the common ADCP and specific PD0, PD8 and PD12 data set variables
"""
import numpy as np

ADCP = {
    # global attributes
    'global': {
        'title': 'Acoustic Doppler Current Profiler (ADCP) Data',
        'summary': ('Current profiler using acoustics to measure 3D water-current velocities for a profile of' +
                    'the water column above or below the sensor. High frequency sound waves (75 to 600 kHz)' +
                    'emitted by the profiler scatter off suspended particles and back to the sensor (range is a' +
                    'function of frequency). The sensor calculates velocity by measuring changes in these sound' +
                    'waves (i.e., Doppler shifts). This instrument is also referred to as an Acoustic Doppler' +
                    'Current Profiler (ADCP).'),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal Endurance Array (EA) and Coastal and Global Scale Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.6'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, ' +
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00Z',
        'axis': 'T',
        'calendar': 'gregorian',
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
    },
    'bin_number': {
        'long_name': 'Bin Number',
        'comment': 'Number of the ADCP velocity bin. Number of bins is dependent on depth of deployment and frequency.',
        # 'units': ''    # deliberately left blank, no units for this value
    }
}

PD0 = {
    # PD0 fixed leader
    'firmware_version': {
        'long_name': 'Firmware Version',
        'comment': 'Version number of current CPU firmware',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'firmware_revision': {
        'long_name': 'Firmware Revision',
        'comment': 'Revision number of current CPU firmware',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sysconfig_frequency': {
        'long_name': 'Sysconfig Frequency',
        'comment': 'Workhorse transducer frequency',
        'units': 'kHz'
    },
    'sysconfig_beam_pattern': {
        'long_name': 'Sysconfig Beam Pattern',
        'comment': 'Transducer head beam pattern',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sysconfig_sensor_config': {
        'long_name': 'Sysconfig Sensor Config',
        'comment': 'Sensor configuration number (1, 2 or 3)',
        # 'units': ''    # deliberately left blank, no units for this value
     },
    'sysconfig_head_attached': {
        'long_name': 'Sysconfig Head Attached',
        'comment': 'Whether transducer head is attached',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sysconfig_vertical_orientation': {
        'long_name': 'Sysconfig Vertical Orientation',
        'comment': 'Whether vertical orientation is upward or downward',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'data_flag': {
        'long_name': 'Real/Simulated Data Flag',
        'comment': 'PD (Data Stream Select) Real or Simulated data flag. Always set to real data (0) by default',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'lag_length': {
        'long_name': 'Lag Length',
        'comment': 'Time between sound pulses.',
        'units': 's'
    },
    'num_beams': {
        'long_name': 'Number Beams',
        'comment': 'Contains the number of beams used to calculate velocity data',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'num_cells': {
        'long_name': 'Number Cells',
        'comment': 'Contains the number of cells over which the ADCP collects data',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pings_per_ensemble': {
        'long_name': 'Pings Per Ensemble',
        'comment': 'Contains the number of pings averaged together during a data ensemble',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'depth_cell_length': {
        'long_name': 'Cell Length',
        'comment': 'Contains the depth of one cell length',
        'units': 'cm'
    },
    'blank_after_transmit': {
        'long_name': 'Blank After Transmit Distance',
        'comment': ('Contains the blanking distance used by the Workhorse ADCP to allow the transmit circuits time ' +
                    'to recover before receive cycle begins'),
        'units': 'cm'
    },
    'signal_processing_mode': {
        'long_name': 'Signal Processing Mode',
        'comment': 'Signal Processing Mode. Always set to 1',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'low_corr_threshold': {
        'long_name': 'Low Correlation Threshold',
        'comment': 'Contains minimum threshold of correlation that water-profile data can have to be considered good.',
        'units': 'counts'
    },
    'num_code_repetitions': {
        'long_name': 'Number of Code Repetitions',
        'comment': 'Number of code repetitions in the transmit pulse',
        'units': 'counts'
    },
    'percent_good_min': {
        'long_name': 'Percent Good Minimum',
        'comment': ('Minimum percentage of water profiling pings in an ensemble that must be good to output ' +
                    'velocity data.'),
        'units': 'percent'
    },
    'error_vel_threshold': {
        'long_name': 'Error Velocity Threshold',
        'comment': 'Threshold value used to flag water-current data as good or bad.',
        'units': 'mm s-1'
    },
    'coord_transform_type': {
        'long_name': 'Coordinate Transform Type',
        'comment': 'Coordinate Transformation type: 0 = None (Beam), 1 = Instrument, 2 = Ship, 3 = Earth.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'coord_transform_tilts': {
        'long_name': 'Coordinate Transform Tilts',
        'comment': 'Whether tilts used in Earth or Ship coordinated transformations',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'coord_transform_beams': {
        'long_name': 'Coord Transform Beams',
        'comment': 'Was 3-beam solution used if 1 beam is below correlation threshold',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'coord_transform_mapping': {
        'long_name': 'Coord Transform Mapping',
        'comment': 'Bin mapping used with tilts and coordinate transformations',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'heading_alignment': {
        'long_name': 'Heading Alignment',
        'comment': 'Correction factor for physical heading misalignment',
        'units': 'cdegrees'
    },
    'heading_bias': {
        'long_name': 'Heading Bias',
        'comment': 'Correction factor for electrical/magnetic heading bias (e.g. Magnetic declination).',
        'units': 'cdegrees'
    },
    'sensor_source_speed': {
        'long_name': 'Sensor Source Speed',
        'comment': 'Contains the selected source for the speed of sound estimation',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_depth': {
        'long_name': 'Sensor Source Depth',
        'comment': 'Uses ED for depth sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_heading': {
        'long_name': 'Sensor Source Heading',
        'comment': 'Uses EH for transducer heading',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_pitch': {
        'long_name': 'Sensor Source Pitch',
        'comment': 'Uses EP for transducer pitch sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_roll': {
        'long_name': 'Sensor Source Roll',
        'comment': 'Uses ER for transducer roll sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_conductivity': {
        'long_name': 'Sensor Source Conductivity',
        'comment': 'Uses ES (salinity) calculated from external conductivity sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_temperature': {
        'long_name': 'Sensor Source Temperature',
        'comment': 'Uses ET for transducer temperature sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_available_depth': {
        'long_name': 'Sensor Available Depth',
        'comment': 'Is depth sensor installed',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_available_heading': {
        'long_name': 'Sensor Available Heading',
        'comment': 'Is heading sensor installed',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_available_pitch': {
        'long_name': 'Sensor Available Pitch',
        'comment': 'Is pitch sensor installed',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_available_roll': {
        'long_name': 'Sensor Available Roll',
        'comment': 'Is roll sensor installed',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_available_conductivity': {
        'long_name': 'Sensor Available Conductivity',
        'comment': 'Is conductivity sensor installed',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_available_temperature': {
        'long_name': 'Sensor Available Temperature',
        'comment': 'Is temperature sensor installed',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'bin_1_distance': {
        'long_name': 'Distance First Bin',
        'comment': 'Distance to the middle of the first depth cell.',
        'units': 'cm'
    },
    'transmit_pulse_length': {
        'long_name': 'Transmit Pulse Length',
        'comment': 'Length of transmit pulse',
        'units': 'cm',
    },
    'reference_layer_start': {
        'long_name': 'Reference Layer Start',
        'comment': 'Starting depth cell used for water reference layer',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'reference_layer_stop': {
        'long_name': 'Reference Layer Stop',
        'comment': 'Ending depth cell used for water reference layer',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'false_target_threshold': {
        'long_name': 'False Target Threshold',
        'comment': 'Threshold value used to reject data received from false targets, usually fish. 255 disables.',
        'units': 'counts'
    },
    'transmit_lag_distance': {
        'long_name': 'Transmit Lag Distance',
        'comment': 'Distance between pulse repetitions',
        'units': 'cm'
    },
    'system_bandwidth': {
        'long_name': 'System Bandwidth',
        'comment': 'Sets profiling mode bandwidth (sampling) rate from wide (0) to narrow (1). Default is 0',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'serial_number': {
        'long_name': 'Serial Number',
        'comment': 'Serial Number',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'beam_angle': {
        'long_name': 'Beam Angle',
        'comment': 'Transducer head beam angle',
        'units': 'degrees'
    },

    # variable leader
    'ensemble_number': {
        'long_name': 'Ensemble Number',
        'comment': 'Sequential number of the ensemble to which the data applies',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'bit_result_demod_1': {
        'long_name': 'BIT DEMOD 1 Error',
        'comment': 'DEMOD 1 error from the ADCP''s builtin test function',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'bit_result_demod_2': {
        'long_name': 'BIT DEMOD 0 Error',
        'comment': 'DEMOD 0 error from the ADCP''s builtin test function',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'bit_result_timing': {
        'long_name': 'BIT Timing Error',
        'comment': 'Timing card error from the ADCP''s builtin test function',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'speed_of_sound': {
        'comment': 'Contains either manual or calculated speed of sound',
        'long_name': 'Speed of Sound',
        'units': 'm s-1',
    },
    'transducer_depth': {
        'long_name': 'Transducer Depth',
        'comment': 'Estimated deployment depth of the ADCP, entered during configuration. Reported in decimeters',
        'units': 'dm'
    },
    'heading': {
        'long_name': 'Heading',
        'comment': 'Measured heading of the ADCP, uncorrected for magnetic declination. Reported in decidegrees.',
        'units': 'ddegrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'comment': 'Measured pitch of the ADCP. Reported in decidegrees.',
        'units': 'ddegrees'
    },
    'roll': {
        'long_name': 'Roll',
        'comment': 'Measured roll of the ADCP. Reported in decidegrees.',
        'units': 'ddegrees'
    },
    'salinity': {
        'long_name': 'Transducer Salinity',
        'comment': ('Estimated salinity for the ADCP at the deployment site. Entered during configuration and used ' +
                    'to estimate the speed of sound.'),
        'units': '1'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'comment': 'In-situ sea water temperature measured at the transducer face, reported in centidegree Celsius.',
        'units': 'cdegrees_Celsius'
    },
    'mpt_minutes': {
        'long_name': 'MPT Minutes',
        'units': 'min',
        'comment': 'Minimum pre-ping wait time (MPT) between ping groups in the ensemble in minutes',
    },
    'mpt_seconds': {
        'comment': 'Minimum pre-ping wait time (MPT) between ping groups in the ensemble in seconds',
        'long_name': 'MPT Seconds',
        'units': 's',
    },
    'heading_stdev': {
        'long_name': 'Heading Standard Deviation',
        'comment': 'Standard deviation of the heading reported in degrees',
        'units': 'degrees',
    },
    'pitch_stdev': {
        'long_name': 'Pitch Standard Deviation',
        'comment': 'Standard deviation of the pitch reported in decidegrees',
        'units': 'ddegrees',
    },
    'roll_stdev': {
        'long_name': 'Roll Standard Deviation',
        'comment': 'Standard deviation of the roll reported in decidegrees',
        'units': 'ddegrees',
    },
    'adc_transmit_current': {
        'long_name': 'ADC Transmit Current',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the transmit current.',
        'units': 'counts',
    },
    'adc_transmit_voltage': {
        'long_name': 'ADC Transmit Voltage',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the transmit voltage.',
        'units': 'counts',
    },
    'adc_ambient_temp': {
        'long_name': 'ADC Ambient Temperature',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the ambient temperature.',
        'units': 'counts',
    },
    'adc_pressure_plus': {
        'long_name': 'ADC Pressure Plus',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the pressure+.',
        'units': 'counts',
    },
    'adc_pressure_minus': {
        'long_name': 'ADC Pressure Minus',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the pressure-.',
        'units': 'counts',
    },
    'adc_attitude_temp': {
        'units': 'counts',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the attitude temperature.',
        'long_name': 'ADC Attitude Temperature',
    },
    'adc_attitude': {
        'long_name': 'ADC Attitiude',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the attitude.',
        'units': 'counts',
    },
    'adc_contamination_sensor': {
        'long_name': 'ADC Contamination Sensor',
        'comment': 'Contains outputs of the A/D converter located on DSP board. Measures the contamination sensor.',
        'units': 'counts',
    },
    'bus_error_exception': {
        'long_name': 'Bus Error Exception',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'address_error_exception': {
        'long_name': 'Address Error Exception',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'illegal_instruction_exception': {
        'long_name': 'Illegal Instruction Exception',
        'comment': 'Recorded in the Error Status Word.'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'zero_divide_instruction': {
        'long_name': 'Zero Divide Instruction',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'emulator_exception': {
        'long_name': 'Emulator Exception',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'unassigned_exception': {
        'long_name': 'Unassigned Exception',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'watchdog_restart_occurred': {
        'long_name': 'Watchdog Restart Occurred',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'battery_saver_power': {
        'long_name': 'Battery Saver Power',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pinging': {
        'long_name': 'Pinging Error',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'cold_wakeup_occurred': {
        'long_name': 'Cold Wakeup Occurred',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'unknown_wakeup_occurred': {
        'long_name': 'Unknown Wakeup Occurred',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'clock_read_error': {
        'long_name': 'Clock Read Error',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'unexpected_alarm': {
        'long_name': 'Unexpected Alarm',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'clock_jump_forward': {
        'long_name': 'Clcok Jump Forward',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'clock_jump_backward': {
        'long_name': 'Clock Jump Backward',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'power_fail': {
        'long_name': 'Power Failure',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'spurious_dsp_interrupt': {
        'long_name': 'Spurious DSP Interrupt',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'spurious_uart_interrupt': {
        'long_name': 'Spurious UART Interrupt',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'spurious_clock_interrupt': {
        'long_name': 'Spurious Clock Interrupt',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'level_7_interrupt': {
        'long_name': 'Level 7 Interrupt',
        'comment': 'Recorded in the Error Status Word'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pressure': {
        'long_name': 'Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'comment': ('ADCP pressure sensor value. Reported in decaPascals. If the value is 0, the unit is not '
                    'equipped with a pressure sensor'),
        'units': 'daPa'
    },
    'pressure_variance': {
        'long_name': 'Pressure Variance',
        'comment': 'Variability in the pressure reading during the ensemble averaging period',
        'units': 'daPa'
    },

    # velocity packets
    'eastward_seawater_velocity_est': {
        'long_name': 'Estimated Eastward Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the eastward seawater velocity component uncorrected for magnetic ' +
                    'declination as reported by the instrument. Considered an estimate of the true eastward velocity ' +
                    'component while uncorrected for magnetic declination.'),
        'standard_name': 'eastward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLE_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'northward_seawater_velocity_est': {
        'long_name': 'Estimated Northward Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the northward seawater velocity component uncorrected for ' +
                    'magnetic declination as reported by the instrument. Considered an estimate of the true ' +
                    'northward velocity component while uncorrected for magnetic declination.'),
        'standard_name': 'northward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLN_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'vertical_seawater_velocity': {
        'long_name': 'Estimated Vertical Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the vertical seawater velocity component as reported by the ' +
                    'instrument'),
        'standard_name': 'upward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLU_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'error_velocity': {
        'long_name': 'Error Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the error velocity component as reported by the instrument.'),
        'data_product_identifier': 'VELPROF-EVL_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },

    # correlation magnitudes
    'correlation_magnitude_beam1': {
        'long_name': 'Correlation Magnitude Beam 1',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },
    'correlation_magnitude_beam2': {
        'long_name': 'Correlation Magnitude Beam 2',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },
    'correlation_magnitude_beam3': {
        'long_name': 'Correlation Magnitude Beam 3',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },
    'correlation_magnitude_beam4': {
        'long_name': 'Correlation Magnitude Beam 4',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },

    # echo intensities
    'echo_intensity_beam1': {
        'long_name': 'Echo Intensity Beam 1',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B1_L0',
        'units': 'counts'
    },
    'echo_intensity_beam2': {
        'long_name': 'Echo Intensity Beam 2',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B2_L0',
        'units': 'counts'
    },
    'echo_intensity_beam3': {
        'long_name': 'Echo Intensity Beam 3',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B3_L0',
        'units': 'counts'
    },
    'echo_intensity_beam4': {
        'long_name': 'Echo Intensity Beam 4',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B4_L0',
        'units': 'counts'
    },

    # percent good
    'percent_good_3beam': {
        'long_name': 'Percent Good 3 Beams',
        'comment': ('Percentage of velocity data collected in an ensemble average that were calculated with just 3 ' +
                    'beams.'),
        'units': 'percent'
    },
    'percent_transforms_reject': {
        'long_name': 'Percent Transforms Rejected',
        'comment': ('Percentage of transformations rejected in an ensemble average (error velocity that was higher ' +
                    'than the WE-command setting)'),
        'units': 'percent'
    },
    'percent_bad_beams': {
        'long_name': 'Percent Bad Beams',
        'comment': ('Percentage of velocity data collected in an ensemble average that were rejected because not ' +
                    'enough beams had good data.'),
        'units': 'percent'
    },
    'percent_good_4beam': {
        'long_name': 'Percent Good 4 Beams',
        'comment': 'Percentage of velocity data collected in an ensemble average that were calculated with all 4 beams',
        'units': 'percent'
    }
}

PD8 = {
    # variable leader
    'ensemble_number': {
        'long_name': 'Ensemble Number',
        'comment': 'Sequential number of the ensemble to which the data applies',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'bit_result': {
        'long_name': 'BIT Results',
        'comment': 'Summary result of the ADCP''s builtin test functions',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'speed_of_sound': {
        'comment': 'Contains calculated speed of sound based on transducer temperature and default salinity',
        'long_name': 'Speed of Sound',
        'units': 'm s-1',
    },
    'heading': {
        'long_name': 'Heading',
        'comment': 'Measured heading of the ADCP, uncorrected for magnetic declination',
        'units': 'degrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'comment': 'Measured pitch of the ADCP.',
        'units': 'degrees'
    },
    'roll': {
        'long_name': 'Roll',
        'comment': 'Measured roll of the ADCP',
        'units': 'degrees'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'comment': 'In-situ sea water temperature measured at the transducer face.',
        'units': 'degrees_Celsius'
    },

    # velocity packets
    'seawater_velocity_direction_est': {
        'long_name': 'Estimated Seawater Velocity Direction',
        'comment': ('Profile indicating direction water is travelling to. Corrected for instrument heading, pitch and ',
                    'roll, but uncorrected for magnetic declination. Considered an estimate of the true velocity ' +
                    'direction while uncorrected for magnetic declination.'),
        'units': 'degrees',
        '_FillValue': np.nan
    },
    'seawater_velocity_magnitude_est': {
        'long_name': 'Estimated Seawater Velocity Magnitude',
        'comment': ('Profile of water current velocities. Corrected for instrument heading, pitch and roll, but ' +
                    'uncorrected for magnetic declination. Considered an estimate of the true velocity magnitude ' +
                    'while uncorrected for magnetic declination.'),
        'units': 'mm s-1',
        '_FillValue': np.nan
    },
    'eastward_seawater_velocity_est': {
        'long_name': 'Estimated Eastward Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the eastward seawater velocity component uncorrected for magnetic ' +
                    'declination as reported by the instrument. Considered an estimate of the true eastward velocity ' +
                    'component while uncorrected for magnetic declination.'),
        'standard_name': 'eastward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLE_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'northward_seawater_velocity_est': {
        'long_name': 'Estimated Northward Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the northward seawater velocity component uncorrected for ' +
                    'magnetic declination as reported by the instrument. Considered an estimate of the true ' +
                    'northward velocity component while uncorrected for magnetic declination.'),
        'standard_name': 'northward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLN_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'vertical_seawater_velocity': {
        'long_name': 'Vertical Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the vertical seawater velocity component as reported by the ' +
                    'instrument'),
        'standard_name': 'upward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLU_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'error_velocity': {
        'long_name': 'Error Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the error velocity component as reported by the instrument.'),
        'data_product_identifier': 'VELPROF-EVL_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },

    # echo intensities
    'echo_intensity_beam1': {
        'long_name': 'Echo Intensity Beam 1',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B1_L0',
        'units': 'counts'
    },
    'echo_intensity_beam2': {
        'long_name': 'Echo Intensity Beam 2',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B2_L0',
        'units': 'counts'
    },
    'echo_intensity_beam3': {
        'long_name': 'Echo Intensity Beam 3',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B3_L0',
        'units': 'counts'
    },
    'echo_intensity_beam4': {
        'long_name': 'Echo Intensity Beam 4',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B4_L0',
        'units': 'counts'
    }
}

PD12 = {
    'imm_record_number': {
        'long_name': 'IMM Record Number',
        'comment': 'Inductive modem record number',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'ensemble_number': {
        'long_name': 'Ensemble Number',
        'comment': 'Sequential number of the ensemble to which the data applies',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'firmware_version': {
        'long_name': 'Firmware Version',
        'comment': 'Version number of current CPU firmware',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'firmware_revision': {
        'long_name': 'Firmware Revision',
        'comment': 'Revision number of current CPU firmware',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'heading': {
        'long_name': 'Heading',
        'comment': 'Measured heading of the ADCP, uncorrected for magnetic declination',
        'units': 'degrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'comment': 'Measured pitch of the ADCP.',
        'units': 'degrees'
    },
    'roll': {
        'long_name': 'Roll',
        'comment': 'Measured roll of the ADCP',
        'units': 'degrees'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'comment': 'In-situ sea water temperature measured at the transducer face.',
        'units': 'degrees_Celsius'
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'comment': 'ADCP pressure sensor value.',
        'units': 'daPa'
    },

    # velocity packets
    'eastward_seawater_velocity_est': {
        'long_name': 'Estimated Eastward Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the eastward seawater velocity component uncorrected for magnetic ' +
                    'declination as reported by the instrument. Considered an estimate of the true eastward velocity ' +
                    'component while uncorrected for magnetic declination.'),
        'standard_name': 'eastward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLE_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'northward_seawater_velocity_est': {
        'long_name': 'Estimated Northward Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the northward seawater velocity component uncorrected for ' +
                    'magnetic declination as reported by the instrument. Considered an estimate of the true ' +
                    'northward velocity component while uncorrected for magnetic declination.'),
        'standard_name': 'northward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLN_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'vertical_seawater_velocity': {
        'long_name': 'Vertical Seawater Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the vertical seawater velocity component as reported by the ' +
                    'instrument'),
        'standard_name': 'upward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLU_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    },
    'error_velocity': {
        'long_name': 'Error Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the error velocity component as reported by the instrument.'),
        'data_product_identifier': 'VELPROF-EVL_L0',
        'units': 'mm s-1',
        '_FillValue': np.int32(-32768)
    }
}

DERIVED = {
    # derived values
    'bin_depth': {
        'long_name': 'Bin Depths',
        'comment': ('Depths of the velocity bins estimated from either the measured ADCP pressure, ' +
                    'or the deployment depth, and associated parameters from the unit''s configuration.'),
        'units': 'm'
    },
    'bin_heights': {
        'long_name': 'Bin Heights',
        'comment': ('Height of the velocity bins above the bottom, estimated from either the measured ADCP pressure, ' +
                    'or the deployment depth, and associated parameters from the unit''s configuration.'),
        'units': 'm'
    },
    'ping_period': {
        'long_name': 'Ping Period',
        'comment': ('Contains the amount of time, in seconds, between pings in an ensemble. Derived from, and' +
                    'replaces, the time_per_ping_seconds and time_per_ping_minutes parameters in the fixed leader' +
                    'section of the raw data'),
        'units': 's'
    },
    'real_time_clock': {
        'long_name': 'Internal Real Time Clock',
        'comment': ('Date and time stamp from the ADCP''s real-time clock for when the ensemble measurement began.' +
                    'Combines data from, and replaces, the data from the two real_time_clock arrays contained in' +
                    'the variable leader section of the raw data. The data is then converted to a Unix epoch time ' +
                    'stamp (seconds since 1970-01-01)'),
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'calendar': 'gregorian'
    },
    'backscatter_beam1': {
        'long_name': 'Estimated Acoustic Backscatter Beam 1',
        'comment': ('Acoustic backscatter is the strength of the returned sound wave pulse transmitted by the ADCP. ' +
                    'Acoustic backscatter can be used as an indicator of the amount of sediment or organisms in the ' +
                    'water column, as well as the quality of a velocity measurement. It is estimated from the echo ' +
                    'intensity measurement using default conversion factors provided in the vendor documentation.'),
        'data_product_identifier': 'ECHOINT-B1_L1',
        'ancillary_variables': 'echo_intensity_beam1',
        'units': 'dB'
    },
    'backscatter_beam2': {
        'long_name': 'Estimated Acoustic Backscatter Beam 2',
        'comment': ('Acoustic backscatter is the strength of the returned sound wave pulse transmitted by the ADCP. ' +
                    'Acoustic backscatter can be used as an indicator of the amount of sediment or organisms in the ' +
                    'water column, as well as the quality of a velocity measurement. It is estimated from the echo ' +
                    'intensity measurement using default conversion factors provided in the vendor documentation.'),
        'data_product_identifier': 'ECHOINT-B2_L1',
        'ancillary_variables': 'echo_intensity_beam2',
        'units': 'dB'
    },
    'backscatter_beam3': {
        'long_name': 'Estimated Acoustic Backscatter Beam 3',
        'comment': ('Acoustic backscatter is the strength of the returned sound wave pulse transmitted by the ADCP. ' +
                    'Acoustic backscatter can be used as an indicator of the amount of sediment or organisms in the ' +
                    'water column, as well as the quality of a velocity measurement. It is estimated from the echo ' +
                    'intensity measurement using default conversion factors provided in the vendor documentation.'),
        'data_product_identifier': 'ECHOINT-B3_L1',
        'ancillary_variables': 'echo_intensity_beam3',
        'units': 'dB'
    },
    'backscatter_beam4': {
        'long_name': 'Estimated Acoustic Backscatter Beam 4',
        'comment': ('Acoustic backscatter is the strength of the returned sound wave pulse transmitted by the ADCP. ' +
                    'Acoustic backscatter can be used as an indicator of the amount of sediment or organisms in the ' +
                    'water column, as well as the quality of a velocity measurement. It is estimated from the echo ' +
                    'intensity measurement using default conversion factors provided in the vendor documentation.'),
        'data_product_identifier': 'ECHOINT-B4_L1',
        'ancillary_variables': 'echo_intensity_beam4',
        'units': 'dB'
    },
    'eastward_seawater_velocity': {
        'long_name': 'Eastward Seawater Velocity',
        'comment': ('Eastward sea water velocity component in Earth coordinates corrected for magnetic declination ' +
                    'and scaled to standard units of m s-1.'),
        'standard_name': 'eastward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLE_L1',
        'ancillary_variables': 'eastward_seawater_velocity_est, northward_seawater_velocity_est, time, lat, lon, z',
        'units': 'm s-1',
        '_FillValue': np.nan
    },
    'northward_seawater_velocity': {
        'long_name': 'Northward Seawater Velocity',
        'comment': ('Northward sea water velocity component in Earth coordinates corrected for magnetic declination ' +
                    'and scaled to standard units of m s-1.'),
        'standard_name': 'northward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLN_L1',
        'ancillary_variables': 'eastward_seawater_velocity_est, northward_seawater_velocity_est, time, lat, lon, z',
        'units': 'm s-1',
        '_FillValue': np.nan
    },
}
