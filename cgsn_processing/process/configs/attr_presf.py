#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_presf
@file cgsn_processing/process/configs/attr_presf.py
@author Joe Futrelle and Christopher Wingard
@brief Attributes for the PRESF variables
       11212023 ppw added RBRQ3 variables
"""
import numpy as np

PRESF = {
    'global': {
        'title': 'Seafloor Pressure',
        'summary': ('Seafloor pressure recorded by the Sea-Bird SBE 26plus Seagauge Wave & Tide Recorder, integrated '
                    'over 60 minutes to record the tidal record at the mooring site. Wave data may be recorded, '
                    'depending on the site depth, but that data is not included in the telemetered record.'),
    },
    'sensor_time': {
        'long_name': 'Sensor Date and Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'comment': ('Internal SBE 26plus clock date and time stamp, recorded when the instrument begins the '
                    'measurement. It is expected that this value will drift from the true time by some amount over '
                    'the course of a deployment. Cross-comparisons to other systems will be required to account for '
                    'the offset and drift. Note, the DCL records the time the measurement is reported, so there '
                    'will be approximately a 1 hour offset between the sensor time and the record time.'),
        'calendar': 'gregorian'
    },
    'pressure_temp': {
        'long_name': 'Pressure Sensor Temperature',
        'units': 'degrees_Celsius',
        'comment': ('The temperature at the pressure sensor (inside the housing, but isolated from housing and the '
                    'electronics) used to calculate the absolute pressure.'),
        '_FillValue': np.nan
    },
    'absolute_pressure': {
        'long_name': 'Absolute Seafloor Pressure',
        'standard_name': 'sea_water_pressure_at_sea_floor',
        'units': 'dbar',
        'comment': ('Absolute seafloor pressure is a measurement of the force on the seafloor exerted by the weight '
                    'of the overlying seawater column plus the pressure due to the overlying sea water, sea ice, air '
                    'and any other medium that may be present.'),
        'data_product_identifier': 'SFLPRES-RTIME_L1',
        '_FillValue': np.nan
    },
    'seawater_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Sea water temperature is the in situ temperature of the sea water.',
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': np.nan
    }
}

RBRQ3 = {
    'global': {
        'title': 'Seafloor Pressure',
        'summary': 'Seafloor pressure ???',
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
    'sea_pressure_00': {
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
