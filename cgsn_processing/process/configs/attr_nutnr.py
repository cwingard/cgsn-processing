#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_nutnr
@file cgsn_processing/process/configs/attr_nutnr.py
@author Christopher Wingard
@brief Attributes for the ISUS nitrate sensor
"""
NUTNR = {
    'global': {
        'title': 'Partial Pressure of CO2 in Sea Water',
        'summary': 'Partial pressure of CO2 in sea water measured using the Sunburst Sensors SAMI2-pCO2 unit.',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes, (CGSN)',
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
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000',
    },
    'date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
        'units': '1'
    },
    'measurement_type': {
        'units': '1'
    },
    'serial_number': {
        'units': '1'
    },
    'date_string': {
        'units': '1'
    },
    'decimal_hours': {
        'units': 'hour'
    },
    'nitrate_concentration': {
        'units': 'umol L-1'
    },
    'auxiliary_fit_1st': {
        'units': '1'
    },
    'auxiliary_fit_2nd': {
        'units': '1'
    },
    'auxiliary_fit_3rd': {
        'units': '1'
    },
    'rms_error': {
        'units': '1'
    },
    'temperature_internal': {
        'units': 'degree_Celsius'
    },
    'temperature_spectrometer': {
        'units': 'degree_Celsius'
    },
    'temperature_lamp': {
        'units': 'degree_Celsius'
    },
    'lamp_on_time': {
        'units': 's'
    },
    'humidity': {
        'units': 'percent'
    },
    'voltage_lamp': {
        'units': 'V'
    },
    'voltage_analog': {
        'units': 'V'
    },
    'voltage_main': {
        'units': 'V'
    },
    'average_reference': {
        'units': 'counts'
    },
    'variance_reference': {
        'units': 'counts'
    },
    'seawater_dark': {
        'units': 'counts'
    },
    'spectral_average': {
        'units': 'counts'
    },
    'channel_measurements': {
        'units': 'counts'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_salinity',
        'units': '1',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'wavelengths': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
    },
    'corrected_nitrate': {
        'long_name': 'Corrected Nitrate Concentration',
        'standard_name': 'mole_concentration_of_nitrate_in_sea_water',
        'units': 'umol L-1'
    }
}
