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
        'summary': ('The aquadopp records 3 minute ensemble averages every 15 minutes of the point velocity.'),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.7'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Name',
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
    'error_code': {
        'long_name': 'Error Code',
        'standard_name': 'status_flag',
        'units': '1',
        'comment': '',
        'flag_mask': np.array(2 ** np.array(range(0, 8)), dtype=object).astype(np.intc),
        'flag_meanings': ('compass_error measurement_data_error sensor_data_error tag_bit_error flash_error '
                          'undefined serial_ct_sensor_read_error undefined'),
        'ancillary_variables': 'headi'
                               'ng pitch roll pressure temperature velocity_east velocity_north velocity_vertical'
    },
    'battery_voltage': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'speed_of_sound': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'heading': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'pitch': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'roll': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'pressure': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'status_code': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'temperature': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'velocity_east': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'velocity_north': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'velocity_vertical': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'amplitude_beam1': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'amplitude_beam2': {
        'long_name': '',
        'units': '',
        'comment': ''
    },
    'amplitude_beam3': {
        'long_name': '',
        'units': '',
        'comment': ''
    }
}
