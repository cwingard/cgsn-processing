#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_nutnr
@file cgsn_processing/process/configs/attr_nutnr.py
@author Christopher Wingard
@brief Attributes for the ISUS and SUNA nitrate sensors
"""
from cgsn_processing.process.common import FILL_INT, FILL_NAN

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
        'units': 'count'
    },
    'variance_reference': {
        'units': 'count'
    },
    'seawater_dark': {
        'units': 'count'
    },
    'spectral_average': {
        'units': 'count'
    },
    'channel_measurements': {
        'units': 'count'
    },
    'wavelengths': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
    },
    # dataset attributes --> co-located CTD data
    'ctd_pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Sea Water Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': FILL_NAN
    },
    'ctd_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. Measurements are from a '
                    'co-located CTD'),
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': FILL_NAN
    },
    'ctd_salinity': {
        'long_name': 'Sea Water Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRACSAL_L2',
        '_FillValue': FILL_NAN
    },
    # dataset attributes --> derived values
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
        'units': 'count'
    },
    'absorbance_250': {
        'units': 'count'
    },
    'bromide_trace': {
        'units': 'mg L-1'
    },
    'spectal_average': {
        'units': 'count'
    },
    'dark_value': {
        'units': 'count'
    },
    'integration_factor': {
    },
    'channel_measurements': {
        'units': 'count'
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
    'wavelengths': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
    },
    # dataset attributes --> co-located CTD data
    'ctd_pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Sea Water Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': FILL_NAN
    },
    'ctd_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. Measurements are from a '
                    'co-located CTD'),
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': FILL_NAN
    },
    'ctd_salinity': {
        'long_name': 'Sea Water Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRACSAL_L2',
        '_FillValue': FILL_NAN
    },
    # dataset attributes --> derived values
    'corrected_nitrate': {
        'long_name': 'Corrected Nitrate Concentration',
        'standard_name': 'mole_concentration_of_nitrate_in_sea_water',
        'units': 'umol L-1'
    }
}
