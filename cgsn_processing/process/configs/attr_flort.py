#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_flort
@file cgsn_processing/process/configs/attr_flort.py
@author Christopher Wingard
@brief Attributes for the FLORT variables, and TURBD variables
"""
import numpy as np

FLORT = {
    'global': {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'units': '1'
    },
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Sensor depth below sea surface',
        'positive': 'down',
        'axis': 'Z'
    },
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'units': '1',
    },
    'measurement_wavelength_beta': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_beta': {
        'units': 'counts'
    },
    'measurement_wavelength_chl': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_chl': {
        'units': 'counts'
    },
    'measurement_wavelength_cdom': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_cdom': {
        'units': 'counts'
    },
    'raw_internal_temp': {
        'units': 'counts'
    },
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'mg L-1'
    },
    'fluorometric_cdom': {
        'long_name': 'Fluorometric CDOM',
        'units': 'ppm'
    },
    'beta_700': {
        'long_name': 'Volume Scattering Function at 700 nm',
        'standard_name': 'volume_scattering_function_of_radiative_flux_in_sea_water',
        'units': 'm-1 sr-1'
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
    'bback': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'units': 'm-1'
    }
}

TURBD = {
    'global': {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'units': '1'
    },
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Sensor depth below sea surface',
        'positive': 'down',
        'axis': 'Z'
    },
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'units': '1',
    },
    'measurement_wavelength_beta': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_beta': {
        'units': 'counts'
    },
    'turbidity': {
        'long_name': 'Raw turbidity value',
        'standard_name': 'sea_water_turbidity',
        'units': 'NTU',
        'comment': ('Turbidity is a dimensionless quantity which is expressed in NTU '
                    '(Nephelometric Turbidity Units). Turbidity expressed in NTU is the proportion '
                    'of white light scattered back to a transceiver by the particulate load in a '
                    'body of water, represented on an arbitrary scale referenced against measurements '
                    'made in the laboratory on aqueous suspensions of formazine beads.'),
        'data_product_identifier': 'TURBWAT_L1',
        '_FillValue': np.nan
        }
}
