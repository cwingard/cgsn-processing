#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_optaa
@file cgsn_processing/process/configs/attr_optaa.py
@author Christopher Wingard
@brief Attributes for the OPTAA variables
"""
from cgsn_processing.process.common import FILL_INT, FILL_NAN

OPTAA = {
    'global': {
        'title': 'Optical Absorbance and Attenuation from OPTAA',
        'summary': (
            'Measures the absorabance and attenuation of particulate and dissolved organic matter with ' +
            'the Sea-Bird Scientific Spectral Absorption and Attenuation Sensor (AC-S).'
        ),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes, (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.6'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, ' +
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': ('Derived from the DCL data logger GPS referenced clock and the internal instrument clock. ' +
                    'The DCL clock information is pulled from the date and time string in the file name.')
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and ' +
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and ' +
                    'the center of the watch circle.')
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Instrument deployment depth',
        'positive': 'down',
        'axis': 'Z'
    },
    # attributes for the raw data sets
    'serial_number': {
        'long_name': 'Unit Serial Number',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pressure_raw': {
        'long_name': 'Raw Pressure',
        'units': 'counts',
        'comment': ('Raw measurements, reported in counts, from the AC-S pressure sensor. If the unit is not ' +
                    'equipped with a pressure sensor, the values will all be 0.')
    },
    'external_temp_raw': {
        'long_name': 'Raw In-Situ Temperature',
        'units': 'counts',
        'data_product_identifier': 'OPTTEMP_L0',
        'comment': ('Raw measurements, reported in counts, from the AC-S external temperature sensor. This sensor ' +
                    'measures the in-situ seawater termperature.')
    },
    'internal_temp_raw': {
        'long_name': 'Raw Internal Instrument Temperature',
        'units': 'counts',
        'comment': ('Raw measurements, reported in counts, from the AC-S internal temperature sensor. This sensor ' +
                    'measures the internal instrument termperature and is used in converting the raw optical ' +
                    'measurements into absorbance and attenuation estimates.')
    },
    'elapsed_run_time': {
        'long_name': 'Elapsed Run Time',
        'units': 'ms',
        'comment': ('Time in milliseconds since the instrument was powered on.')
    },
    'wavelength_number': {
        'long_name': 'Wavelength Number',
        # 'units': ''    # deliberately left blank, no units for this value
        'comment': ('An index between 0 and 99 used to set a common length dimension for the absorbance and ' +
                    'attenuation measurements. The actual number of wavelengths is variable between sensors ' +
                    'and may even change for a particular sensor over time if servicing requires a replacement ' +
                    'of the filter set. The actual number of wavelengths for this sensor is represented here ' +
                    'by the attribute actual_wavelengths.')
    },
    'a_wavelengths': {
        'long_name': 'A Channel Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
        'comment': ('Absorbance measurement wavelengths, specific to the filter wheel set installed in the AC-S.'),
        '_FillValue': FILL_NAN,
    },
    'a_reference_dark': {
        'long_name': 'A Channel Dark Reference',
        'units': 'counts',
        'comment': ('A channel reference detector dark counts (before the lamp is turned on). Used in conversion ' +
                    'of the raw a channel measurements to absorbance estimates.')
    },
    'a_reference_raw': {
        'long_name': 'A Channel Raw Reference',
        'units': 'counts',
        'comment': ('A channel reference detector raw counts (while the lamp is turned on). Used in conversion ' +
                    'of the raw a channel measurements to absorbance estimates.'),
        'data_product_identifier': 'OPTAREF_L0',
        '_FillValue': FILL_INT,
    },
    'a_signal_dark': {
        'long_name': 'A Channel Dark Signal',
        'units': 'counts',
        'comment': ('A channel signal detector dark counts (before the lamp is turned on). Used in conversion ' +
                    'of the raw a channel measurements to absorbance estimates.')
    },
    'a_signal_raw': {
        'long_name': 'A Channel Raw Signal',
        'units': 'counts',
        'comment': ('A channel signal detector raw ounts (while the lamp is turned on). Used in conversion ' +
                    'of the raw a channel measurements to absorbance estimates.'),
        'data_product_identifier': 'OPTASIG_L0',
        '_FillValue': FILL_INT,
    },
    'c_wavelengths': {
        'long_name': 'C Channel Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
        'comment': ('Attenuation measurement wavelengths, specific to the filter wheel set installed in the AC-S.'),
        '_FillValue': FILL_NAN,
    },
    'c_reference_dark': {
        'long_name': 'C Channel Dark Reference',
        'units': 'counts',
        'comment': ('C channel reference detector dark counts (before the lamp is turned on). Used in conversion ' +
                    'of the raw c channel measurements to attenuation estimates.')
    },
    'c_reference_raw': {
        'long_name': 'C Channel Raw Reference',
        'units': 'counts',
        'comment': ('C channel reference detector raw counts (while the lamp is turned on). Used in conversion ' +
                    'of the raw c channel measurements to attenuation estimates.'),
        'data_product_identifier': 'OPTCREF_L0',
        '_FillValue': FILL_INT,
    },
    'c_signal_dark': {
        'long_name': 'C Channel Dark Signal',
        'units': 'counts',
        'comment': ('C channel signal detector dark counts (before the lamp is turned on). Used in conversion ' +
                    'of the raw c channel measurements to attenuation estimates.')
    },
    'c_signal_raw': {
        'long_name': 'C Channel Raw Signal',
        'units': 'counts',
        'comment': ('C channel signal detector raw counts (while the lamp is turned on). Used in conversion ' +
                    'of the raw c channel measurements to attenuation estimates.'),
        'data_product_identifier': 'OPTCSIG_L0',
        '_FillValue': FILL_INT,
    },

    # Derived values in the processed data set
    'pressure': {
        'long_name': 'Pressure',
        'units': 'dbar',
        'comment': ('Seawater pressure, measured at the top of the pressure housing. If the unit is not equipped ' +
                    'with a pressure sensor, the values will all be reported as 0.'),
        'ancillary_variables': 'pressure_raw',
    },
    'external_temp': {
        'long_name': 'In-Situ Temperature',
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius',
        'comment': ('In-situ sea water temperature measurements from the sensor mounted at the top of the ' +
                    'AC-S pressure housing.'),
        'ancillary_variables': 'external_temp_raw',
    },
    'internal_temp': {
        'long_name': 'Internal Instrument Temperature',
        'units': 'degrees_Celsius',
        'comment': ('Internal instrument temperature, used to convert raw absorbance and attenuation measurements.'),
        'ancillary_variables': 'internal_temp_raw',
    },
    'apd': {
        'long_name': 'Particulate and Dissolved Absorbance',
        'units': 'm-1',
        'comment': ('The optical absorption coefficient is the rate that the intensity of a beam of light will ' +
                    'decrease in response to the absorption (removal) of light energy as a function of propagation ' +
                    'distance. The optical absorption coefficient reflects the absorption coefficient for the ' +
                    'combination of all seawater impurities including all particulate and dissolved matter of ' +
                    'optical importance.'),
        'ancillary_variables': ('a_wavelengths internal_temp a_signal_raw a_reference_raw ' +
                                'a_signal_dark a_reference_dark'),
        '_FillValue': FILL_NAN,
    },
    'apd_ts': {
        'long_name': 'Particulate and Dissolved Absorbance with TS Correction',
        'units': 'm-1',
        'comment': ('The optical absorption coefficient corrected for the effects of temperature and salinity. ' +
                    'This dataset assumes a constant salinity of 33 psu, given the overall negligible effects of ' +
                    'salinity (as opposed to temperature) on the absorption coefficient.'),
        'ancillary_variables': 'a_wavelengths external_temp apd',
        '_FillValue': FILL_NAN,
    },
    'apd_ts_s': {
        'long_name': 'Particulate and Dissolved Absorbance with TS and Scatter Correction',
        'units': 'm-1',
        'comment': ('The optical absorption coefficient corrected for the effects of temperature and salinity, ' +
                    'with the baseline effects due to scattering at 715 nm removed.'),
        'data_product_identifier': 'OPTABSN_L2',
        'ancillary_variables': 'oxygen_concentration, pressure, temperature, salinity, lat, lon',
        '_FillValue': FILL_NAN,
    },
    'cpd': {
        'long_name': 'Particulate and Dissolved Attenuation',
        'units': 'm-1',
        'comment': ('The optical beam attenuation coefficient is the rate that the intensity of a beam of light will ' +
                    'decrease in response to the combined effects of absorption and scatter as a function of ' +
                    'propagation distance. The attenuation coefficient results from the spectral beam attenuation of ' +
                    'the combination of all seawater impurities including all particulate and dissolved matter of ' +
                    'optical importance.'),
        'ancillary_variables': ('c_wavelengths internal_temp c_signal_raw c_reference_raw ' +
                                'c_signal_dark c_reference_dark'),
        '_FillValue': FILL_NAN,
    },
    'cpd_ts': {
        'long_name': 'Particulate and Dissolved Attenuation with TS Correction',
        'units': 'm-1',
        'comment': ('The optical beam attenuation coefficient corrected for the effects of temperature and salinity. ' +
                    'This dataset assumes a constant salinity of 33 psu, given the overall negligible effects of ' +
                    'salinity (as opposed to temperature) on the attenuation coefficient.'),
        'data_product_identifier': 'OPTATTN_L2',
        'ancillary_variables': 'c_wavelengths external_temp cpd',
        '_FillValue': FILL_NAN,
    }
}
