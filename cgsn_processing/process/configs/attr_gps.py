#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_gps
@file cgsn_processing/process/configs/attr_gps.py
@author Christopher Wingard
@brief Attributes for the GPS variables
"""
import numpy as np

GPS = {
    'global': {
        'title': 'Mooring GPS Data',
        'summary': 'Precise latitude and longitude data recorded from the GPS sensor mounted on the buoy.'
    },
    # dataset attributes --> parsed data
    'precise_lat': {
        'long_name': 'Precise Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'comment': ('Mooring location measured by a GPS sensor located atop the mooring masthead. Provides a '
                    'precise measurement of the mooring location, compared to the nominal location determined '
                    'after mooring deployment from an anchor survey.')
    },
    'precise_lon': {
        'long_name': 'Precise Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'comment': ('Mooring location measured by a GPS sensor located atop the mooring masthead. Provides a '
                    'precise measurement of the mooring location, compared to the nominal location determined '
                    'after mooring deployment from an anchor survey.')
    },
    'speed_over_ground': {
        'long_name': 'Speed Over Ground',
        'units': 'knot',
        'comment': 'Speed of the mooring over water.'
    },
    'course_over_ground': {
        'long_name': 'Course Over Ground',
        'units': 'degrees',
        'comment': 'Course of the mooring over water.'
    },
    'fix_quality': {
        'long_name': 'Fix Quality',
        'standard_name': 'status_flag',
        'units': '1',
        'comment': 'Indication of the GPS fix quality.',
        'flag_values': np.intc([0, 1, 2, 3, 4, 5, 6, 7, 8]),
        'flag_meanings': ('fix_not_available normal_gps_fix differential_gps_fix pps_fix real_time_kinematic '
                          'float_real_time_kinematic estimated_dead_reckoning manual_input_mode simulation_mode'),
        'ancillary_variables': 'precise_lat precise_lon'
    },
    'number_satellites': {
        'long_name': 'Number of Satellites',
        'units': 'count',
        'comment': 'Number of satellites in the field of view used in the GPS fix.'
    },
    'horiz_dilution_precision': {
        'long_name': 'Horizontal Dilution of Precision',
        # 'units': '',    deliberately left blank, no units for this value,
        'comment': ('Describes the quality of the horizontal fix (latitude and longitude) based on the number of '
                    'good views to satellites low on the horizon. Smaller HDOP values are indicative of '
                    'more precise location measurements. Values less than or equal to 1 are considered ideal, 1-2 are '
                    'excellent, 2-5 are good, 5-10 are moderate, 10-20 are fair, and greater than 20 are poor.')
    },
    'altitude': {
        'long_name': 'Altitude',
        'units': 'm',
        'comment': 'Height of the sensor above the WGS-84 geoid.'
    }
}
