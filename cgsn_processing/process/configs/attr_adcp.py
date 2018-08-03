#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_adcp
@file cgsn_processing/process/configs/attr_adcp.py
@author Christopher Wingard
@brief Attributes for the common ADCP and specific PD0, PD8 and PD12 data set variables
"""

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
        'institution': 'Coastal and Global Scales Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
        'feature_type': 'timeSeriesProfile',
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
    },

    # PD0 header
'num_bytes': {
        'long_name': '',
        'comment': ''
    },
'num_data_types': {
        'long_name': '',
        'comment': ''
    },

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
        'comment': 'Transducer head beam pattern',
        'long_name': 'Sysconfig Beam Pattern',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sysconfig_sensor_config': {
        'comment': 'Sensor configuration number (1, 2 or 3)',
        'long_name': 'Sysconfig Sensor Config',
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
        'comment': 'Number of beams used to calculate velocity data',
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
    'time_per_ping_minutes': {
        'long_name': 'Time Per Ping',
        'comment': 'Contains the amount of time, in minutes, between pings in an ensemble.',
        'units': 'min'
    },
    'time_per_ping_seconds': {
        'long_name': 'Time Per Ping',
        'comment': 'Contains the amount of time, in seconds, between pings in an ensemble.',
        'units': 's'
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
        'comment': 'Correction factor for physical heading misalignment',
        'long_name': 'Heading Alignment',
        'units': 'cdegrees'
    },
    'heading_bias': {
        'long_name': 'Heading Bias',
        'comment': 'Correction factor for electrical/magnetic heading bias (e.g. Magnetic declination).',
        'units': 'cdegrees'
    },
    'sensor_source_speed': {
        'long_name': 'Sensor Source Speed',
        'comment': 'Whether speed of sound was calculated from depth, salinity and temperature?',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_depth': {
        'long_name': 'Sensor Source Depth',
        'comment': 'Uses ED from depth sensor?',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_heading': {
        'long_name': 'Sensor Source Heading',
        'comment': 'Uses EH from transducer heading?',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_pitch': {
        'long_name': 'Sensor Source Pitch',
        'comment': 'Uses EP from transducer pitch sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_roll': {
        'long_name': 'Sensor Source Roll',
        'comment': 'Uses ER from transducer roll sensor',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_conductivity': {
        'long_name': 'Sensor Source Conductivity',
        'comment': 'Uses ES (salinity) calculated from external conductivity sensor?',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_source_temperature': {
        'long_name': 'Sensor Source Temperature',
        'comment': 'Uses ET from transducer temperature sensor?',
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
        'long_name': '',
        'comment': ''
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
        'comment': 'System configuration for beam angle, 0 = 15E, 1 = 20E, 2 = 30E, 4 = Other',
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
'ensemble_number_increment': {
        'long_name': '',
        'comment': ''
    },
'real_time_clock1': {
        'long_name': '',
        'comment': ''
    },
'bit_result_demod_1': {
        'long_name': '',
        'comment': ''
    },
'bit_result_demod_2': {
        'long_name': '',
        'comment': ''
    },
'bit_result_timing': {
        'long_name': '',
        'comment': ''
    },
'speed_of_sound': {
        'long_name': '',
        'comment': ''
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
        'long_name': 'Transducer Temperature',
        'comment': 'Measured temperature at the transducer face, reported in centidegree Celsius.',
        'units': 'cdegree_Celsius'
    },
'mpt_minutes': {
        'long_name': '',
        'comment': ''
    },
'mpt_seconds': {
        'long_name': '',
        'comment': ''
    },
'heading_stdev': {
        'long_name': '',
        'comment': ''
    },
'pitch_stdev': {
        'long_name': '',
        'comment': ''
    },
'roll_stdev': {
        'long_name': '',
        'comment': ''
    },
'adc_transmit_current': {
        'long_name': '',
        'comment': ''
    },
'adc_transmit_voltage': {
        'long_name': '',
        'comment': ''
    },
'adc_ambient_temp': {
        'long_name': '',
        'comment': ''
    },
'adc_pressure_plus': {
        'long_name': '',
        'comment': ''
    },
'adc_pressure_minus': {
        'long_name': '',
        'comment': ''
    },
'adc_attitude_temp': {
        'long_name': '',
        'comment': ''
    },
'adc_attitude': {
        'long_name': '',
        'comment': ''
    },
'adc_contamination_sensor': {
        'long_name': '',
        'comment': ''
    },
'bus_error_exception': {
        'long_name': '',
        'comment': ''
    },
'address_error_exception': {
        'long_name': '',
        'comment': ''
    },
'illegal_instruction_exception': {
        'long_name': '',
        'comment': ''
    },
'zero_divide_instruction': {
        'long_name': '',
        'comment': ''
    },
'emulator_exception': {
        'long_name': '',
        'comment': ''
    },
'unassigned_exception': {
        'long_name': '',
        'comment': ''
    },
'watchdog_restart_occurred': {
        'long_name': '',
        'comment': ''
    },
'battery_saver_power': {
        'long_name': '',
        'comment': ''
    },
'pinging': {
        'long_name': '',
        'comment': ''
    },
'cold_wakeup_occurred': {
        'long_name': '',
        'comment': ''
    },
'unknown_wakeup_occurred': {
        'long_name': '',
        'comment': ''
    },
'clock_read_error': {
        'long_name': '',
        'comment': ''
    },
'unexpected_alarm': {
        'long_name': '',
        'comment': ''
    },
'clock_jump_forward': {
        'long_name': '',
        'comment': ''
    },
'clock_jump_backward': {
        'long_name': '',
        'comment': ''
    },
'power_fail': {
        'long_name': '',
        'comment': ''
    },
'spurious_dsp_interrupt': {
        'long_name': '',
        'comment': ''
    },
'spurious_uart_interrupt': {
        'long_name': '',
        'comment': ''
    },
'spurious_clock_interrupt': {
        'long_name': '',
        'comment': ''
    },
'level_7_interrupt': {
        'long_name': '',
        'comment': ''
    },
    'pressure': {
        'long_name': 'Pressure',
        'comment': 'ADCP pressure sensor value. Reported in decaPascals',
        'units': 'daPa'
    },
    'pressure_variance': {
        'long_name': 'Pressure Variance',
        'comment': 'Variability in the pressure reading during the ensemble averaging period',
        'units': 'daPa'
    },
'real_time_clock': {
        'long_name': '',
        'comment': ''
    },

    # velocity packets
    'eastward': {
        'long_name': 'Eastward Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the eastward seawater velocity component uncorrected for magnetic ' +
                    'declination as reported by the instrument.'),
        'data_product_identifier': 'VELPROF-VLE_L0',
        'units': 'mm/s'
    },
    'northward': {
        'long_name': 'Northward Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the northward seawater velocity component uncorrected for ' +
                    'magnetic declination as reported by the instrument.'),
        'data_product_identifier': 'VELPROF-VLN_L0',
        'units': 'mm/s'
    },
    'vertical': {
        'long_name': 'Vertical Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the vertical seawater velocity component as reported by the ' +
                    'instrument'),
        'data_product_identifier': 'VELPROF-VLU_L0',
        'units': 'mm/s'
    },
    'error': {
        'long_name': 'Error Velocity',
        'comment': ('A velocity profile includes water velocity (speed & direction) throughout the depth range of an ' +
                    'ADCP sensor. This instance is the error velocity component as reported by the instrument.'),
        'data_product_identifier': 'VELPROF-EVL_L0',
        'units': 'mm/s'
    },

    # correlation magnitudes
    'magnitude_beam1': {
        'long_name': 'Correlation Magnitude Beam 1',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },
    'magnitude_beam2': {
        'long_name': 'Correlation Magnitude Beam 2',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },
    'magnitude_beam3': {
        'long_name': 'Correlation Magnitude Beam 3',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },
    'magnitude_beam4': {
        'long_name': 'Correlation Magnitude Beam 4',
        'comment': ('Magnitude of the normalized echo auto-correlation at the lag used for estimating the Doppler ' +
                    'phase change. 0 represents no correlation and 255 represents perfect correlation.'),
        'units': 'counts'
    },

    # echo intensities
    'intensity_beam1': {
        'long_name': 'Echo Intensity Beam 1',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B1_L0',
        'units': 'counts'
    },
    'intensity_beam2': {
        'long_name': 'Echo Intensity Beam 2',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B2_L0',
        'units': 'counts'
    },
    'intensity_beam3': {
        'long_name': 'Echo Intensity Beam 3',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B3_L0',
        'units': 'counts'
    },
    'intensity_beam4': {
        'long_name': 'Echo Intensity Beam 4',
        'comment': ('Echo Intensity is the acoustic return signal per beam that is output directly from the ADCP. ' +
                    'This is the raw measurement used to calculate the echo intensity data product for the beam.'),
        'data_product_identifier': 'ECHOINT-B4_L0',
        'units': 'counts'
    },

    # percent good
    'good_3beam': {
        'long_name': 'Percent Good 3Beam',
        'comment': ('Percentage of good 3-beam solutions in an ensemble average (successful velocity calculations ' +
                    'using 3-beams).'),
        'units': 'percent'
    },
    'transforms_reject': {
        'long_name': 'Percent Transforms Rejected',
        'comment': ('Percentage of transformations rejected in an ensemble average (error velocity that was higher ' +
                    'than the WE-command setting)'),
        'units': 'percent'
    },
    'bad_beams': {
        'long_name': 'Percent Bad Beams',
        'comment': ('Percentage of velocity data collected in an ensemble average that were rejected because not ' +
                    'enough beams had good data.'),
        'units': 'percent'
    },
    'good_4beam': {
        'long_name': 'Percent Good 4 Beams',
        'comment': 'Percentage of velocity data collected in an ensemble average that were calculated with all 4 beams',
        'units': 'percent'
    },

    # derived values
    'bin_depths': {
        'long_name': 'Bin Depths',
        'comment': ('Depths of the velocity bins estimated from the measured ADCP pressure and associated parameters ' +
                    'from the unit''s configuration.'),
        'ancillary_variables': 'pressure,depth_cell_length,sysconfig_vertical_orientation,bin_1_distance,num_cells,z',
        'units': 'm'
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
                    'and scaled to standard units of m/s.'),
        'standard_name': 'eastward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLE_L1',
        'ancillary_variables': 'eastward, northward, time, lat, lon, z',
        'units': 'm/s'
    },
    'northward_seawater_velocity': {
        'long_name': 'Northward Seawater Velocity',
        'comment': ('Northward sea water velocity component in Earth coordinates corrected for magnetic declination ' +
                    'and scaled to standard units of m/s.'),
        'standard_name': 'northward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLN_L1',
        'ancillary_variables': 'eastward, northward, time, lat, lon, z',
        'units': 'm/s'
    },
    'vertical_seawater_velocity': {
        'long_name': 'Vertical Seawater Velocity',
        'comment': 'Vertical sea water velocity component scaled to standard units of m/s.',
        'standard_name': 'upward_sea_water_velocity',
        'data_product_identifier': 'VELPROF-VLU_L1',
        'ancillary_variables': 'vertical',
        'units': 'm/s'
    },
    'error_velocity': {
        'long_name': 'Error Velocity',
        'comment': 'Error velocity component scaled to standard units of m/s.',
        'data_product_identifier': 'VELPROF-EVL_L1',
        'ancillary_variables': 'error',
        'units': 'm/s'
    }
}
