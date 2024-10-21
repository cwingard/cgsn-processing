#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_adcpu
@file cgsn_processing/process/configs/attr_adcpu.py
@author Paul Whelan
@brief Attributes for the Nortek Aquadopp 2 (ADCPU)
"""
import numpy as np

ADCPU = {
    # global attributes
    'global': {
        'title': '3D Point Velocity Measurements from the Nortek Aquadopp 2',
        'summary': ('The Nortek Aquadopp 2  ' +
                    '...'),
    },
    'cell_number': {
        'long_name': 'Cell number',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Instrument reported cell number'
    },
    'instrument_name': {
        'long_name': 'Instrument name',
        'comment': 'Name of the instrument in use',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'instrument_type': {
        'long_name': 'Instrument type',
        'comment': '0-Aquadopp 1-Aquadopp profiler 2-Signature',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'number_beams': {
        'long_name': 'Number Beams',
        'comment': 'Contains the number of beams used to calculate velocity data',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'number_cells': {
        'long_name': 'Number Cells',
        'comment': 'Contains the number of cells over which the Aquadopp 2 collects data',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'cell_size': {
        'long_name': 'Cell Size',
        'comment': 'Contains the depth of one cell length',
        'units': 'm'
    },
    'coordinate_system': {
        'long_name': 'Coordinate system used: 0-ENU, 1-XYZ, 2-BEAM',
        'comment': 'Index indicating the coordinate system in use',
        # 'units': '',     deliberately left blank, no units for this value
    },
    'blanking': {
        'long_name': 'Blank After Transmit Distance',
        'comment': ('Contains the blanking distance used by the Aquadopp 2 to allow the transmit circuits time '
                    'to recover before receive cycle begins'),
        'units': 'm'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': 'Voltage of either the internal battery pack or externally supplied power, whichever is greater.',
        'units': 'V'
    },
    'sound_speed': {
        'long_name': 'Speed of Sound',
        'comment': ('Estimated speed of sound derived internally by the VEL3D from the temperature sensor ' +
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
        'flag_meanings': ('compass_error measurement_error sensor_data_error tag_bit_error ' +
                          'flash_error ct_sensor_read_error'),
        'comment': 'Integer representation of the instrument error codes.'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'status_code': {
        'long_name': 'Instrument Status Codes',
        'flag_masks': np.array([1, 2, 4, 8, 48, 48, 48, 48, 192, 192, 192, 192], dtype=np.uint8),
        'flag_values': np.array([1, 2, 4, 8, 0, 16, 32, 48, 0, 64, 128, 192], dtype=np.uint8),
        'flag_meanings': ('orientation_down scaling_factor_0.1 pitch_out_of_range roll_out_of_range ' +
                          'wake_bad_power wake_break_received wake_power_applied wake_rtc_alarm ' +
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
    'analog_in_1': {
        'long_name': 'Analog input 1',
        'comment': 'Analog input 1 data values',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'analog_in_2': {
        'long_name': 'Analog input 2',
        'comment': 'Analog input 2 data values',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'velocity_beam_1': {
        'long_name': 'Sea Water Velocity axis 1',
        'comment': 'sea water velocity axis 1 uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLE_L0',
        'units': 'm s-1',
    },
    'velocity_beam_2': {
        'long_name': 'Sea Water Velocity axis 2',
        'comment': 'Sea water velocity axis 2 uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLN_L0',
        'units': 'm s-1',
    },
    'velocity_beam_3': {
        'long_name': 'Sea Water Velocity axis 3',
        'comment': 'Sea water velocity axis 3 uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLU_L0',
        'units': 'm s-1',
    },
    'velocity_east_corrected': {
        'long_name': 'Eastward Sea Water Velocity',
        'standard_name': 'eastward_sea_water_velocity',
        'comment': 'Eastward sea water velocity corrected for magnetic declination and scaled to m/s.',
        'data_product_identifier': 'VELPTTU-VLE_L1',
        'units': 'm s-1',
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
        'units': 'm s-1',
    },
    'speed': {
        'long_name': 'Speed, of what?',
        'comment': 'Speed of ?',
        'units': 'm s-1',
    },
    'direction': {
        'long name': 'Direction, of what?',
        'comment': 'Direction of ?',
        'units': 'degrees',
    },
    'amplitude_beam_1': {
        'long_name': 'Velocity Amplitude Beam 1',
        'comment': ('Raw measurement, for beam 1, of the difference in frequency between the transmitted ' +
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'amplitude_beam_2': {
        'long_name': 'Velocity Amplitude Beam 2',
        'comment': ('Raw measurement, for beam 2, of the difference in frequency between the transmitted ' +
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'amplitude_beam_3': {
        'long_name': 'Velocity Amplitude Beam 3',
        'comment': ('Raw measurement, for beam 3, of the difference in frequency between the transmitted ' +
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'correlation_beam_1': {
        'long_name': 'Percent Correlation Beam 1',
        'comment': ('Percent correlation, for beam 1, is a measure of the similarity of two pulse echoes being ' +
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between ' +
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high ' +
                    'correlation because it gives us confidence the system measured the two pulses it originally ' +
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    },
    'correlation_beam_2': {
        'long_name': 'Percent Correlation Beam 2',
        'comment': ('Percent correlation, for beam 2, is a measure of the similarity of two pulse echoes being ' +
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between ' +
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high ' +
                    'correlation because it gives us confidence the system measured the two pulses it originally ' +
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    },
    'correlation_beam_3': {
        'long_name': 'Percent Correlation Beam 3',
        'comment': ('Percent correlation, for beam 3, is a measure of the similarity of two pulse echoes being ' +
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between ' +
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high ' +
                    'correlation because it gives us confidence the system measured the two pulses it originally ' +
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    }
}
