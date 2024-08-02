#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_co2pro
@file cgsn_processing/process/configs/attr_co2pro.py
@author Christopher Wingard
@brief Attributes for the Pro-Oceanus pCO2-Pro CV variables
"""
PCO2W = {
    # global attributes
    'global': {
        'title': 'Pro-Oceanus pCO2-Pro CV Data',
        'summary': ('In-water pCO2 data from the Pro-Oceanus pCO2-Pro CV instrument. The pCO2-Pro CV is a '
                    'compact, rugged, and low power system designed for autonomous deployment on moorings, '
                    'profiling floats, and other autonomous platforms. The pCO2-Pro CV measures the partial '
                    'pressure of CO2 in seawater using a non-dispersive infrared (NDIR) gas analyzer. The '
                    'pCO2-Pro CV is designed to be used in a variety of environments, including freshwater, '
                    'coastal, and open ocean.'),
    },
    # dataset attributes --> parsed data
    'sensor_time': {
        'long_name': 'Sensor Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'comment': ('Time of the sensor measurement in seconds since 1970-01-01 from the internal clock of the '
                    'instrument.')
    },
    'zero_a2d': {
        'long_name': 'Zero A2D Counts',
        'units': 'counts',
        'comment': ('Zero counts from the A2D module representing the zero point of the instrument. Updated every 12 '
                    'hours.')
    },
    'current_a2d': {
        'long_name': 'Current A2D Counts',
        'units': 'counts',
        'comment': 'Current counts from the A2D module representing the raw pCO2 measurement of the instrument.'
    },
    'measured_water_co2': {
        'long_name': 'Measured CO2',
        'units': 'ppm',
        'comment': ('Measured CO2 concentration reported by the instrument in ppm. This is the raw measurement that '
                    'needs to adjusted for the gas stream pressure in order to convert it to uatm.')
    },
    'avg_irga_temperature': {
        'long_name': 'Average IRGA Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Average temperature of the infrared gas analyzer.'
    },
    'humidity': {
        'long_name': 'Humidity',
        'standard_name': 'humidity',
        'units': 'mbar',
        'comment': 'Humidity measurement of the gas stream.'
    },
    'humidity_temperature': {
        'long_name': 'Humidity Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Temperature of the humidity sensor.'
    },
    'gas_stream_pressure': {
        'long_name': 'Gas Stream Pressure',
        'units': 'mbar',
        'comment': 'Pressure of the gas stream in the instrument. Used to calculate the pCO2.'
    },
    'supply_voltage': {
        'long_name': 'Supply Voltage',
        'units': 'V',
        'comment': 'Voltage supplied to the instrument by the DCL.'
    },
    # dataset attributes --> derived values
    'pCO2': {
        'long_name': 'Partial Pressure of CO2 in Seawater',
        'standard_name': 'partial_pressure_of_co2_in_sea_water',
        'units': 'uatm',
        'comment': 'Partial pressure of CO2 in the water. Calculated from the measured CO2 and gas stream pressure.',
        'ancillary_variables': 'gas_stream_pressure measured_co2'
    }
}
