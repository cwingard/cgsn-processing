#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_spkir
@file cgsn_processing/process/configs/attr_spkir.py
@author Joe Futrelle
@brief Attributes for the SPKIR variables
"""

SPKIR = {
    'global': {
        'title': 'Downwelling Spectral Irradiance at 7 meters',
        'summary': 'Downwelling spectral irradiance measured over 7 wavelengths at 7 meter depth',
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
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'standard_name': 'dcl_date_time_string',
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
    'serial_number': {
        'units': '1'
    },
    'timer': {
        'units': 's'
    },
    'sample_delay': {
        'units': 'ms'
    },
    'raw_channels': {
        'units': 'counts'
    },
    'input_voltage': {
        'units': 'V'
    },
    'analog_rail_voltage': {
        'units': 'V'
    },
    'frame_counter': {
        'units': '1'
    },
    'internal_temperature': {
        'units': 'degrees_Celsius'
    },
    'irradiance': {
        'long_name': 'Downwelling Spectral Irradiance',
        'standard_name': 'downwelling_spectral_spherical_irradiance_in_sea_water',
        'units': 'uW cm-2 nm-1'
    },
    'wavelengths': {
        'long_name': 'Radiation Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    }
}
