#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_hydgn
@file cgsn_processing/process/configs/attr_hydgn.py
@author Christopher Wingard
@brief Attributes for the hydrogen gas variables
"""
HYDGN = {
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
    'hydrogen_concentration': {
        'long_name': 'Hydrogen LEL Concentration',
        'standard_name': 'hydrogen_concentration',
        'units': '%',
    }
}
