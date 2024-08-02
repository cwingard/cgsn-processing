#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_flort
@file cgsn_processing/process/configs/attr_flort.py
@author Christopher Wingard
@brief Attributes for the FLORT variables, and TURBD variables
"""
import numpy as np
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_common import CO_LOCATED

FLORT = {
    # global attributes
    'global': {
        'title': 'Chlorophyll, CDOM and Optical Backscatter Data',
        'summary': ('Measurements of chlorophyll and CDOM fluorescence and optical backscatter at 700 nm from the '
                    'Sea-Bird Electronics ECO-Triplet sensor. In some select cases, additional measurements of '
                    'the sea water turbidity (derived from the backscatter measurement) are also available.'),
    },
    'measurement_wavelength_beta': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_backscatter': {
        'long_name': 'Raw Optical Backscatter at 700 nm',
        'units': 'count',
        'comment': 'Raw optical backscatter measurements at 700 nm.',
        'data_product_identifier': 'FLUBSCT_L0'
    },
    'measurement_wavelength_chl': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_chlorophyll': {
        'long_name': 'Raw Chlorophyll Fluorescence',
        'units': 'count',
        'comment': 'Raw chlorophyll fluorescence (470 nm excitation/ 695 nm emission) measurements.',
        'data_product_identifier': 'CHLAFLO_L0'
    },
    'measurement_wavelength_fdom': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_fdom': {
        'long_name': 'Raw CDOM Fluorescence',
        'units': 'count',
        'comment': 'Raw CDOM fluorescence (370 nm excitation/ 460 nm emission) measurements.',
        'data_product_identifier': 'CDOMFLO_L0'
    },
    'raw_internal_temp': {
        'long_name': 'Raw Internal Thermistor Temperature',
        'units': 'count',
        'comment': ('This parameter is not defined in the instrument manual, and the exact use for it is uncertain.'
                    'Including here it on the off-chance that it may provide some benefit at a future data.')
    },
    # dataset attributes --> derived values
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll Concentration',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'ug L-1',
        'comment': ('Estimated chlorophyll concentration based upon a calibration curve derived from a fluorescent '
                    'proxy approximately equal to 25 ug/l of a Thalassiosira weissflogii phytoplankton culture. '
                    'This measurement is considered to be an estimate only of the true chlorophyll concentration.'),
        'data_product_identifier': 'CHLAFLO_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_chl'
    },
    'fluorometric_cdom': {
        'long_name': 'Fluorometric CDOM Concentration',
        'standard_name': ('concentration_of_colored_dissolved_organic_matter_in_sea_water_expressed_as_equivalent'
                          '_mass_fraction_of_quinine_sulfate_dihydrate'),
        'units': 'ppb',
        'comment': ('More commonly referred to as Chromophoric Dissolved Organic Matter (CDOM). CDOM plays an '
                    'important role in the carbon cycling and biogeochemistry of coastal waters. It occurs '
                    'naturally in aquatic environments primarily as a result of tannins released from decaying '
                    'plant and animal matter, and can enter coastal areas in river run-off containing organic '
                    'materials leached from soils.'),
        'data_product_identifier': 'CDOMFLO_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_cdom'
    },
    'beta_700': {
        'long_name': 'Volume Scattering Function at 700 nm',
        'standard_name': 'volume_scattering_function_of_radiative_flux_in_sea_water',
        'units': 'm-1 sr-1',
        'comment': ('Radiative flux is the sum of shortwave and longwave radiative fluxes. Scattering of '
                    'radiation is its deflection from its incident path without loss of energy. The volume '
                    'scattering function is the intensity (flux per unit solid angle) of scattered radiation per '
                    'unit length of scattering medium, normalised by the incident radiation flux.'),
        'data_product_identifier': 'FLUBSCT_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_beta'
    },
    'bback': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'units': 'm-1',
        'comment': ('Total (particulate + water) optical backscatter at 700 nm, derived from the Volume '
                    'Scattering Function and corrected for effects of temperature and salinity.'),
        'data_product_identifier': 'FLUBSCT_L2',
        '_FillValue': np.nan,
        'ancillary_variables': 'beta_700 ctd_temperature ctd_salinity'
    },
    # dataset attributes --> derived values if a turbidity calibration is available
    'turbidity': {
        'long_name': 'Sea Water Turbidity',
        'standard_name': 'sea_water_turbidity',
        'units': 'NTU',
        'comment': ('Turbidity is a dimensionless quantity which is expressed in NTU (Nephelometric Turbidity Units). '
                    'Turbidity expressed in NTU is the proportion of white light scattered back to a transceiver by '
                    'the particulate load in a body of water, represented on an arbitrary scale referenced against '
                    'measurements made in the laboratory on aqueous suspensions of formazine beads.'),
        'data_product_identifier': 'TURBWAT_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_beta'
    }
}

# add the co-located CTD attributes to the FLORT attributes
FLORT = dict_update(FLORT, CO_LOCATED)