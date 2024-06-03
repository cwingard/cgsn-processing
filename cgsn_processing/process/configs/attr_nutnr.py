#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_nutnr
@file cgsn_processing/process/configs/attr_nutnr.py
@author Christopher Wingard
@brief Attributes for the ISUS and SUNA nitrate sensors
"""
from cgsn_processing.process.common import FILL_INT, FILL_NAN

NUTNR = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Nitrate Concentration',
        'summary': ('Nitrate concentration in sea water measured using either the Satlantic ISUS-V3, or the SUNA-V2 '
                    'sensor.'),
    },
    # attributes common to all forms of the NUTNR
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': '',    deliberately left blank, no units for this value,
        'comment': 'Instrument serial number.'
    },
    'nitrate_concentration': {
        'long_name': 'Nitrate Concentration',
        'standard_name': 'mole_concentration_of_nitrate_in_sea_water',
        'units': 'umol L-1',
        'data_product_identifier': 'NITROPT_L1',
        'comment': ('Initial estimate of the dissolved nitrate concentration calculated onboard the sensor. This '
                    'value has not been corrected for the effects of salinity and temperature, instead using onboard '
                    'constants.')
    },
    'channel_measurements': {
        'long_name': 'Raw Absorbance Measurements',
        'units': 'counts',
        'data_product_identifier': 'NITROPT_L0',
        'comment': ('Array of 256 raw absorbance measurements in the UV portion of the spectra, used to derive the '
                    'nitrate concentration.'),
        '_FillValue': FILL_INT
    },
    'spectral_average': {
        'long_name': 'Spectral Average',
        'units': 'counts',
        'comment': 'Average value of the raw absorbance measurements.',
        '_FillValue': FILL_INT
    },
    'seawater_dark': {
        'long_name': 'Seawater Dark Measurement',
        'units': 'counts',
        'comment': ('Average, raw absorbance measurement when the lamp is turned off. The value is used as the '
                    'dark reference in the calculation of the dissolved nitrate concentration.'),
        '_FillValue': FILL_INT
    },
    'rms_error': {
        'long_name': 'Root Mean Square Error',
        'units': 'counts',
        'comment': ('The root mean square error parameter can be used to make an estimate of how well the nitrate '
                    'spectral fit is. This should usually be less than 1E-3. If it is higher, there is spectral shape '
                    '(likely due to CDOM) that adversely impacts the nitrate estimate.')
    },
    'fit_auxiliary_1': {
        'long_name': 'Auxiliary Fit 1',
        # 'units': ''    # deliberately left blank, units for this value are unknown,
        'comment': 'Vendor documentation does not provide enough information to define this variable.',
        '_FillValue': FILL_NAN
    },
    'fit_auxiliary_2': {
        'long_name': 'Auxiliary Fit 2',
        # 'units': ''    # deliberately left blank, units for this value are unknown,
        'comment': 'Vendor documentation does not provide enough information to define this variable.',
        '_FillValue': FILL_NAN
    },
    'temperature_internal': {
        'long_name': 'Internal Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Internal instrument temperature at the time of the measurement.',
        '_FillValue': FILL_NAN
    },
    'temperature_spectrometer': {
        'long_name': 'Spectrometer Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Temperature of the spectrometer at the time of the measurement.',
        '_FillValue': FILL_NAN
    },
    'temperature_lamp': {
        'long_name': 'Lamp Temperature',
        'units': 'degrees_Celsius',
        'comment': ('Temperature of the lamp at the time of the measurement. The sensor will turn off the lamp if the '
                    'lamp temperature exceeds 35 degrees Celsius.'),
        '_FillValue': FILL_NAN
    },
    'lamp_on_time': {
        'long_name': 'Lamp On Time',
        'units': 's',
        'comment': 'Total time the lamp has been turned on. The lamp should be replaced after 1000 hours.',
        '_FillValue': FILL_INT
    },
    'humidity': {
        'long_name': 'Relative Humidity',
        'units': 'percent',
        'comment': 'Percent relative humidity internal to the sensor. Increasing values can indicate a slow leak.',
        '_FillValue': FILL_NAN
    },
    'voltage_lamp': {
        'long_name': 'Lamp Voltage',
        'units': 'V',
        'comment': 'Voltage supplied to the lamp.',
        '_FillValue': FILL_NAN
    },
    'voltage_main': {
        'long_name': 'Main Voltage',
        'units': 'V',
        'comment': 'Voltage supplied to the instrument.',
        '_FillValue': FILL_NAN
    },
    'wavelengths': {
        'long_name': 'Measurement Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
        'comment': 'Spectral range, between 190 and 370 nm, output by the sensor. Exact range is instrument specific, '
                   'with the values obtained from the instrument calibration record.',
    },
    # parameters unique to the ISUS
    'voltage_analog': {
        'long_name': 'Analog Voltage',
        'units': 'V',
        'comment': 'Voltage supplied to analog sensors connected to the instrument.',
        '_FillValue': FILL_NAN
    },
    'fit_auxiliary_3': {
        'long_name': 'Auxiliary Fit 3',
        # 'units': ''    # deliberately left blank, units for this value are unknown,
        'comment': 'Vendor documentation does not provide enough information to define this variable.',
        '_FillValue': FILL_NAN
    },
    'average_reference': {
        'long_name': 'Reference Diode Average',
        'units': 'counts',
        'comment': ('Average of the reference diode measurements (used as an indicator of lamp output) collected '
                    'during the sample time.'),
        '_FillValue': FILL_NAN
    },
    'variance_reference': {
        'long_name': 'Reference Diode Variance',
        'units': 'counts',
        'comment': ('Variance of the reference diode measurements (used as an indicator of lamp output) collected '
                    'during the sample time.'),
        '_FillValue': FILL_NAN
    },
    # parameters unique to the SUNA
    'nitrogen_in_nitrate': {
        'long_name': 'Nitrogen Concentration',
        'standard_name': 'mass_concentration_of_inorganic_nitrogen_in_sea_water',
        'units': 'mg L-1',
        'comments': ('The dissolved inorganic nitrogen concentration derived from the nitrate concentration '
                     'and expressed in units of mg Nitrogen per liter. Most water monitoring programs and many '
                     'researchers use units of milligrams per liter. This unit is almost always expressed as '
                     'milligrams of relevant atoms per liter—for example, milligrams of nitrogen (N) per liter, rather '
                     'than milligrams of nitrate per liter. Although nitrate NO3 is the most prevalent form of '
                     'nitrogen, this unit is frequently used as a means of easily keeping track of total nitrogen '
                     'loading.'),
    },
    'absorbance_254': {
        'long_name': 'Absorbance at 254 nm',
        'units': 'counts',
        'comment': 'Absorbance measurement at 254 nm.',
    },
    'absorbance_350': {
        'long_name': 'Absorbance at 350 nm',
        'units': 'counts',
        'comment': 'Absorbance measurement at 350 nm.',
    },
    'bromide_trace': {
        'long_name': 'Bromide Trace Concentration',
        'units': 'mg L-1',
        'comment': ('Bromide ion is one of the trace constituents of seawater, and its average concentration in '
                    'seawater is approximately 60–70 mg/L.'),
    },
    'integration_factor': {
        'long_name': 'Integration Time Factor',
        'units': 'ms',
        'comment': ('The SUNA V2 has a 256-channel spectrometer that integrates for a specific length of time, '
                    'usually 300–500 ms, to maximize the signal while it collects data. When the sensor does a '
                    'measurement, the spectrograph collects UV light for the length of the integration period. In '
                    'optically dense waters, with high turbidity or CDOM, very little UV light is transmitted through '
                    'the water, so the spectrometer ''sees'' a much lower signal. The SUNA V2 automatically increases '
                    'the integration period to compensate for the low light, so the sensor collects a strong signal '
                    'in extreme environmental conditions.'),
    },
    'voltage_internal': {
        'long_name': 'Internal Voltage',
        'units': 'V',
        'comment': 'Internal voltage used by the sensor for operations.',
    },
    'main_current': {
        'long_name': 'Main Current',
        'units': 'mA',
        'comment': 'Main current draw by the sensor during the measurement cycle.',
    },
    'fit_base_1': {
        'long_name': 'Fit Base 1',
        # 'units': ''    # deliberately left blank, units for this value are unknown,
        'comment': 'Vendor documentation does not provide enough information to define this variable.'
    },
    'fit_base_2': {
        'long_name': 'Fit Base 2',
        # 'units': ''    # deliberately left blank, units for this value are unknown,
        'comment': 'Vendor documentation does not provide enough information to define this variable.'
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
        '_FillValue': FILL_NAN
    },
    'ctd_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. Measurements are from a '
                    'co-located CTD'),
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': FILL_NAN
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
        '_FillValue': FILL_NAN
    },
    # dataset attributes --> derived values
    'corrected_nitrate': {
        'long_name': 'Corrected Nitrate Concentration',
        'standard_name': 'mole_concentration_of_nitrate_in_sea_water',
        'units': 'umol L-1',
        'comments': ('The dissolved nitrate concentration with the Sakamoto et. al. (2009) algorithm that uses the '
                     'observed sample salinity and temperature to subtract the bromide component of the overall '
                     'seawater UV absorption spectrum before solving for the nitrate concentration.'),
        'data_product_identifier': 'NITRTSC_L2',
        '_FillValue': FILL_NAN,
    },
    'corrected_nitrogen_in_nitrate': {
        'long_name': 'Corrected Nitrogen Concentration',
        'standard_name': 'mass_concentration_of_inorganic_nitrogen_in_sea_water',
        'units': 'mg L-1',
        'comments': ('The dissolved inorganic nitrogen concentration derived from the corrected nitrate concentration '
                     'and expressed in units of mg Nitrogen per liter. Most water monitoring programs and many '
                     'researchers use units of milligrams per liter. This unit is almost always expressed as '
                     'milligrams of relevant atoms per liter—for example, milligrams of nitrogen (N) per liter, rather '
                     'than milligrams of nitrate per liter. Although nitrate NO3 is the most prevalent form of '
                     'nitrogen, this unit is frequently used as a means of easily keeping track of total nitrogen '
                     'loading.'),
        '_FillValue': FILL_NAN
    }
}
