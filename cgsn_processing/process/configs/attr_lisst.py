#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_lisst
@file cgsn_processing/process/configs/attr_lisst.py
@author Samuel Dahlberg
@brief Attributes for the LISST variables
"""

LISST = {
    'global': {
        'title': 'Particle Size Analyzer.',
        'summary': 'Laser-diffraction particle size analyzer, classifying particles into 36 size bins ranging from '
                   '1.00 μm to 500 μm.',
    },
    'clock_offset': {
        'long_name': 'Internal Clock Offset',
        'units': 's',
        'comment': 'Cross-compares the instrument clock to the GPS-based timestamp applied by the DCL upon receipt '
                   'of the data string. Allows for a determination of the internal clock offset and drift over the '
                   'course of a deployment.'
    },
    'lisst_volume_concentration': {
        'long_name': 'Volume Concentration For Size Class 1 Through 36',
        'units': 'μL',
        'comment': 'Volume concentration for particles analyzed by instrument, distributed through 36 size classes '
                   'ranging from 1.00 μm to 500 μm, with ranges increasing logarithmically. Each bin label represents '
                   'the lower limit of that bin size.'
    },
    'lower_particle_size': {
        'long_name': 'Lower Size Limit Of Each Bin',
        'units': 'µm',
        'comment': 'Contains the lower size limit of each bin. There is no size gap between bins, so the upper limit '
                   'of each bin is the next bin''s lower limit.'
    },
    'laser_transmission_sensor': {
        'long_name': 'Laser Transmission Sensor',
        'units': 'mW',
        'comment': 'The intensity of the laser reference sensor, measured in mW.'
    },
    'supply_voltage': {
        'long_name': 'Supply Voltage',
        'units': 'V',
        'comment': 'Voltage being supplied to the instrument.'
    },
    'laser_reference_sensor': {
        'long_name': 'Laser Reference Sensor',
        'units': 'mW',
        'comment': 'The intensity of the laser reference sensor, measured in mW. Used to correct scattering '
                   'calculations for variations in beam output intensity.'
    },
    'depth': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'The vertical distance below the surface.'
    },
    'temperature': {
        'long_name': 'Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'The in situ temperature of the sea water.'
    },
    'instrument_timestamp': {
        'long_name': 'Instrument Time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'calendar': 'gregorian',
        'comment': 'Date and time from the sensor''s internal clock.'
    },
    'mean_diameter': {
        'long_name': 'Mean Particle Diameter',
        'units': 'μm',
        'comment': 'The mean diameter of analyzed particles. Calculated from fully processed size distribution.'
    },
    'total_volume_concentration': {
        'long_name': 'Total Volume Concentration Of Particles',
        'units': 'ppm',
        'comment': 'The total volume concentration of particles in parts per million.'
    },
    'relative_humidity': {
        'long_name': 'Instrument Internal Humidity',
        'standard_name': 'relative_humidity',
        'units': 'percent',
        'comment': 'Percent relative humidity internal to the sensor. Increasing values can indicate a slow leak.'
    },
    'pressure': {
        'long_name': 'Raw Pressure',
        'standard_name': 'sea_water_pressure',
        # 'units': ''    # deliberately left blank, no units for this value
        'comment': 'Sea water pressure'
    },
    'ambient_light': {
        'long_name': 'Ambient Light',
        'units': 'count',
        'comment': 'Measure of light not produced by instrument laser. This is used to get accurate particle readings.'
    },
    'computed_optical_transmission': {
        'long_name': 'Computed Optical Transmission Over Path',
        'units': '1',
        'comment': 'Optical transmission is a measure of what proportion of light is transmitted through a turbid '
                   'medium. Light may be attenuated due to absorption or scattered out of the beam, and provides a '
                   'gross measure of total particles in seawater. Transmission values greater than 0.995 and less '
                   'than 0.1 indicated either very clear or very turbid waters and should be disregarded, while values '
                   'for very clear water (0.98-0.995) yield noisy data and should be used carefully.'
    },
    'beam_attenuation': {
        'long_name': 'Beam Attenuation (c)',
        'units': 'm-1',
        'comment': 'The Beam Attenuation Coefficient is the rate that the intensity of a beam of light will decrease '
                   'in response to the combined effects of absorption and scatter as a function of propagation '
                   'distance. The Attenuation Coefficient results from the spectral beam attenuation of the '
                   'combination of all seawater impurities including all particulate and dissolved matter of optical '
                   'importance at the measurement wavelength.'
    }
}