#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2a
@file cgsn_processing/process/configs/attr_pco2a.py
@author Christopher Wingard
@brief Attributes for the PCO2A variables
"""
import numpy as np

PCO2A = {
    'global': {
        'title': 'Partial Pressure of CO2 in the Air and Water',
        'summary': ('Measures partial pressure of CO2 in the air and surface seawater water, concurrently.'),
    },
    'co2_source': {
        'long_name': 'CO2 Measurement Source',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Indicates whether the measurement source is air (0) or water (1).',
        'flag_values': np.intc([0, 1]),
        'flag_meanings': 'air_measurement water_measurement'
    },
    'zero_a2d': {
        'long_name': 'Raw Zero Measurement',
        'units': 'count',
        'comment': ('The raw A2D zero measurement updated by the instrument approximately every 12 hours, used '
                    'in internal calculations to produce the c02_mole_fraction measurement.')
    },
    'current_a2d': {
        'long_name': 'Raw CO2 Measurement',
        'units': 'count',
        'comment': ('The raw air or water CO2 measurement collected in burst mode (9 measurements per sample source '
                    'every hour), used in internal calculations to produce the c02_mole_fraction measurement.')
    },
    'co2_mole_fraction': {
        'long_name': 'CO2 Mole Fraction',
        'units': 'ppm',
        'comment': ('The measured CO2 mole fraction in air or seawater internally computed onboard the sensor '
                    'from the raw measurements.')
    },
    'avg_irga_temperature': {
        'long_name': 'Average IRGA Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Average temperature measured at the infrared gas analyzer (IRGA) sensor.'
    },
    'humidity': {
        'long_name': 'Partial Pressure of Water Vapor',
        'units': 'mbar',
        'comment': ('The CO2-Pro measures the “wet” (i.e. partial pressure of water vapour included) xCO2 of '
                    'a gas stream that has equilibrated with surrounding water in mbar. In addition, the sensor '
                    'measures the total pressure of the gas stream, in millibars (mbar). This measurement represents '
                    'the water vapor pressure.')
    },
    'humidity_temperature': {
        'long_name': 'Humidity Sensor Temperature',
        'units': 'degrees_Celsius',
        'comment': ('Temperature of the "wet", or partial pressure of water vapour, sensor. Used internally by the '
                    'instrument to calculate the co2_mole_fraction.')
    },
    'gas_stream_pressure': {
        'long_name': 'Total Gas Stream Pressure',
        'units': 'mbar',
        'comment': ('The gas stream pressure is the pressure of the internal gas volume of the pCO2 Air-Sea '
                   'instrument. This data product is used to calculate Partial Pressure of CO2 in air and seawater.')
    },
    'irga_detector_temperature': {
        'long_name': 'IRGA Detector Temperature',
        'units': 'degrees_Celsius',
        'comment': ''
    },
    'irga_source_temperature': {
        'long_name': 'IRGA Source Temperature',
        'units': 'degrees_Celsius',
        'comment': ''
    },
    # ---- derived values ----
    'pCO2': {
        'long_name': 'Partial Pressure of CO2',
        'units': 'uatm',
        'comment': ('The partial pressure of CO2 in air or seawater refers to the pressure that would be exerted by '
                    'CO2 if all other gases were removed. The Partial pressure of CO2 (uatm) in air or seawater is '
                    'calculated from the CO2 mole fraction (ppm), the gas stream pressure (mbar) and standard '
                    'atmospheric pressure set to a default of 1013.25 mbar/atm. The CO2 Measurement Source variable '
                    'indicates whether the value is an air or water measurement.'),
        'ancillary_variables': 'co2_source co2_mole_fraction gas_stream_pressure'
    }
}
