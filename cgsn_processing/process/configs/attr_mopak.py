#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mopak
@file cgsn_processing/process/configs/attr_mopak.py
@author Christopher Wingard
@brief Attributes for the hydrogen gas variables
"""

MOPAK = {
    'global': {
        'title': 'Mooring 3D Accelerometer Data collected in bursts at 10 Hz',
        'summary': 'Records the motion and orientation of the mooring via a 3D accelerometer.'
    },
    'acceleration_x': {
        'long_name': 'X-axis Acceleration Vector',
        'units': 'gravity',
        'comment': ('This is a vector quantifying the direction and magnitude of the acceleration that the '
                    'mooring is exposed to. This quantity is fully temperature compensated and scaled into '
                    'physical units of g (1 g = 9.80665 m/sec^2). It is expressed in terms of the MOPAK’s '
                    'local coordinate system (in this case the X-axis).')
    },
    'acceleration_y': {
        'long_name': 'Y-axis Acceleration Vector',
        'units': 'gravity',
        'comment': ('This is a vector quantifying the direction and magnitude of the acceleration that the '
                    'mooring is exposed to. This quantity is fully temperature compensated and scaled into '
                    'physical units of g (1 g = 9.80665 m/sec^2). It is expressed in terms of the MOPAK’s '
                    'local coordinate system (in this case the Y-axis).')
    },
    'acceleration_z': {
        'long_name': 'Z-axis Acceleration Vector',
        'units': 'gravity',
        'comment': ('This is a vector quantifying the direction and magnitude of the acceleration that the '
                    'mooring is exposed to. This quantity is fully temperature compensated and scaled into '
                    'physical units of g (1 g = 9.80665 m/sec^2). It is expressed in terms of the MOPAK’s '
                    'local coordinate system (in this case the Z-axis).')
    },
    'angular_rate_x': {
        'long_name': 'X-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the rate of rotation of the mooring. This quantity is '
                    'is fully temperature compensated and scaled into units of radians/second. It is '
                    'expressed in terms of the MOPAK’s local coordinate system (in this case the X-axis) '
                    'in units of radians/second.')
    },
    'angular_rate_y': {
        'long_name': 'Y-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the rate of rotation of the mooring. This quantity is '
                    'is fully temperature compensated and scaled into units of radians/second. It is '
                    'expressed in terms of the MOPAK’s local coordinate system (in this case the Y-axis) '
                    'in units of radians/second.')
    },
    'angular_rate_z': {
        'long_name': 'Z-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the rate of rotation of the mooring. This quantity is '
                    'is fully temperature compensated and scaled into units of radians/second. It is '
                    'expressed in terms of the MOPAK’s local coordinate system (in this case the Z-axis) '
                    'in units of radians/second.')
    },
    'magnetometer_x': {
        'long_name': 'X-axis Magnetometer',
        'units': 'gauss',
        'comment': ('This is a vector which gives the instantaneous magnetometer direction and magnitude. It '
                    'is fully temperature compensated and is expressed in terms of the MOPAK’s local '
                    'coordinate system (in this case the X-axis) in units of Gauss.')
    },
    'magnetometer_y': {
        'long_name': 'Y-axis Magnetometer',
        'units': 'gauss',
        'comment': ('This is a vector which gives the instantaneous magnetometer direction and magnitude. It '
                    'is fully temperature compensated and is expressed in terms of the MOPAK’s local '
                    'coordinate system (in this case the Y-axis) in units of Gauss.')
    },
    'magnetometer_z': {
        'long_name': 'Z-axis Magnetometer',
        'units': 'gauss',
        'comment': ('This is a vector which gives the instantaneous magnetometer direction and magnitude. It '
                    'is fully temperature compensated and is expressed in terms of the MOPAK’s local '
                    'coordinate system (in this case the Z-axis) in units of Gauss.')
    },
    'timer': {
        'long_name': 'Timer',
        'units': 's',
        'comment': ('The time, in seconds, since the system started up. This is a relative measure of time '
                    'that is used, along with the file start time, to calculate the time in seconds since '
                    '1970-01-01.')
    }
}
