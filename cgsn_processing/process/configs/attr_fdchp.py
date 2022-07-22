#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_fdchp
@file cgsn_processing/process/configs/attr_fdchp.py
@author Christopher Wingard
@brief Attributes for the FDCHP variables
"""

FDCHP = {
    'global': {
        'title': 'Summarized Flux Direct Covariance Sensor Measurements',
        'summary': 'Records the hourly summarized flux direct covariance measurements from the FDCHP.',
    },
    'start_time': {
        'long_name': 'Start Time',
        'standard_name': 'time',
        'comment': ('Instrument start time, recorded as seconds since 1970-01-01. Can be compared to the time record '
                    'recorded by the DCL clock to determine the average measurement time.'),
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'calendar': 'gregorian'
    },
    'processing_version': {
        'long_name': 'Processing Version',
        # 'units': ''    # deliberately left blank, no units for this value
        'comment': 'Version number of the processing software used by the FDCHP.'
    },
    'status': {
        'long_name': 'Status',
        # 'units': ''    # deliberately left blank, no units for this value
        'comment': ('Six character hex string representing the status of the different instruments and calculations '
                    'used by the instrument. The order (from left to right) of the status values corresponds to W ('
                    'wind),  R (rates), A (acceleration), O (heading, pitch and roll), C (conditions), and F (flux '
                    'calculations). No further information is available at this time to further decode the '
                    'status flags.')
    },
    'avg_wind_u': {
        'long_name': 'U-Axis Wind Speed',
        'units': 'm s-1',
        'comment': ('Average wind speed along the instrument''s U-Axis. Positive U-Axis velocities are towards the '
                    'instrument''s reference spar. Normally this spar is aligned to North, but it is used, '
                    'in this case, to align the instrument with the wind vane, or x-axis, of the buoy. Thus, '
                    'U-Axis velocities are generally positive in this coordinate system as the wind blows towards  '
                    'the wind vane; the vane orients the x-axis of the buoy so it is facing into the wind.'),
        'ancillary_variables': 'std_wind_u max_wind_u min_wind_u'
    },
    'avg_wind_v': {
        'long_name': 'V-Axis Wind Speed',
        'units': 'm s-1',
        'comment': ('Average wind speed along the instrument''s V-Axis. Positive V-Axis velocities are towards the '
                    'left (90 degrees counter-clockwise) of the instrument''s reference spar. Relative to the buoy, '
                    'positive V-Axis velocities are to the port (along the y-axis of the buoy) of the wind vane.'),
        'ancillary_variables': 'std_wind_v max_wind_v min_wind_v'
    },
    'avg_wind_w': {
        'long_name': 'W-Axis Wind Speed',
        'units': 'm s-1',
        'comment': ('Average wind speed along the instrument''s W-Axis. Positive W-Axis velocities are defined as '
                    'vertically up the instrument''s mounting shaft (the buoy''s z-axis).'),
        'ancillary_variables': 'std_wind_w max_wind_w min_wind_w'
    },
    'speed_of_sound': {
        'long_name': 'Speed of Sound',
        'units': 'm s-1',
        'comment': 'Average speed of sound measured during the sampling period.',
        'ancillary_variables': 'std_speed_of_sound max_speed_of_sound min_speed_of_sound'
    },
    'std_wind_u': {
        'long_name': 'Standard Deviation U-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Standard deviation of the U-Axis wind velocities measured during the sampling period.'
    },
    'std_wind_v': {
        'long_name': 'Standard Deviation V-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Standard deviation of the V-Axis wind velocities measured during the sampling period.'
    },
    'std_wind_w': {
        'long_name': 'Standard Deviation W-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Standard deviation of the W-Axis wind velocities measured during the sampling period.'
    },
    'std_speed_of_sound': {
        'long_name': 'Standard Deviation Speed of Sound',
        'units': 'm s-1',
        'comment': 'Standard deviation of the speed of sound measured during the sampling period.'
    },
    'max_wind_u': {
        'long_name': 'Maximum U-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Maximum of the U-Axis wind velocities measured during the sampling period.'
    },
    'max_wind_v': {
        'long_name': 'Maximum V-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Maximum of the V-Axis wind velocities measured during the sampling period.',
    },
    'max_wind_w': {
        'long_name': 'Maximum W-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Maximum of the W-Axis wind velocities measured during the sampling period.'
    },
    'max_speed_of_sound': {
        'long_name': 'Maximum Speed of Sound',
        'units': 'm s-1',
        'comment': 'Maximum of the speed of sound measured during the sampling period.'
    },
    'min_wind_u': {
        'long_name': 'Minimum U-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Minimum of the U-Axis wind velocities measured during the sampling period.'
    },
    'min_wind_v': {
        'long_name': 'Minimum V-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Minimum of the V-Axis wind velocities measured during the sampling period.'
    },
    'min_wind_w': {
        'long_name': 'Minimum W-Axis Wind Speed',
        'units': 'm s-1',
        'comment': 'Minimum of the W-Axis wind velocities measured during the sampling period.'
    },
    'min_speed_of_sound': {
        'long_name': 'Minimum Speed of Sound',
        'units': 'm s-1',
        'comment': 'Minimum of the speed of sound measured during the sampling period.'
    },
    'acceleration_x': {
        'long_name': 'X-axis Acceleration',
        'units': 'm s-2',
        'comment': ('This is a vector quantifying the direction and magnitude of the average acceleration that the '
                    'buoy is exposed to during the sampling period. It is expressed in terms of the instrument''s '
                    'local coordinate system. The x-axis of the instrument is aligned with the buoy wind vane, such '
                    'that a positive x is pointing towards the buoy''s wind vane.'),
        'ancillary_variables': 'std_acc_x max_acc_x min_acc_x'
    },
    'acceleration_y': {
        'long_name': 'Y-axis Acceleration',
        'units': 'm s-2',
        'comment': ('This is a vector quantifying the direction and magnitude of the average acceleration that the '
                    'buoy is exposed to during the sampling period. It is expressed in terms of the instrument''s '
                    'local coordinate system. The y-axis of the instrument is aligned perpendicular to the buoy wind '
                    'vane, such that a postive y is to the port (90 degrees counter-clockwise) of the vane.'),
        'ancillary_variables': 'std_acc_y max_acc_y min_acc_y'
    },
    'acceleration_z': {
        'long_name': 'Z-axis Acceleration',
        'units': 'm s-2',
        'comment': ('This is a vector quantifying the direction and magnitude of the average acceleration that the '
                    'buoy is exposed to during the sampling period. It is expressed in terms of the instrument''s '
                    'local coordinate system. The z-axis is aligned vertically with the buoy, such that a positive '
                    'z is pointing upwards.'),
        'ancillary_variables': 'std_acc_z max_acc_z min_acc_z'
    },
    'std_acc_x': {
        'long_name': 'Standard Deviation X-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Standard deviation of the X-axis acceleration measured during the sampling period.'
    },
    'std_acc_y': {
        'long_name': 'Standard Deviation Y-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Standard deviation of the Y-axis acceleration measured during the sampling period.'
    },
    'std_acc_z': {
        'long_name': 'Standard Deviation Z-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Standard deviation of the Z-axis acceleration measured during the sampling period.'
    },
    'max_acc_x': {
        'long_name': 'Maximum X-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Maximum of the X-axis acceleration measured during the sampling period.'
    },
    'max_acc_y': {
        'long_name': 'Maximum Y-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Maximum of the Y-axis acceleration measured during the sampling period.'
    },
    'max_acc_z': {
        'long_name': 'Maximum Z-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Maximum of the Z-axis acceleration measured during the sampling period.'
    },
    'min_acc_x': {
        'long_name': 'Minimum X-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Minimum of the X-axis acceleration measured during the sampling period.'
    },
    'min_acc_y': {
        'long_name': 'Minimum Y-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Minimum of the Y-axis acceleration measured during the sampling period.'
    },
    'min_acc_z': {
        'long_name': 'Minimum Z-Axis Acceleration',
        'units': 'm s-2',
        'comment': 'Minimum of the Z-axis acceleration measured during the sampling period.'
    },
    'rate_x': {
        'long_name': 'X-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the average rate of rotation of the buoy during the sampling period. '
                    'It is expressed in terms of the instrument''s local coordinate system (in this case the X-axis) '
                    'in units of radians/second.')
    },
    'rate_y': {
        'long_name': 'Y-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the average rate of rotation of the buoy during the sampling period. '
                    'It is expressed in terms of the instrument''s local coordinate system (in this case the Y-axis) '
                    'in units of radians/second.')
    },
    'rate_z': {
        'long_name': 'Z-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the average rate of rotation of the buoy during the sampling period. '
                    'It is expressed in terms of the instrument''s local coordinate system (in this case the Z-axis) '
                    'in units of radians/second.')
    },
    'std_rate_x': {
        'long_name': 'Standard Deviation X-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Standard deviation of the X-axis angular rate of rotation measured during the sampling period.'
    },
    'std_rate_y': {
        'long_name': 'Standard Deviation Y-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Standard deviation of the Y-axis angular rate of rotation measured during the sampling period.'
    },
    'std_rate_z': {
        'long_name': 'Standard Deviation Z-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Standard deviation of the Z-axis angular rate of rotation measured during the sampling period.'
    },
    'max_rate_x': {
        'long_name': 'Maximum X-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Maximum of the X-axis angular rate of rotation measured during the sampling period.'
    },
    'max_rate_y': {
        'long_name': 'Maximum Y-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Maximum of the Y-axis angular rate of rotation measured during the sampling period.'
    },
    'max_rate_z': {
        'long_name': 'Maximum Z-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Maximum of the Z-axis angular rate of rotation measured during the sampling period.'
    },
    'min_rate_x': {
        'long_name': 'Minimum X-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Minimum of the X-axis angular rate of rotation measured during the sampling period.'
    },
    'min_rate_y': {
        'long_name': 'Minimum Y-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Minimum of the Y-axis angular rate of rotation measured during the sampling period.'
    },
    'min_rate_z': {
        'long_name': 'Minimum Z-axis Angular Rate',
        'units': 'radians/s',
        'comment': 'Minimum of the Z-axis angular rate of rotation measured during the sampling period.'
    },
    'heading': {
        'long_name': 'Heading',
        'standard_name': 'platform_orientation',
        'units': 'radians',
        'comment': ('The heading (or yaw) follows a right-hand rule, such that the heading is positive when the '
                    'instrument is rotated counter-clockwise around positive-z of the z-axis. In the buoy reference, '
                    'this means that the buoy is rotating to port. Note that the right-handed definition of heading '
                    'used here is opposite the typical left-handed definition used for a compass.')
    },
    'pitch': {
        'long_name': 'Pitch',
        'standard_name': 'platform_pitch',
        'units': 'radians',
        'comment': ('Pitch is rotation about an axis that is perpendicular to both the local upward axis and the '
                    'nominal forward motion direction of the instrument. Pitch is relative to the "at rest" rotation '
                    'of the instrument with respect to the axis of rotation. In the buoy reference frame, the pitch '
                    'is positive when the positive-x of the x-axis (aligned with, and facing the wind vane) is pitched '
                    'down.')
    },
    'roll': {
        'long_name': 'Roll',
        'standard_name': 'platform_roll',
        'units': 'radians',
        'comment': ('Roll is rotation about an axis that is perpendicular to the local upward axis and is coplanar '
                    'with the nominal forward motion direction of the platform. Roll is relative to the "at rest" '
                    'rotation of the platform with respect to the axis of rotation. In the buoy reference frame, '
                    'roll is positive when the positive-y of the y-axis (port side of the buoy when facing the wind '
                    'vane) is rolled up.')
    },
    'std_heading': {
        'long_name': 'Standard Deviation Heading',
        'units': 'radians',
        'comment': 'Standard deviation of the heading measured during the sampling period.'
    },
    'std_pitch': {
        'long_name': 'Standard Deviation Pitch',
        'units': 'radians',
        'comment': 'Standard deviation of the pitch measured during the sampling period.'
    },
    'std_roll': {
        'long_name': 'Standard Deviation Roll',
        'units': 'radians',
        'comment': 'Standard deviation of the roll measured during the sampling period.'
    },
    'max_heading': {
        'long_name': 'Maximum Heading',
        'units': 'radians',
        'comment': 'Maximum of the heading measured during the sampling period.'
    },
    'max_pitch': {
        'long_name': 'Maximum Pitch',
        'units': 'radians',
        'comment': 'Maximum of the pitch measured during the sampling period.'
    },
    'max_roll': {
        'long_name': 'Maximum Roll',
        'units': 'radians',
        'comment': 'Maximum of the roll measured during the sampling period.'
    },
    'min_heading': {
        'long_name': 'Minimum Heading',
        'units': 'radians',
        'comment': 'Minimum of the heading measured during the sampling period.'
    },
    'min_pitch': {
        'long_name': 'Minimum Pitch',
        'units': 'radians',
        'comment': 'Minimum of the pitch measured during the sampling period.'
    },
    'min_roll': {
        'long_name': 'Minimum Roll',
        'units': 'radians',
        'comment': 'Minimum of the roll measured during the sampling period.'
    },
    'u_corrected': {
        'long_name': 'Northerly Wind Speed',
        'units': 'm s-1',
        'comment': ('The relative U, V and W-Axis wind speeds, corrected for buoy motion, are used to produce wind '
                    'velocities relative to Earth. The northerly wind speeds, following the right-handed convention '
                    'of the instrument, are positive to the North.'),
        'data_product_identifier': 'WINDTUR-VLN_L1',
    },
    'v_corrected': {
        'long_name': 'Westerly Wind Speed',
        'units': 'm s-1',
        'comment': ('The relative U, V and W-Axis wind speeds, corrected for buoy motion, are used to produce wind '
                    'velocities relative to Earth. The westerly wind speeds, following the right-handed convention '
                    'of the instrument, are positive to the West.'),
        'data_product_identifier': 'WINDTUR-VLW_L1',
    },
    'w_corrected': {
        'long_name': 'Upward Wind Speed',
        'units': 'm s-1',
        'comment': ('The relative U, V and W-Axis wind speeds, corrected for buoy motion, are used to produce wind '
                    'velocities relative to Earth. The upward wind speeds, following the right-handed convention '
                    'of the instrument, are positive upwards.'),
        'data_product_identifier': 'WINDTUR-VLU_L1',
    },
    'std_u_corrected': {
        'long_name': 'Standard Deviation Along-Wind Compenent',
        'units': 'm s-1',
        'comment': ('The wind speeds relative to the earth are rotated into longitudinal (streamwise) winds and '
                    'linearly detrended to produce measures of the horizontal and vertical velocity fluctuations. '
                    'This measurement represents the standard deviation of the along-wind component of the '
                    'horizontal velocities.')
    },
    'std_v_corrected': {
        'long_name': 'Standard Deviation Cross-Wind Compenent',
        'units': 'm s-1',
        'comment': ('The wind speeds relative to the earth are rotated into longitudinal (streamwise) winds and '
                    'linearly detrended to produce measures of the horizontal and vertical velocity fluctuations. '
                    'This measurement represents the standard deviation of the cross-wind component of the '
                    'horizontal velocities.')
    },
    'std_w_corrected': {
        'long_name': 'Standard Deviation Vertical Compenent',
        'units': 'm s-1',
        'comment': ('The wind speeds relative to the earth are rotated into longitudinal (streamwise) winds and '
                    'linearly detrended to produce measures of the horizontal and vertical velocity fluctuations. '
                    'This measurement represents the standard deviation of the vertical velocities.')
    },
    'wind_speed': {
        'long_name': 'Wind Speed',
        'standard_name': 'wind_speed',
        'units': 'm s-1',
        'comment': 'Wind speed, corrected for the motion of the buoy, relative to the ground.'
    },
    'momentum_flux_uw': {
        'long_name': 'Along-Wind Momentum Flux',
        'units': 'm2 s-2',
        'comment': ('The momentum flux is the vertical transfer of horizontal momentum from the air to the ocean and '
                    'is called the wind stress. It is the transfer of energy from the wind physically pushing against '
                    'the water. The along-wind component generally carries most of the momentum flux, i.e., it is '
                    'responsible for most of the surface stress.'),
        'data_product_identifier': 'FLUXMOM-U_L2',
    },
    'momentum_flux_vw': {
        'long_name': 'Cross-Wind Momentum Flux',
        'units': 'm2 s-2',
        'comment': ('The momentum flux is the vertical transfer of horizontal momentum from the air to the ocean and '
                    'is called the wind stress. It is the transfer of energy from the wind physically pushing against '
                    'the water. The cross-wind component is generally smaller than the along-wind component, '
                    'signifying that the wind and stress vectors are closely aligned. However, this component can '
                    'become as large as or even larger than the along-wind component near the ocean surface in the '
                    'presence of waves. It can also be large in light-wind conditions where the wind and stress '
                    'vectors are poorly defined.'),
        'data_product_identifier': 'FLUXMOM-V_L2',
    },
    'buoyancy_flux': {
        'long_name': 'Buoyancy Flux',
        'units': 'm s-1 K',
        'comment': ('The buoyancy flux is computed using the direct covariance method. The method incorporates the '
                    'effect of both temperature and moisture on the buoyancy of an air parcel (i.e., its density '
                    'compared to the density of the surrounding air). For example, a moist parcel of air is less dense '
                    'than a dry parcel of air at the same temperature. Such a parcel would have positive buoyancy and '
                    'would want to rise thereby transferring moisture (and latent heat) upwards.'),
        'data_product_identifier': 'FLUXHOT_L2',
    },
    'wave_motion': {
        'long_name': 'Significant Wave Height',
        'standard_name': 'sea_surface_wave_significant_height',
        'units': 'm',
        'comment': 'Estimated significant wave height computed from the 3-D accelerometer data.'
    },
}
