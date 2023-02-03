#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_presf
@file cgsn_processing/process/configs/attr_presf.py
@author Joe Futrelle and Christopher Wingard
@brief Attributes for the PRESF variables
"""
PRESF = {
    'global': {
        'title': 'Seafloor Pressure',
        'summary': 'Seafloor pressure integrated over 60 minutes showing the tidal signature.',
    },
    # dataset attributes --> parsed data
    'sensor_time': {
        'long_name': 'Sensor Date and Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'comment': ('Internal sensor clock date and time stamp, recorded when the instrument begins the measurement. '
                    'It is expected that this value will drift from the true time by some amount over the course of '
                    'a deployment. Cross-comparisons to the DCL time stamp will be required to account for the offset '
                    'and drift.'),
        'calendar': 'gregorian'
    },
    'sensor_temperature': {
        'long_name': 'Pressure Sensor Temperature',
        'units': 'degrees_Celsius',
        'comment': ('Temperature of the pressure sensor, internal to the instrument. This reading is used to correct '
                    'the pressure sensor reading for the effects of temperature. It is expected to be slightly higher '
                    'than the in-situ temperature due to the warming effect of the electronics.')
    },
    'absolute_pressure': {
        'long_name': 'Absolute Pressure',
        'standard_name': 'sea_water_pressure_at_sea_floor',
        'units': 'psi',
        'comment': ('Sea water pressure at the sea floor is the pressure that exists at the sea floor. It includes the '
                    'pressure due to the overlying sea water, sea ice, air and any other medium that may be present. '
                    'The value represents a measurement of the pressure at the seafloor integrated over an hour to '
                    'track the tidal signature of the site.'),
        'data_product_identifier': 'SFLPRES-RTIME_L0'
    },
    'seawater_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature_at_sea_floor',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. The temperature at the sea '
                    'floor is that adjacent to the ocean bottom, which would be the deepest grid cell in an ocean '
                    'model and within the benthic boundary layer for measurements.')
    },
    # dataset attributes --> derived values
    'seafloor_pressure': {
        'long_name': 'Seafloor Pressure',
        'standard_name': 'sea_water_pressure_at_sea_floor',
        'units': 'dbar',
        'comment': ('Sea water pressure at the sea floor is the pressure that exists at the sea floor. It includes the '
                    'pressure due to the overlying sea water, sea ice, air and any other medium that may be present. '
                    'The value represents a measurement of the pressure at the seafloor integrated over an hour to '
                    'track the tidal signature of the site.'),
        'data_product_identifier': 'SFLPRES-RTIME_L1'
    }
}
