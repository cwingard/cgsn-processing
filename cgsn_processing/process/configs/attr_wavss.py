#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_wavss
@file cgsn_processing/process/configs/attr_wavss.py
@author Christopher Wingard
@brief Attributes for the AXYS Technologies wave monitoring sensor
"""
WAVSS = {
    'global': {
        'title': 'Summary Wave Statistics',
        'summary': 'Records the hourly summarized wave statistics from the Axys Technologies, TriAxys Wave Sensor.',
    },
    'date_string': {
        'long_name': 'Date of Measurement',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Date of Measurement (UTC), recorded as a string by the instrument''s internal clock.'
    },
    'time_string': {
        'long_name': 'Time of Measurement',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Time of measurement (UTC), recorded as a string by the instrument''s internal clock.'
    },
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Instrument serial number.',
    },
    'num_zero_crossings': {
        'long_name': 'Number of Zero Crossings',
        'units': 'count',
        'comment': ('Number of zero crossings in the underlying displacement data, used primarily for verification '
                    'and QC.'),
        'data_product_identifier': 'WAVSTAT-N0_L0'
    },
    'average_wave_height': {
        'long_name': 'Average Wave Height',
        'standard_name': 'sea_surface_wave_mean_height',
        'units': 'm',
        'comment': 'Average wave height (Havg) from all of the zero crossings of the observed waves.',
        'data_product_identifier': 'WAVSTAT-HAVG_L0'
    },
    'mean_spectral_period': {
        'long_name': 'Mean Spectral Period',
        'units': 'seconds',
        'comment': 'The mean spectral period (Tz) is the mean of all wave periods in the observed time series.'
    },
    'maximum_wave_height': {
        'long_name': 'Maximum Wave Height',
        'standard_name': 'sea_surface_wave_maximum_height',
        'units': 'm',
        'comment': ('Wave height is defined as the vertical distance from a wave trough to the following wave crest. '
                    'The maximum wave height (Hmax) is the greatest trough to crest distance measured during the '
                    'observation period.'),
        'data_product_identifier': 'WAVSTAT-HMAX_L0'
    },
    'significant_wave_height': {
        'long_name': 'Significant Wave Height',
        'standard_name': 'sea_surface_wave_significant_height',
        'units': 'm',
        'comment': ('Significant wave height (Hs) is the average wave height from the highest third of the waves '
                    'observed.'),
        'data_product_identifier': 'WAVSTAT-HSIG_L0'
    },
    'significant_wave_period': {
        'long_name': 'Significant Wave Period',
        'standard_name': 'sea_surface_wave_significant_period',
        'units': 'seconds',
        'comment': ('Significant wave period (Ts) is the average wave period from the highest third of the waves '
                    'observed.'),
        'data_product_identifier': 'WAVSTAT-TSIG_L0'
    },
    'average_tenth_height': {
        'long_name': 'Mean Wave Height, Highest Tenth',
        'standard_name': 'sea_surface_wave_mean_height_of_highest_tenth',
        'units': 'm',
        'comment': ('H10, or the height of the highest tenth is defined as the mean of the highest ten per cent of '
                    'trough to crest distances measured during the observation period.'),
        'data_product_identifier': 'WAVSTAT-H10_L0'
    },
    'average_tenth_period': {
        'long_name': 'Mean Wave Period, Highest Tenth',
        'standard_name': 'sea_surface_wave_mean_period_of_highest_tenth',
        'units': 'seconds',
        'comment': 'The mean period of the highest one-tenth (T10) of waves during the observation duration.',
        'data_product_identifier': 'WAVSTAT-T10_L0'
    },
    'average_wave_period': {
        'long_name': 'Average Wave Period',
        'standard_name': 'sea_surface_wave_mean_period',
        'units': 'seconds',
        'comment': 'Average wave period (Tavg) from all of the zero crossings of the observed waves.',
        'data_product_identifier': 'WAVSTAT-TAVG_L0'
    },
    'peak_period': {
        'long_name': 'Peak Wave Period',
        'standard_name': 'sea_surface_wave_period_at_variance_spectral_density_maximum',
        'units': 's',
        'comment': ('The sea_surface_wave_period_at_variance_spectral_density_maximum, sometimes called peak wave '
                    'period (Tp), is the period of the most energetic waves in the total wave spectrum at a specific '
                    'location.'),
        'data_product_identifier': 'WAVSTAT-TP_L0'
    },
    'peak_period_read': {
        'long_name': 'Peak Wave Period from READ Method',
        'units': 's',
        'comment': ('Peak wave period as computed by the READ method (Tp5). This measure has less statistical '
                    'variability than the peak wave period (Tp) because it is based on spectral moments. The Tp5 '
                    'is determined from calculating the average frequency computed with the weighting function '
                    'S(f)**5 over the defined upper and lower frequency range.'),
        'data_product_identifier': 'WAVSTAT-TP5_L0'
    },
    'spectral_wave_height': {
        'long_name': 'Significant Wave Height from Spectral Moments',
        'units': 'm',
        'comment': 'Significant wave height estimated by an alternate method based on spectral moments (Hmo).',
        'data_product_identifier': 'WAVSTAT-HMO_L0'
    },
    'mean_wave_direction': {
        'long_name': 'Mean Wave Direction',
        'standard_name': 'sea_surface_wave_from_direction',
        'units': 'degrees',
        'comment': ('The direction from which the waves at the dominant period are coming. The direction of the '
                    'wave field is relative to true North, though it has not been corrected for magnetic declination.'),
        'data_product_identifier': 'WAVSTAT-D_L0'
    },
    'mean_directional_spread': {
        'long_name': 'Mean Wave Directional Spread',
        'standard_name': 'sea_surface_wave_directional_spread',
        'units': 'degrees',
        'comment': 'Mean directional spread of the observed wave field.'
    }
}
