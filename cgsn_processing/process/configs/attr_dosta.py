#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_dosta
@file cgsn_processing/process/configs/attr_dosta.py
@author Christopher Wingard
@brief Attributes for the dissolved oxygen (DOSTA) sensor
"""
import numpy as np

DOSTA = {
    # global and coordinate attributes
    'global': {
        'title': 'Dissolved Oxygen (DOSTA) Data',
        'summary': 'Dissolved oxygen concentrations from the Aanderaa Optode dissolved oxygen sensor.'
    },
    # dataset attributes --> parsed data
    'product_number': {
        'long_name': 'Product Number',
        'comment': 'Optode product number, usually model 4831 for OOI systems.',
        # 'units': '',    deliberately left blank, no units for this value,
    },
    'serial_number': {
        'long_name': 'Serial Number',
        'comment': 'Instrument serial number.',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'an optode oxygen sensor. Computed on-board the sensor using internal calibration coefficients.'),
        'data_product_identifier': 'DOCONCS_L1'
    },
    'oxygen_saturation': {
        'long_name': 'Dissolved Oxygen Saturation',
        'units': 'percent',
        'comment': ('Oxygen saturation is the percentage of dissolved oxygen relative to the absolute solubility of '
                    'oxygen at a particular water temperature. Computed on-board the sensor using internal calibration '
                    'coefficients.')
    },
    'oxygen_thermistor_temperature': {
        'long_name': 'Optode Thermistor Temperature',
        'standard_name': 'temperature_of_sensor_for_oxygen_in_sea_water',
        'units': 'degrees_Celsius',
        'comment': ('Optode internal thermistor temperature used in calculation of the absolute oxygen ' 
                    'concentration. This is not the in-situ sea water temperature, though it will be very close.'),
        'ancillary_variables': 'raw_oxygen_thermistor'
    },
    'calibrated_phase': {
        'long_name': 'Calibrated Phase Difference',
        'units': 'degrees',
        'comment': ('The optode measures oxygen by exciting a special platinum porphyrin complex embedded in a '
                    'gas permeable foil with modulated blue light. The optode measures the phase shift of the '
                    'returned red light. By linearizing and temperature compensating, with an incorporated '
                    'temperature sensor, the absolute O2 concentration can be determined.'),
        'data_product_identifier': 'DOCONCS-VLT_L0'
    },
    'compensated_phase': {
        'long_name': 'Temperature Compensated Calibrated Phase Difference',
        'units': 'degrees',
        'comment': 'Temperature compensated (using the temperature data from an onboard thermistor) calibrated phase '
                   'difference.',
        'ancillary_variables': 'oxygen_thermistor_temperature, calibrated_phase'
    },
    'blue_phase': {
        'long_name': 'Blue Phase Measurement',
        'units': 'degree',
        'comment': ('Phase measurement with blue excitation light of the returned signal after the luminophore '
                    'quenching')
    },
    'red_phase': {
        'long_name': 'Red Phase Measurement',
        'units': 'degree',
        'comment': ('Phase measurement, with red excitation light, of the returned signal after the luminophore '
                    'quenching')
    },
    'blue_amplitude': {
        'long_name': 'Blue Amplitude Measurement',
        'units': 'mV',
        'comment': ('Amplitude measurement, with blue excitation light, of the returned signal after the luminophore '
                    'quenching')
    },
    'red_amplitude': {
        'long_name': 'Red Amplitude Measurement',
        'units': 'mV',
        'comment': ('Amplitude measurement, with red excitation light, of the returned signal after the luminophore '
                    'quenching')
    },
    'raw_oxygen_thermistor': {
        'long_name': 'Raw Optode Thermistor Temperature',
        'units': 'mV',
        'comment': ('The optode includes an integrated internal thermistor to measure the temperature at '
                    'the sensing foil.')
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
    'svu_oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'an optode oxygen sensor. Compares to the oxygen_concentration computed on-board the sensor, '
                    'but is recomputed using factory calibration coefficients, the calibrated phase values and '
                    'the optode thermistor temperature via the Stern-Volmer-Uchida equation.'),
        'data_product_identifier': 'DOCONCS_L1',
        'ancillary_variables': 'oxygen_thermistor_temperature, calibrated_phase',
        '_FillValue': np.nan
    },
    'oxygen_concentration_corrected': {
        'long_name': 'Corrected Dissolved Oxygen Concentration',
        'standard_name': 'moles_of_oxygen_per_unit_mass_in_sea_water',
        'units': 'umol kg-1',
        'comments': ('The dissolved oxygen concentration from the Stable Response Dissolved Oxygen Instrument is a '
                     'measure of the concentration of gaseous oxygen mixed in seawater. This data product corrects '
                     'the dissolved oxygen concentration for the effects of salinity, temperature, and pressure with '
                     'data from a co-located CTD.'),
        'data_product_identifier': 'DOXYGEN_L2',
        'ancillary_variables': 'svu_oxygen_concentration, ctd_temperature, ctd_pressure, ctd_salinity, lat, lon',
        '_FillValue': np.nan
    }
}
