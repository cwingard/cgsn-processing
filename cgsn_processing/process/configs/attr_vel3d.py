#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_vel3d
@file cgsn_processing/process/configs/attr_vel3d.py
@author Christopher Wingard
@brief Attributes for the Nortek Vector Velocimeter (VEL3D)
"""
import numpy as np

VEL3D = {
    # global attributes
    'global': {
        'title': '3D Point Velocity Measurements from the Nortek Vector Velocimeter',
        'summary': ('The Nortek Velocimeters belong to a special class of high-resolution 3D instruments used to '
                    'study rapid velocity fluctuations in the laboratory or in the ocean. The Vector is a field '
                    'instrument designed for measurements of rapid small scale changes in 3D velocity, used for '
                    'turbulence, boundary layer measurements, surf zone measurements, and measurements in very '
                    'low flow areas.')
    },
    'noise_amplitude_beam1': {
        'long_name': 'Noise Amplitude Beam 1',
        'comment': ('Ambient noise amplitudes measured by beam 1 prior to a the collection of a 3 minute burst of '
                    '8 Hz velocity data and recorded in the header data packet.'),
        'units': 'counts'
    },
    'noise_amplitude_beam2': {
        'long_name': 'Noise Amplitude Beam 2',
        'comment': ('Ambient noise amplitudes measured by beam 2 prior to a the collection of a 3 minute burst of '
                    '8 Hz velocity data and recorded in the header data packet.'),
        'units': 'counts'
    },
    'noise_amplitude_beam3': {
        'long_name': 'Noise Amplitude Beam 3',
        'comment': ('Ambient noise amplitudes measured by beam 3 prior to a the collection of a 3 minute burst of '
                    '8 Hz velocity data and recorded in the header data packet.'),
        'units': 'counts'
    },
    'noise_correlation_beam1': {
        'long_name': 'Noise Correlation Beam 1',
        'comment': ('Ambient noise correlations measured by beam 1 prior to a the collection of a 3 minute burst of '
                    '8 Hz velocity data and recorded in the header data packet.'),
        'units': 'percent'
    },
    'noise_correlation_beam2': {
        'long_name': 'Noise Correlation Beam 2',
        'comment': ('Ambient noise correlations measured by beam 2 prior to a the collection of a 3 minute burst of '
                    '8 Hz velocity data and recorded in the header data packet.'),
        'units': 'percent'
    },
    'noise_correlation_beam3': {
        'long_name': 'Noise Correlation Beam 3',
        'comment': ('Ambient noise correlations measured by beam 3 prior to a the collection of a 3 minute burst of '
                    '8 Hz velocity data and recorded in the header data packet.'),
        'units': 'percent'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': 'Voltage of either the internal battery pack or externally supplied power, whichever is greater.',
        'units': 'V'
    },
    'speed_of_sound': {
        'long_name': 'Speed of Sound',
        'comment': ('Estimated speed of sound derived internally by the VEL3D from the temperature sensor '
                    'measurements and an assumed constant salinity of 33 psu.'),
        'units': 'm s-1'
    },
    'heading': {
        'long_name': 'Heading',
        'comment': 'Measured heading of the VEL3D, uncorrected for magnetic declination.',
        'units': 'degrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'comment': 'Measured pitch of the VEL3D.',
        'units': 'degrees'
    },
    'roll': {
        'long_name': 'Roll',
        'comment': 'Measured roll of the VEL3D.',
        'units': 'degrees'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'comment': 'In-situ sea water temperature measured at the base of the transducer stalk.',
        'units': 'degrees_Celsius'
    },
    'error_code': {
        'long_name': 'Instrument Error Codes',
        'flag_masks': np.array([1, 2, 4, 8, 16, 64], dtype=np.uint8),
        'flag_meanings': ('compass_error measurement_error sensor_data_error tag_bit_error '
                          'flash_error ct_sensor_read_error'),
        'comment': 'Integer representation of the instrument error codes.'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'status_code': {
        'long_name': 'Instrument Status Codes',
        'flag_masks': np.array([1, 2, 4, 8, 48, 48, 48, 48, 192, 192, 192, 192], dtype=np.uint8),
        'flag_values': np.array([1, 2, 4, 8, 0, 16, 32, 48, 0, 64, 128, 192], dtype=np.uint8),
        'flag_meanings': ('orientation_down scaling_factor_0.1 pitch_out_of_range roll_out_of_range '
                          'wake_bad_power wake_break_received wake_power_applied wake_rtc_alarm '
                          'power_level_high power_level_1 power_level_2 power_level_low'),
        'comment': 'Integer representation of the instrument status codes.'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pressure': {
        'long_name': 'Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'comment': 'Sea water pressure measured at the base of the transducer stalk.',
        'units': 'dbar'
    },
    'velocity_east': {
        'long_name': 'Estimated Eastward Sea Water Velocity',
        'comment': 'Estimated eastward sea water velocity uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLE_L0',
        'units': 'mm s-1',
    },
    'velocity_east_corrected': {
        'long_name': 'Eastward Sea Water Velocity',
        'standard_name': 'eastward_sea_water_velocity',
        'comment': 'Eastward sea water velocity corrected for magnetic declination and scaled to m/s.',
        'data_product_identifier': 'VELPTTU-VLE_L1',
        'units': 'm s-1',
    },
    'velocity_north': {
        'long_name': 'Estimated Northward Sea Water Velocity',
        'comment': 'Estimated northward sea water velocity uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLN_L0',
        'units': 'mm s-1',
    },
    'velocity_north_corrected': {
        'long_name': 'Northward Sea Water Velocity',
        'standard_name': 'northward_sea_water_velocity',
        'comment': 'Northward sea water velocity corrected for magnetic declination and scaled to m/s.',
        'data_product_identifier': 'VELPTTU-VLN_L1',
        'units': 'm s-1',
    },
    'velocity_vertical': {
        'long_name': 'Upward Sea Water Velocity',
        'standard_name': 'upward_sea_water_velocity',
        'comment': 'Vertical sea water velocity component.',
        'data_product_identifier': 'VELPTTU-VLU_L0',
        'units': 'mm s-1',
    },
    'amplitude_beam1': {
        'long_name': 'Velocity Amplitude Beam 1',
        'comment': ('Raw measurement, for beam 1, of the difference in frequency between the transmitted '
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'amplitude_beam2': {
        'long_name': 'Velocity Amplitude Beam 2',
        'comment': ('Raw measurement, for beam 2, of the difference in frequency between the transmitted '
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'amplitude_beam3': {
        'long_name': 'Velocity Amplitude Beam 3',
        'comment': ('Raw measurement, for beam 3, of the difference in frequency between the transmitted '
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'correlation_beam1': {
        'long_name': 'Percent Correlation Beam 1',
        'comment': ('Percent correlation, for beam 1, is a measure of the similarity of two pulse echoes being '
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between '
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high '
                    'correlation because it gives us confidence the system measured the two pulses it originally '
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    },
    'correlation_beam2': {
        'long_name': 'Percent Correlation Beam 2',
        'comment': ('Percent correlation, for beam 2, is a measure of the similarity of two pulse echoes being '
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between '
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high '
                    'correlation because it gives us confidence the system measured the two pulses it originally '
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    },
    'correlation_beam3': {
        'long_name': 'Percent Correlation Beam 3',
        'comment': ('Percent correlation, for beam 3, is a measure of the similarity of two pulse echoes being '
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between '
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high '
                    'correlation because it gives us confidence the system measured the two pulses it originally '
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    }
}
