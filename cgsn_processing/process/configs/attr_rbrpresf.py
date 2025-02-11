#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_rbrpresf
@file cgsn_processing/process/configs/attr_rnrpresf.py
@author Paul Whelan
@brief Attributes for the RBR PRESF variables
"""

RBRQ3 = {
    'global': {
        'title': 'Seafloor Pressure',
        'summary': 'Seafloor pressure ???',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'standard_name': 'deployment_id',
        'units': '1',
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
        'comment': ('Derived from a data logger GPS referenced clock, or the internal instrument clock '
                    'if this is an IMM hosted instrument. For instruments attached to a DCL, the instrument''s '
                    'internal clock can be cross-compared to the GPS clock to determine the internal clock''s '
                    'offset and drift.')
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': 'Mooring deployment location, surveyed after deployment to determine center of watch circle.'
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': 'Mooring deployment location, surveyed after deployment to determine center of watch circle.'
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Instrument deployment depth',
        'positive': 'down',
        'axis': 'Z'
    },
    'depth_00': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000',
    },
    'temperature_00': {
        'long_name': 'Temperature of ???',
        'units': 'degrees_Celsius',
    },
    'pressure_00': {
        'long_name': 'Pressure of ???',
        'units': 'degrees_Celsius',
    },
    'temperature_01': {
        'long_name': 'Temperature of ???',
        'units': 'degrees_Celsius',
    },
    'seapressure_00': {
        'long_name': 'Sea floor pressure',
        'standard_name': 'seafloor_pressure',
        'units': 'dbar',
    },
    'period_00': {
        'long_name': 'Period of ???',
        'units': 'seconds???',
    },
    'period_01': {
        'long_name': 'Period of ???',
        'units': 'seconds???',
    }
}
