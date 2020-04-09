#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_nutnr
@file cgsn_processing/process/configs/attr_nutnr.py
@author Christopher Wingard
@brief Attributes for the ISUS and SUNA nitrate sensors
"""
ISUS = {
    'global': {
        'title': 'Nitrate Concentration',
        'summary': 'Nitrate Concentration in sea water measured using the Satlantic ISUS unit.',
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
        'standard_name': 'deployment_id'
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
        'standard_name': 'dcl_date_time_string'
    },
    'measurement_type': {
    },
    'serial_number': {
    },
    'date_string': {
    },
    'decimal_hours': {
        'units': 'hour'
    },
    'nitrate_concentration': {
        'units': 'umol L-1'
    },
    'auxiliary_fit_1st': {
    },
    'auxiliary_fit_2nd': {
    },
    'auxiliary_fit_3rd': {
    },
    'rms_error': {
    },
    'temperature_internal': {
        'units': 'degrees_Celsius'
    },
    'temperature_spectrometer': {
        'units': 'degrees_Celsius'
    },
    'temperature_lamp': {
        'units': 'degrees_Celsius'
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
        'units': 'degrees_Celsius',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
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

SUNA = {
    'global': {
        'title': 'Nitrate Concentration',
        'summary': 'Nitrate Concentration in sea water measured using the Satlantic ISUS unit.',
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
        'standard_name': 'deployment_id'
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
        'standard_name': 'dcl_date_time_string'
    },
    'measurement_type': {
    },
    'year': {
        'units': 'year'
    },
    'day_of_year': {
        'units': 'day'
    },
    'decimal_hours': {
        'units': 'hour'
    },
    'nitrate_concentration': {
        'units': 'umol L-1'
    },
    'nitrogen_in_nitrate': {
        'units': 'mg L-1'
    },
    'absorbance_254': {
        'units': 'counts'
    },
    'absorbance_250': {
        'units': 'counts'
    },
    'bromide_trace': {
        'units': 'mg L-1'
    },
    'spectal_average': {
        'units': 'counts'
    },
    'dark_value': {
        'units': 'counts'
    },
    'integration_factor': {
    },
    'channel_measurements': {
        'units': 'counts'
    },
    'temperature_internal': {
        'units': 'degrees_Celsius'
    },
    'temperature_spectrometer': {
        'units': 'degrees_Celsius'
    },
    'temperature_lamp': {
        'units': 'degrees_Celsius'
    },
    'lamp_on_time': {
        'units': 's'
    },
    'humidity': {
        'units': 'percent'
    },
    'voltage_main': {
        'units': 'V'
    },
    'voltage_lamp': {
        'units': 'V'
    },
    'voltage_internal': {
        'units': 'V'
    },
    'main_current': {
        'units': 'mA'
    },
    'fit_auxiliary_1': {
    },
    'fit_auxiliary_2': {
    },
    'fit_base_1': {
    },
    'fit_base_2': {
    },
    'fit_rmse': {
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
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
