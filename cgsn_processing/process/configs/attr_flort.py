#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_flort
@file cgsn_processing/process/configs/attr_flort.py
@author Christopher Wingard
@brief Attributes for the FLORT variables
"""
import numpy as np

FLORT = {
    # global attributes
    'global': {
        'title': 'Chlorophyll, CDOM and Optical Backscatter Data',
        'summary': ('Measurements of chlorophyll and CDOM fluorescence and optical backscatter at 700 nm from the '
                    'Sea-Bird Electronics ECO-Triplet sensor.')
    },
    'measurement_wavelength_beta': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_beta': {
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
    'raw_signal_chl': {
        'long_name': 'Raw Chlorophyll Fluorescence',
        'units': 'count',
        'comment': 'Raw chlorophyll fluorescence (470 nm excitation/ 695 nm emission) measurements.',
        'data_product_identifier': 'CHLAFLO_L0'
    },
    'measurement_wavelength_cdom': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_cdom': {
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
        '_FillValue': np.nan
    },
    'ctd_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. Measurements are from a '
                    'co-located CTD'),
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': np.nan
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
        '_FillValue': np.nan
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
    }
}
