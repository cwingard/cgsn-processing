#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""

METBK = {
    'global': {
        'title': 'Bulk Meteorological (METBK) Measurements',
        'summary': (
            'Measures surface meteorology and provides the data required to compute '
            'air-sea fluxes of heat, freshwater, and momentum.'
        ),
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'standard_name': 'deployment_id',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'barometric_pressure': {
        'long_name': 'Barometric Pressure',
        'standard_name': 'barometric_pressure',
        'units': 'mbar',
    },
    'relative_humidity': {
        'long_name': 'Relative Humidity',
        'standard_name': 'relative_humidity',
        'units': 'percent',
    },
    'air_temperature': {
        'long_name': 'Air Temperature',
        'standard_name': 'air_temperature',
        'units': 'degrees_Celsius',
    },
    'longwave_irradiance': {
        'long_name': 'Longwave Irradiance',
        'standard_name': 'longwave_irradiance',
        'units': 'W m-2',
    },
    'precipitation_level': {
        'long_name': 'Precipitation Level',
        'standard_name': 'precipitation_level',
        'units': 'mm',
    },
    'sea_surface_temperature': {
        'long_name': 'Sea Surface Temperature',
        'standard_name': 'sea_surface_temperature',
        'units': 'degrees_Celsius',
    },
    'sea_surface_conductivity': {
        'long_name': 'Sea Surface Conductivity',
        'standard_name': 'sea_surface_conductivity',
        'units': 'S m-1',
    },
    'shortwave_irradiance': {
        'long_name': 'Shortwave Irradiance',
        'standard_name': 'shortwave_irradiance',
        'units': 'W m-2',
    },
    'eastward_wind_velocity': {
        'long_name': 'Eastward Wind Velocity',
        'standard_name': 'eastward_wind_velocity',
        'units': 'm s-1',
    },
    'northward_wind_velocity': {
        'long_name': 'Northward Wind Velocity',
        'standard_name': 'northward_wind_velocity',
        'units': 'm s-1',
    },
    'psu': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
    },
    'rho': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
    }
}
