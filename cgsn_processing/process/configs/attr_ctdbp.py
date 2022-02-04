#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ctdbp
@file cgsn_processing/process/configs/attr_ctdbp.py
@author Christopher Wingard
@brief Attributes for the CTDBP variables
"""
import numpy as np
from cgsn_processing.process.common import FILL_INT

CTDBP = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Conductivity, Temperature and Depth (CTD) Data',
        'summary': 'Moored CTD time series data sets.'
    },
    # attributes for all instances of the CTDBP, regardless of system used to log data or instrument(s) attached.
    # --> reported values
    'sensor_time': {
        'long_name': 'CTD Date and Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'comment': ('Internal CTD clock date and time stamp, recorded when the instrument begins the measurement. It '
                    'is expected that this value will drift from the true time by some amount over the course of '
                    'a deployment. Cross-comparisons to other systems will be required to account for the offset '
                    'and drift.'),
        'calendar': 'gregorian'
    },
    'conductivity': {
        'long_name': 'Sea Water Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1',
        'comment': ('Sea water conductivity refers to the ability of seawater to conduct electricity. The presence '
                    'of ions, such as salt, increases the electrical conducting ability of seawater. As such, '
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of '
                    'seawater.'),
        'data_product_identifier': 'CONDWAT_L1',
        '_FillValue': np.nan
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Sea water temperature is the in situ temperature of the sea water.',
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': np.nan
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': np.nan
    },
    # --> derived values
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable.'),
        'data_product_identifier': 'PRACSAL_L2',
        'ancillary_variables': 'conductivity, temperature, pressure',
        '_FillValue': np.nan
    },
    'density': {
        'long_name': 'In-Situ Sea Water Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'comment': ('Sea water Density is the in situ density and is defined as mass per unit volume. It is '
                    'calculated from the conductivity, temperature and depth of a sea water sample.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, salinity, temperature, pressure',
        '_FillValue': np.nan
    },

    # attributes associated with the status message output from a CTDBP connected to an inductive modem (IMM)
    'status_time': {
        'long_name': 'Status Update Time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'comment': 'Date and time the CTD status was queried.',
        'calendar': 'gregorian',
        '_FillValue': np.nan
    },
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': ''    # deliberately left blank, no units for this value
        'comment': 'Instrument serial number.',
        '_FillValue': FILL_INT,
    },
    'main_battery_voltage': {
        'long_name': 'Main Battery Voltage',
        'units': 'V',
        'comment': 'Voltage of either the internal battery pack or externally supplied power, whichever is greater.',
        '_FillValue': np.nan
    },
    'lithium_battery_voltage': {
        'long_name': 'Lithium Battery Voltage',
        'units': 'V',
        'comment': 'Voltage of the internal battery cell, used to maintain the clock and firmware settings.',
        '_FillValue': np.nan
    },
    'samples_recorded': {
        'long_name': 'Number of Samples Recorded',
        'units': 'counts',
        'comment': 'Number of samples recorded during the deployment',
        '_FillValue': FILL_INT
    },
    'sample_slots_free': {
        'long_name': 'Number of Free Sample Slots Remaining',
        'units': 'counts',
        'comment': 'Number of free samples available for recording, representing the memory available in the unit',
        '_FillValue': FILL_INT
    },
    'main_current': {
        'long_name': 'Main Current',
        'units': 'mA',
        'comment': 'Total current draw on the system, encompassing all functions and external sensors.',
        '_FillValue': np.nan
    },
    'pump_current': {
        'long_name': 'Pump Current',
        'units': 'mA',
        'comment': 'Current draw from the system by the external pump.',
        '_FillValue': np.nan
    },
    'oxy_current': {
        'long_name': 'Oxygen Sensor Current',
        'units': 'mA',
        'comment': 'Current draw from the system by the external optode oxygen (DOSTA) sensor.',
        '_FillValue': np.nan
    },
    'flr_current': {
        'long_name': 'Fluorometer Sensor Current',
        'units': 'mA',
        'comment': 'Current draw from the system by the external two-channel fluorometer (FLORD) sensor.',
        '_FillValue': np.nan
    },

    # Values recorded by the different CTDBP configurations
    # --> equipped with an optode (DOSTA)
    'raw_calibrated_phase': {
        'long_name': 'Raw Calibrated Phase Difference',
        'units': 'V',
        'comment': ('The optode measures oxygen by exciting a special platinum porphyrin complex embedded in a '
                    'gas permeable foil with modulated blue light. The Optode measures the phase shift of a '
                    'returned red light. To convert the raw calibrated phase difference reported in V to degrees, '
                    'This value is recorded by the CTD as an analog voltage signal.'),
        'data_product_identifier': 'DOCONCS-VLT_L0',
        '_FillValue': np.nan
    },
    'calibrated_phase': {
        'long_name': 'Optode Calibrated Phase',
        'units': 'degrees',
        'comment': ('Calibrated phase shift, measurement reported in degrees, of the red light when the sensing '
                    'foil is excited with modulated blue light.'),
        'data_product_identifier': 'DOCONCS-DEG_L0',
        'ancillary_variables': 'raw_calibrated_phase',
        '_FillValue': np.nan
    },
    'raw_oxygen_thermistor': {
        'long_name': 'Raw Optode Thermistor',
        'units': 'V',
        'comment': ('The optode includes an integrated internal thermistor to measure the temperature at '
                    'the sensing foil. This value is recorded by the CTD as an analog voltage signal.'),
        '_FillValue': np.nan
    },
    'oxygen_thermistor_temperature': {
        'long_name': 'Optode Thermistor Temperature',
        'standard_name': 'temperature_of_sensor_for_oxygen_in_sea_water',
        'units': 'degrees_Celsius',
        'comment': ('Optode internal thermistor temperature used in calculation of the absolute oxygen '
                    'concentration. This is not the in situ sea water temperature, though it will be very close.'),
        'ancillary_variables': 'raw_oxygen_thermistor',
        '_FillValue': np.nan
    },
    'svu_oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'an optode oxygen sensor. It is computed using factory calibration coefficients, the '
                    'calibrated phase values and the optode thermistor temperature via the '
                    'Stern-Volmer-Uchida equation.'),
        'data_product_identifier': 'DOCONCS-L1',
        'ancillary_variables': 'oxygen_phase, oxygen_thermistor',
        '_FillValue': np.nan
    },
    'oxygen_concentration_corrected': {
        'long_name': 'Corrected Dissolved Oxygen Concentration',
        'standard_name': 'moles_of_oxygen_per_unit_mass_in_sea_water',
        'units': 'umol kg-1',
        'comment': ('Dissolved oxygen concentration corrected for the effects of density and salinity on the '
                    'sensor, and reported as the mole concentration per unit mass.'),
        'data_product_identifier': 'DOXYGEN_L2',
        'ancillary_variables': 'oxygen_concentration, pressure, temperature, salinity, lat, lon',
        '_FillValue': np.nan
    },

    # --> with WET Labs ECO Triplet (FLORT)
    'raw_backscatter': {
        'long_name': 'Raw Optical Backscatter',
        'units': 'counts',
        'comment': 'Raw optical backscatter at 700 nm measurements as recorded by the CTD.',
        'data_product_identifier': 'FLUBSCT_L0',
        '_FillValue': FILL_INT
    },
    'raw_chlorophyll': {
        'long_name': 'Raw Chlorophyll Fluorescence',
        'units': 'counts',
        'comment': ('Raw chlorophyll fluorescence (470 nm excitation/ 695 nm emission) measurements as recorded by '
                    'the CTD.'),
        'data_product_identifier': 'CHLAFLO_L0',
        '_FillValue': FILL_INT
    },
    'raw_cdom': {
        'long_name': 'Raw CDOM Fluorescence',
        'units': 'counts',
        'comment': ('Raw chromophoric dissolved organic matter (CDOM) fluorescence (370 nm excitation/ 460 nm '
                    'emission) measurements as recorded by the CTD.'),
        'data_product_identifier': 'CDOMFLO_L0',
        '_FillValue': FILL_INT
    },
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll Concentration',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'ug L-1',
        'comment': ('Estimated chlorophyll concentration based upon a calibration curve derived from a fluorescent '
                    'proxy approximately equal to 25 ug/L of a Thalassiosira weissflogii phytoplankton culture. '
                    'This measurement is considered to be an estimate only of the true chlorophyll concentration.'),
        'data_product_identifier': 'CHLAFLO_L1',
        'ancillary_variables': 'raw_chlorophyll',
        '_FillValue': np.nan
    },
    'fluorometric_cdom': {
        'long_name': 'Fluorometric CDOM Concentration',
        'standard_name': ('concentration_of_colored_dissolved_organic_matter_in_sea_water_expressed_as_equivalent_'
                          'mass_fraction_of_quinine_sulfate_dihydrate'),
        'units': 'ppb',
        'comment': ('More commonly referred to as Chromophoric Dissolved Organic Matter (CDOM). CDOM plays an '
                    'important role in the carbon cycling and biogeochemistry of coastal waters. It occurs naturally '
                    'in aquatic environments primarily as a result of tannins released from decaying plant and '
                    'animal matter, and can enter coastal areas in river run-off containing organic materials '
                    'leached from soils.'),
        'data_product_identifier': 'CDOMFLO_L1',
        'ancillary_variables': 'raw_cdom',
        '_FillValue': np.nan
    },
    'beta_700': {
        'long_name': 'Volume Scattering Function at 700 nm',
        'standard_name': 'volume_scattering_function_of_radiative_flux_in_sea_water',
        'units': 'm-1 sr-1',
        'comment': ('Radiative flux is the sum of shortwave and longwave radiative fluxes. Scattering of radiation '
                    'is its deflection from its incident path without loss of energy. The volume scattering function '
                    'is the intensity (flux per unit solid angle) of scattered radiation per unit length of '
                    'scattering medium, normalised by the incident radiation flux.'),
        'data_product_identifier': 'FLUBSCT_L1',
        'ancillary_variables': 'raw_backscatter',
        '_FillValue': np.nan
    },
    'total_optical_backscatter': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'standard_name': 'volume_backwards_scattering_coefficient_of_radiative_flux_in_sea_water',
        'units': 'm-1',
        'comment': ('Total (particulate + water) optical backscatter at 700 nm, derived from the Volume Scattering '
                    'Function and corrected for effects of temperature and salinity.'),
        'data_product_identifier': 'FLUBSCT_L2',
        'ancillary_variables': 'beta_700, temperature, salinity',
        '_FillValue': np.nan
    },
}
