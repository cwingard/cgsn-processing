#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_swnd
@file cgsn_processing/process/configs/attr_swnd.py
@author Christopher Wingard
@brief Attributes for the ASIMET Sonic Wind (SWND) module variables
"""
SWND = {
    # global attributes
    'global': {
        'title': 'ASIMET Sonic Wind (SWND) Module Data',
        'summary': ('Standalone wind data from the ASIMET Sonic Wind (SWND) module recorded separately from the '
                    'METBK logger in order to determine potential sources of error in the eastward and northward '
                    'wind components reported by the METBK.'),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
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
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'Derived from the GPS referenced clock used by DCL data logger'
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Instrument deployment depth',
        'positive': 'down',
        'axis': 'Z'
    },
    # variable attributes
    'eastward_wind_relative': {
        'long_name': 'Eastward Wind Velocity (Relative)',
        'comment': ('Relative eastward wind velocity component. Winds are relative to the instrument coordinate frame.'
                    'Positive values indicate wind moving eastward. The north axis of the instrument is aligned with '
                    'a separate compass module allowing the relative wind components to be aligned to magnetic north '
                    'in subsequent calculations.'),
        'units': 'm s-1'
    },
    'northward_wind_relative': {
        'long_name': 'Northward Wind Velocity (Relative)',
        'comment': ('Relative northward wind velocity component. Winds are relative to the instrument coordinate frame.'
                    'Positive values indicate wind moving northward. The north axis of the instrument is aligned with '
                    'a separate compass module allowing the relative wind components to be aligned to magnetic north '
                    'in subsequent calculations.'),
        'units': 'm s-1'
    },
    'sonic_temperature': {
        'long_name': 'Sonic Temperature',
        'standard_name': 'apparent_air_temperature',
        'comment': ('Air temperature calculated by the sonic anemometer. The temperature is not directly measured by '
                    'the sonic anemometer, but is derived from the speed of sound measurement and assumptions '
                    'regarding humidity.'),
        'units': 'degrees_Celsius'
    },
    'speed_of_sound': {
        'long_name': 'Speed of Sound',
        'standard_name': 'speed_of_sound_in_air',
        'comment': 'Speed of sound measured by the sonic anemometer.',
        'units': 'm s-1'
    },
    'heading': {
        'long_name': 'Compass Heading',
        'standard_name': 'heading',
        'comment': ('Compass heading of the instrument. The heading is used to align the relative wind components to '
                    'magnetic north. The heading is measured in degrees from magnetic north.'),
        'units': 'degrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'standard_name': 'platform_pitch_angle',
        'comment': ('Pitch angle of the instrument. Pitch is the rotation of the instrument around the east-west axis. '
                    'Positive values indicate the instrument is pitching up.'),
    },
    'roll': {
        'long_name': 'Roll',
        'standard_name': 'platform_roll_angle',
        'comment': ('Roll angle of the instrument. Roll is the rotation of the instrument around the north-south axis. '
                    'Positive values indicate the instrument is rolling to the right.'),
    },
    'wind_speed': {
        'long_name': 'Wind Speed',
        'standard_name': 'wind_speed',
        'comment': ('Wind speed calculated from the 5-second relative eastward and northward wind components and then '
                    'scalar averaged in the 1-minute data. Wind speed is the magnitude of the wind velocity vector.'),
        'units': 'm s-1',
        'ancillary_variables': 'eastward_wind_relative northward_wind_relative'
    },
    'eastward_wind_asimet': {
        'long_name': 'Eastward Wind Velocity (ASIMET)',
        'standard_name': 'eastward_wind',
        'comment': ('Eastward wind velocity component in Earth coordinates. Positive values indicate wind moving from '
                    'the west to the east. Calculated from the relative wind velocity components, the wind speed and '
                    'the instrument heading.'),
        'units': 'm s-1',
        'ancillary_variables': 'eastward_wind_relative northward_wind_relative wind_speed heading'
    },
    'northward_wind_asimet': {
        'long_name': 'Northward Wind Velocity (ASIMET)',
        'standard_name': 'northward_wind',
        'comment': ('Northward wind velocity component. Positive values indicate wind moving from the south to the '
                    'north. Calculated from the relative wind velocity components, which are relative to the '
                    'instrument, the wind speed and the instrument heading.'),
        'units': 'm s-1',
        'ancillary_variables': 'eastward_wind_relative northward_wind_relative wind_speed heading'
    },
    'wind_speed_max': {
        'long_name': 'Maximum Wind Speed',
        'standard_name': 'wind_speed_of_gust',
        'comment': 'Maximum wind speed recorded during the 1-minute sampling period.',
        'units': 'm s-1',
        'ancillary_variables': 'wind_speed'
    },
    'wind_direction': {
        'long_name': 'Wind Direction',
        'standard_name': 'wind_to_direction',
        'comment': ('Wind direction relative to true north. Calculated as the arctan of the vector averaged eastward '
                    'and northward wind components, and then converted to degrees from magnetic north. Wind direction '
                    'is calculated as the direction the wind is moving towards, following the oceanographic '
                    'convention.'),
        'units': 'degrees',
        'ancillary_variables': 'eastward_wind_asimet northward_wind_asimet'
    },
    'eastward_wind_ndbc': {
        'long_name': 'Eastward Wind Velocity (NDBC)',
        'standard_name': 'eastward_wind',
        'comment': ('Eastward wind velocity component in Earth coordinates. Positive values indicate wind moving from '
                    'the west to the east. Calculated from the scalar averaged wind speed and the wind direction '
                    'derived from the vector averaged eastward and northward wind components following the protocol '
                    'outlined by NDBC.'),
        'units': 'm s-1',
        'ancillary_variables': 'wind_speed wind_direction'
    },
    'northward_wind_ndbc': {
        'long_name': 'Northward Wind Velocity (NDBC)',
        'standard_name': 'northward_wind',
        'comment': ('Northward wind velocity component. Positive values indicate wind moving from the south to the '
                    'north. Calculated from the scalar averaged wind speed and the wind direction derived from the '
                    'vector averaged eastward and northward wind components following the protocol outlined by NDBC.'),
        'units': 'm s-1',
        'ancillary_variables': 'wind_speed wind_direction'
    }
}
