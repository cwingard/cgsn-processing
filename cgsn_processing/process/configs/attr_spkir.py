#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_spkir
@file cgsn_processing/process/configs/attr_spkir.py
@author Joe Futrelle
@brief Attributes for the SPKIR variables
"""
import numpy as np

SPKIR = {
    'global': {
        'title': 'Downwelling Spectral Irradiance',
        'summary': ('Downwelling spectral irradiance measured at 7 discrete wavelengths with the Sea-Bird Electronics '
                    '(formerly Satlantic) OCR-507 Multispectral Radiometer.'),
    },
    # dataset attributes --> reported values
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': '',    # deliberately left blank, no units for this value,
        'comment': ('A string denoting the serial number of the instrument. This field combined with the text '
                    'SATDI7 uniquely identifies the instrument. This combination is known as the frame header or '
                    'synchronization string. This is normally a four-character field.'),
    },
    'timer': {
        'long_name': 'Timer',
        'units': 's',
        'comment': ('Indicates the number of seconds that have passed since the end of the initialization sequence. '
                    'This field is precise to two decimal places.')
    },
    'sample_delay': {
        'long_name': 'Sample Delay',
        'units': 'ms',
        'comment': ('The number of milliseconds to offset the Timer value to give an accurate indication of when '
                    'the frame''s sensors were sampled.')
    },
    'raw_irradiance_412': {
        'long_name': 'Raw Downwelling Irradiance 412 nm',
        'comment': ('Raw downwelling spectral irradiance at 412 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-412',
    },
    'raw_irradiance_444': {
        'long_name': 'Raw Downwelling Irradiance 444 nm',
        'comment': ('Raw downwelling spectral irradiance at 444 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-444',
    },
    'raw_irradiance_490': {
        'long_name': 'Raw Downwelling Irradiance 490 nm',
        'comment': ('Raw downwelling spectral irradiance at 490 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-490',
    },
    'raw_irradiance_510': {
        'long_name': 'Raw Downwelling Irradiance 510 nm',
        'comment': ('Raw downwelling spectral irradiance at 510 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-510',
    },
    'raw_irradiance_555': {
        'long_name': 'Raw Downwelling Irradiance 555 nm',
        'comment': ('Raw downwelling spectral irradiance at 555 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-555',
    },
    'raw_irradiance_620': {
        'long_name': 'Raw Downwelling Irradiance 620 nm',
        'comment': ('Raw downwelling spectral irradiance at 620 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-620',
    },
    'raw_irradiance_683': {
        'long_name': 'Raw Downwelling Irradiance 683 nm',
        'comment': ('Raw downwelling spectral irradiance at 683 nm measured by the Sea-Bird Electronics (formerly '
                    'Satlantic) OCR-507 sensor.'),
        'units': 'count',
        'data_product_identifier': 'SPECTIR_L0-683',
    },
    'input_voltage': {
        'long_name': 'Input Voltage',
        'units': 'V',
        'comment': 'Voltage supplied by the DCL to power the instrument.'
    },
    'analog_rail_voltage': {
        'long_name': 'Analog Rail Voltage',
        'units': 'V',
        'comment': 'Indicates the analog rail voltage for the operational components of the instrument.',
    },
    'internal_temperature': {
        'long_name': 'Internal Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Internal temperature of the instrument.',
    },
    'frame_counter': {
        'long_name': 'Frame Counter',
        'units': 'count',
        'comment': ('A data integrity sensor that maintains a count of each frame transmitted. The count increments '
                    'by one for each frame transmitted from 0 to 255, at which point it rolls back to zero again.'),
    },
    # dataset attributes --> derived values
    'downwelling_irradiance_412': {
        'long_name': 'Downwelling Spectral Irradiance at 412 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 412 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-412',
        'radiation_wavelength': 412,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_412'
    },
    'downwelling_irradiance_444': {
        'long_name': 'Downwelling Spectral Irradiance at 444 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 444 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-444',
        'radiation_wavelength': 444,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_444'
    },
    'downwelling_irradiance_490': {
        'long_name': 'Downwelling Spectral Irradiance at 490 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 490 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-490',
        'radiation_wavelength': 490,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_490'
    },
    'downwelling_irradiance_510': {
        'long_name': 'Downwelling Spectral Irradiance at 510 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 510 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-510',
        'radiation_wavelength': 510,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_510'
    },
    'downwelling_irradiance_555': {
        'long_name': 'Downwelling Spectral Irradiance at 555 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 555 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-555',
        'radiation_wavelength': 555,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_555'
    },
    'downwelling_irradiance_620': {
        'long_name': 'Downwelling Spectral Irradiance at 620 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 620 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-620',
        'radiation_wavelength': 620,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_620'
    },
    'downwelling_irradiance_683': {
        'long_name': 'Downwelling Spectral Irradiance at 683 nm',
        'standard_name': 'downwelling_photon_spherical_irradiance_per_unit_wavelength_in_sea_water',
        'units': 'uW cm-2 nm-1',
        'comment': ('Downwelling spectral irradiance measured at 683 nm by the Sea-Bird Electronics OCR-507 '
                    'Multispectral Radiometer. Spectral irradiance is a critical measurement for defining important '
                    'ocean processes, such as the radiant heating rate, and sets the energy available to drive a '
                    'range of biological and chemical processes in the ocean.'),
        'data_product_identifier': 'SPECTIR_L1-683',
        'radiation_wavelength': 683,
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_irradiance_683'
    }
}
