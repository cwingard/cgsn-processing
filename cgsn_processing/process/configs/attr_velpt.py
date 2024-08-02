#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_velpt
@file cgsn_processing/process/configs/attr_velpt.py
@author Christopher Wingard
@brief Attributes for the Nortek Aquadopp (VELPT)
"""
import numpy as np

VELPT = {
    'global': {
        'title': 'Point Velocity Measurements from the Nortek Aquadopp',
        'summary': 'The aquadopp records 3 minute ensemble averages every 15 minutes of the point velocity.',
    },
    'error_code': {
        'long_name': 'Error Code',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Instrument error codes.',
        'flag_mask': np.array(2 ** np.array(range(0, 8)), dtype=object).astype(np.intc),
        'flag_meanings': ('compass_error measurement_data_error sensor_data_error tag_bit_error flash_error '
                          'undefined serial_ct_sensor_read_error undefined'),
        'ancillary_variables': 'error_code status_code'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'units': 'V',
        'comment': 'Reports either the internal battery voltage, or the external power applied, whichever is greater.'
    },
    'speed_of_sound': {
        'long_name': 'Speed of Sound',
        'units': 'm s-1',
        'comment': 'Contains either manual or calculated speed of sound'
    },
    'heading': {
        'long_name': 'Heading',
        'units': 'degrees',
        'comment': 'Measured heading of the instrument, uncorrected for magnetic declination',
        'ancillary_variables': 'error_code status_code'
    },
    'pitch': {
        'long_name': 'Pitch',
        'units': 'degrees',
        'comment': 'Measured pitch of the instrument.',
        'ancillary_variables': 'error_code status_code'
    },
    'roll': {
        'long_name': 'Roll',
        'units': 'degrees',
        'comment': 'Measured roll of the instrument',
        'ancillary_variables': 'error_code status_code'
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': 'Instrument pressure sensor value recorded in dbar.',
        'ancillary_variables': 'error_code status_code'
    },
    'status_code': {
        'long_name': 'Status Code',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Instrument status codes.',
        'flag_mask': np.array([1, 1, 2, 2, 4, 8, 48, 48, 48, 48, 192, 192, 192, 192], dtype=object).astype(np.intc),
        'flag_values': np.array([0, 1, 0, 2, 4, 8, 0, 16, 32, 48, 0, 64, 128, 192], dtype=object).astype(np.intc),
        'flag_meanings': ('orientation_up orientation_down sacaling_mm_per_second scaling_0.1mm_per_second '
                          'pitch_out_of_range roll_out_of_range wakeup_state_bad_power wakeup_state_break '
                          'wakeup_state_power_applied wakeup_state_rtc_alarm power_level_high power_level_mid_high '
                          'power_level_mid_low power_level_low')
        # Per https://cfconventions.org/cf-conventions/cf-conventions.html#flags, a blend of flag masks, flag values,
        # and flag meanings are used "to describe a blend of independent Boolean conditions and enumerated status
        # codes."
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'In-situ sea water temperature measured at the transducer face.',
        'ancillary_variables': 'error_code status_code'
    },
    'velocity_east': {
        'long_name': 'Estimated Eastward Seawater Velocity',
        'units': 'mm s-1',
        'comment': ('This is the eastward seawater velocity component uncorrected for magnetic declination as '
                    'reported by the instrument in mm/s.'),
        'data_product_identifier': 'VELPTMN-VLE_L0',
        'ancillary_variables': 'error_code status_code'
    },
    'velocity_north': {
        'long_name': 'Estimated Northward Seawater Velocity',
        'units': 'mm s-1',
        'comment': ('This is the northward seawater velocity component uncorrected for magnetic declination as '
                    'reported by the instrument in mm/s.'),
        'data_product_identifier': 'VELPTMN-VLN_L0',
        'ancillary_variables': 'error_code status_code'
    },
    'velocity_vertical': {
        'long_name': 'Vertical Seawater Velocity',
        'standard_name': 'upward_sea_water_velocity',
        'units': 'mm s-1',
        'comment': 'The vertical seawater velocity component as reported by the instrument in mm/s.',
        'data_product_identifier': 'VELPTMN-VLU_L0',
        'ancillary_variables': 'error_code status_code'
    },
    'amplitude_beam1': {
        'long_name': 'Amplitude Beam 1',
        'units': 'count',
        'comment': ('This is the raw measurement, the acoustic return signal for the beam, used to calculate the '
                    'seawater velocity. This value should be roughly equivalent to the other two beams. Significant '
                    'differences would suggest one or more of the beams is blocked or otherwise impaired.'),
        'ancillary_variables': 'error_code status_code'
    },
    'amplitude_beam2': {
        'long_name': 'Amplitude Beam 2',
        'units': 'count',
        'comment': ('This is the raw measurement, the acoustic return signal for the beam, used to calculate the '
                    'seawater velocity. This value should be roughly equivalent to the other two beams. Significant '
                    'differences would suggest one or more of the beams is blocked or otherwise impaired.'),
        'ancillary_variables': 'error_code status_code'
    },
    'amplitude_beam3': {
        'long_name': 'Amplitude Beam 3',
        'units': 'count',
        'comment': ('This is the raw measurement, the acoustic return signal for the beam, used to calculate the '
                    'seawater velocity. This value should be roughly equivalent to the other two beams. Significant '
                    'differences would suggest one or more of the beams is blocked or otherwise impaired.'),
        'ancillary_variables': 'error_code status_code'
    },
    # ---- derived values ----
    'eastward_seawater_velocity': {
        'long_name': 'Eastward Seawater Velocity',
        'standard_name': 'eastward_sea_water_velocity',
        'units': 'm s-1',
        'comment': ('Eastward sea water velocity component in Earth coordinates corrected for magnetic declination '
                    'and scaled to standard units of m s-1.'),
        'data_product_identifier': 'VELPTMN-VLE_L1',
        'ancillary_variables': 'velocity_east, velocity_north, time, lat, lon, z'
    },
    'northward_seawater_velocity': {
        'long_name': 'Northward Seawater Velocity',
        'standard_name': 'northward_sea_water_velocity',
        'units': 'm s-1',
        'comment': ('Northward sea water velocity component in Earth coordinates corrected for magnetic declination '
                    'and scaled to standard units of m s-1.'),
        'data_product_identifier': 'VELPTMN-VLN_L1',
        'ancillary_variables': 'velocity_east, velocity_north, time, lat, lon, z'
    }
}
