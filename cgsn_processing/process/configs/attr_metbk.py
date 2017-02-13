#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""

METBK = {
    'barometric_pressure': {
        'long_name': 'Barometric Pressure',
        'standard_name': 'barometric_pressure',
        'units': 'mbar',
        'coordinates': 'time longitude latitude depth_bpr',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '0',
        'valid_max': '2000'
    },
    'relative_humidity': {
        'long_name': 'Relative Humidity',
        'standard_name': 'relative_humidity',
        'units': '1',
        'coordinates': 'time longitude latitude depth_rh',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '0',
        'valid_max': '100'
    },
    'air_temperature': {
        'long_name': 'Air Temperature',
        'standard_name': 'air_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time longitude latitude depth_rh',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '-5',
        'valid_max': '30'
    },
    'longwave_irradiance': {
        'long_name': 'Longwave Irradiance',
        'standard_name': 'longwave_irradiance',
        'units': 'W m-2',
        'coordinates': 'time longitude latitude depth_irr',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '0',
        'valid_max': '1000'
    },
    'precipitation_level': {
        'long_name': 'Precipitation Level',
        'standard_name': 'precipitation_level',
        'units': 'mm',
        'coordinates': 'time longitude latitude depth_prc',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '0',
        'valid_max': '100'
    },
    'sea_surface_temperature': {
        'long_name': 'Sea Surface Temperature',
        'standard_name': 'sea_surface_temperature',
        'units': 'degree_Celcius',
        'coordinates': 'time longitude latitude depth_ct',
        'sensor_mount': 'mounted on mooring subsurface bridle',
        'valid_min': '0',
        'valid_max': '30'
    },
    'sea_surface_conductivity': {
        'long_name': 'Sea Surface Conductivity',
        'standard_name': 'sea_surface_conductivity',
        'units': 'S m-1',
        'coordinates': 'time longitude latitude depth_ct',
        'sensor_mount': 'mounted on mooring subsurface bridle',
        'valid_min': '0',
        'valid_max': '5'
    },
    'shortwave_irradiance': {
        'long_name': 'Shortwave Irradiance',
        'standard_name': 'shortwave_irradiance',
        'units': 'W m-2',
        'coordinates': 'time longitude latitude depth_irr',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '0',
        'valid_max': '1000'
    },
    'eastward_wind_velocity': {
        'long_name': 'Eastward Wind Velocity',
        'standard_name': 'eastward_wind_velocity',
        'units': 'm s-1',
        'coordinates': 'time longitude latitude depth_wnd',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '-100',
        'valid_max': '100'
    },
    'northward_wind_velocity': {
        'long_name': 'Northward Wind Velocity',
        'standard_name': 'northward_wind_velocity',
        'units': 'm s-1',
        'coordinates': 'time longitude latitude depth_wnd',
        'sensor_mount': 'mounted on mooring tower',
        'valid_min': '-100',
        'valid_max': '100'
    },
    'psu': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_salinity',
        'units': '1',
        'coordinates': 'time longitude latitude depth_ct',
        'sensor_mount': 'mounted on mooring subsurface bridle',
        'valid_min': '0',
        'valid_max': '40'
    },
    'rho': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'coordinates': 'time longitude latitude depth_ct',
        'sensor_mount': 'mounted on mooring subsurface bridle',
        'valid_min': '0',
        'valid_max': '30'
    },
    'depth_bpr': {
        'long_name': 'Sensor Height',
        'standard_name': 'height_of_sensor_above_water',
        'units': 'm',
        'coordinates': 'time',
        'valid_min': '-10000',
        'valid_max': '1000'
    },
    'depth_irr': {
        'long_name': 'Sensor Height',
        'standard_name': 'height_of_sensor_above_water',
        'units': 'm',
        'coordinates': 'time',
        'valid_min': '-10000',
        'valid_max': '1000'
    },
    'depth_prc': {
        'long_name': 'Sensor Height',
        'standard_name': 'height_of_sensor_above_water',
        'units': 'm',
        'coordinates': 'time',
        'valid_min': '-10000',
        'valid_max': '1000'
    },
    'depth_rh': {
        'long_name': 'Sensor Height',
        'standard_name': 'height_of_sensor_above_water',
        'units': 'm',
        'coordinates': 'time',
        'valid_min': '-10000',
        'valid_max': '1000'
    },
    'depth_wnd': {
        'long_name': 'Sensor Height',
        'standard_name': 'height_of_sensor_above_water',
        'units': 'm',
        'coordinates': 'time',
        'valid_min': '-10000',
        'valid_max': '1000'
    },
    'depth_ct': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'coordinates': 'time',
        'valid_min': '-10000',
        'valid_max': '1000'
    }
}
