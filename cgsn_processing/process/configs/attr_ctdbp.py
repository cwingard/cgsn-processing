#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ctdbp
@file cgsn_processing/process/configs/attr_ctdbp.py
@author Christopher Wingard
@brief Attributes for the CTDBP variables
"""
CTDBP = {
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
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'ctd_date_time_string': {
        'long_name': 'CTD Date and Time Stamp',
        'standard_name': 'ctd_date_time_string',
        'units': '1',
        'coordinates': 'time z longitude latitude',
        'grid_mapping': 'crs',
        'platform': 'platform',
        'ancillary_variables': 'platform',
        'coverage_content_type': 'physicalMeasurement'
    },
    'temperature': {
        'units': 'degrees_Celsius'
    },
    'conductivity': {
        'units': 'S/m'
    },
    'pressure': {
        'units': 'dbar'
    },
    'oxygen_concentration': {
        'units': 'umol/L'
    },
    'raw_backscatter': {
        'units': 'counts'
    },
    'raw_chlorophyll': {
        'units': 'counts'
    },
    'raw_cdom': {
        'units': 'counts'
    },
    'psu': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_salinity',
        'units': '1',
        'valid_min': '0',
        'valid_max': '40'
    },
    'rho': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'valid_min': '0',
        'valid_max': '35'
    }
}
