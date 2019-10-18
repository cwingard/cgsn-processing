#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pco2w
@file cgsn_processing/process/configs/attr_pco2w.py
@author Christopher Wingard
@brief Attributes for the PCO2W variables
"""
import numpy as np

GLOBAL = {
    'global': {
        'title': 'Partial Pressure of CO2 in Sea Water',
        'summary': 'Partial pressure of CO2 in sea water measured using the Sunburst Sensors SAMI2-pCO2 instrument.',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal Endurance Array (EA) and Coastal and Global Scale Nodes (CGSN)',
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
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': ('Derived from either the DCL data logger GPS referenced clock, or the internal instrument clock ' +
                    'if this is an IMM hosted instrument. For instruments attached to a DCL, the instrument''s ' +
                    'internal clock is cross-compared to the GPS clock to determine the internal clock''s time ' +
                    'offset and drift.')
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': 'Mooring deployment location, surveyed after deployment to determine center of watch circle.'
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': 'Mooring deployment location, surveyed after deployment to determine center of watch circle.'
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Instrument deployment depth',
        'positive': 'down',
        'axis': 'Z'
    }
}

PCO2W = {
    'collect_date_time': {
        'long_name': 'Sample Collection Date and Time Stamp',
        'comment': 'Data logger time stamp, recorded when the instrument cycles the pump and collects a sample.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'process_date_time': {
        'long_name': 'Sample Processing Date and Time Stamp',
        'comment': ('Data logger time stamp, recorded when the instrument processes the sample after a period ' +
                    'of equilibration of the CO2 across the sample volume membrane.'),
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'unique_id': {
        'long_name': 'Instrument Unique ID',
        'comment': ('One byte checksum summary of the instrument serial number, name, calibration date and firmware ' +
                    'version serving as a proxy for a unique ID. While identified as the instrument unique ID, it is ' +
                    'possible for more than one instrument to have the same checksum summary. Thus, the uniqueness ' +
                    'of this value should be considered with a certain degree of caution.'),
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'record_number': {
        'long_name': 'IMM Record Number',
        'comment': 'Inductive modem record number',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'record_length': {
        'long_name': 'Record Length',
        'comment': 'Number of bytes in the record.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'record_type': {
        'long_name': 'Record Type',
        'comment': 'Records the record type, which is either a blank (type = 5), or a sampling (type = 4) record.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'comment': 'Derived from the SAMI2-pCO2 internal clock.',
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'calendar': 'gregorian'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'comment': ('Difference between the internal clock and the external GPS-based data logger clock. Offset ' +
                    'can be used to determine instrument clock offset and drift over the course of a deployment'),
        'units': 'seconds',
        'ancillary_variables': 'record_time, time'
    },
    'dark_reference_a': {
        'long_name': 'Dark LED Reference Intensity, 1st Measurement',
        'comment': ('First of two measurements of the dark LED reference intensity. Dark signal and reference ' +
                    'values, where the LEDs are turned off, should range from ~50 – 200. Higher or erratic dark ' +
                    'signals could indicate an electronic problem with the sensor'),
        'units': 'counts'
    },
    'dark_signal_a': {
        'long_name': 'Dark LED Signal Intensity, 1st Measurement',
        'comment': ('First of two measurements of the dark LED signal intensity. Dark signal and reference values, ' +
                    'where the LEDs are turned off, should range from ~50 – 200. Higher or erratic dark signals ' +
                    'could indicate an electronic problem with the sensor'),
        'units': 'counts'
    },
    'reference_434_a': {
        'long_name': 'Reference Intensity at 434 nm, 1st Measurement',
        'comment': ('First of two measurements of the reference intensity at 434 nm, used in combination with the ' +
                    'signal intensity to derive the optical absorbance ratio. Reference intensities should be ' +
                    'greater than ~1500. Lower intensities will result in higher noise in absorbance and, thus, ' +
                    'pCO2 measurements. However, if during blank measurement signal intensities are low, but ' +
                    'reference intensities are not, the flow cell needs to be flushed.'),
        'units': 'counts'
    },
    'signal_434_a': {
        'long_name': 'Signal Intensity at 434 nm, 1st Measurement',
        'comment': ('First of two measurements of the signal intensity at 434 nm, used in combination with the ' +
                    'reference intensity to derive the optical absorbance ratio. Signal intensities can range from ' +
                    '0 to 4096. If any signal intensity is at or near 4000, the channel may be saturated with light, ' +
                    'giving erroneous results. Blank signal intensities should be greater than ~1500.'),
        'units': 'counts'
    },
    'reference_620_a': {
        'long_name': 'Reference Intensity at 620 nm, 1st Measurement',
        'comment': ('First of two measurements of the reference intensity at 620 nm, used in combination with the ' +
                    'signal intensity to derive the optical absorbance ratio. Reference intensities should be ' +
                    'greater than ~1500. Lower intensities will result in higher noise in absorbance and, thus, ' +
                    'pCO2 measurements. However, if during a blank measurement signal intensities are low, but ' +
                    'reference intensities are not, the flow cell needs to be flushed.'),
        'units': 'counts'
    },
    'signal_620_a': {
        'long_name': 'Signal Intensity at 620 nm, 1st Measurement',
        'comment': ('First of two measurements of the signal intensity at 620 nm, used in combination with the ' +
                    'reference intensity to derive the optical absorbance ratio. Signal intensities can range from ' +
                    '0 to 4096. If any signal intensity is at or near 4000, the channel may be saturated with light, ' +
                    'giving erroneous results. Blank signal intensities should be greater than ~1500.'),
        'units': 'counts'
    },
    'ratio_434': {
        'long_name': 'Optical Absorbance Ratio at 434 nm',
        'comment': ('Optical absorbance ratio at 434 nm and report in counts. During a measurement cycle, this value ' +
                    'is used in the calculation of pCO2. During a blank measurement (approximately every few days), ' +
                    'this value is used to determine the blank intensity ratio at 434 nm.'),
        'data_product_identifier': 'CO2ABS1_L0',
        'units': 'counts'
    },
    'ratio_620': {
        'long_name': 'Optical Absorbance Ratio at 620 nm',
        'comment': ('Optical absorbance ratio at 620 nm and report in counts. During a measurement cycle, this value ' +
                    'is used in the calculation of pCO2. During a blank measurement (approximately every few days), ' +
                    'this value is used to determine the blank intensity ratio at 620 nm.'),
        'data_product_identifier': 'CO2ABS2_L0',
        'units': 'counts'
    },
    'dark_reference_b': {
        'long_name': 'Dark LED Reference Intensity, 2nd Measurement',
        'comment': ('Second of two measurements of the dark LED reference intensity. Dark signal and reference ' +
                    'values, where the LEDs are turned off, should range from ~50 – 200. Higher or erratic dark ' +
                    'signals could indicate an electronic problem with the sensor'),
        'units': 'counts'
    },
    'dark_signal_b': {
        'long_name': 'Dark LED Signal Intensity, 2nd Measurement',
        'comment': ('Second of two measurements of the dark LED signal intensity. Dark signal and reference values, ' +
                    'where the LEDs are turned off, should range from ~50 – 200. Higher or erratic dark signals ' +
                    'could indicate an electronic problem with the sensor'),
        'units': 'counts'
    },
    'reference_434_b': {
        'long_name': 'Reference Intensity at 434 nm, 2nd Measurement',
        'comment': ('Second of two measurements of the reference intensity at 434 nm, used in combination with the ' +
                    'signal intensity to derive the optical absorbance ratio. Reference intensities should be ' +
                    'greater than ~1500. Lower intensities will result in higher noise in absorbance and, thus, ' +
                    'pCO2 measurements. However, if during blank measurement signal intensities are low, but ' +
                    'reference intensities are not, the flow cell needs to be flushed.'),
        'units': 'counts'
    },
    'signal_434_b': {
        'long_name': 'Signal Intensity at 434 nm, 2nd Measurement',
        'comment': ('Second of two measurements of the signal intensity at 434 nm, used in combination with the ' +
                    'reference intensity to derive the optical absorbance ratio. Signal intensities can range from ' +
                    '0 to 4096. If any signal intensity is at or near 4000, the channel may be saturated with light, ' +
                    'giving erroneous results. Blank signal intensities should be greater than ~1500.'),
        'units': 'counts'
    },
    'reference_620_b': {
        'long_name': 'Reference Intensity at 620 nm, 2nd Measurement',
        'comment': ('Second of two measurements of the reference intensity at 620 nm, used in combination with the ' +
                    'signal intensity to derive the optical absorbance ratio. Reference intensities should be ' +
                    'greater than ~1500. Lower intensities will result in higher noise in absorbance and, thus, ' +
                    'pCO2 measurements. However, if during a blank measurement signal intensities are low, but ' +
                    'reference intensities are not, the flow cell needs to be flushed.'),
        'units': 'counts'
    },
    'signal_620_b': {
        'long_name': 'Signal Intensity at 620 nm, 2nd Measurement',
        'comment': ('Second of two measurements of the signal intensity at 620 nm, used in combination with the ' +
                    'reference intensity to derive the optical absorbance ratio. Signal intensities can range from ' +
                    '0 to 4096. If any signal intensity is at or near 4000, the channel may be saturated with light, ' +
                    'giving erroneous results. Blank signal intensities should be greater than ~1500.'),
        'units': 'counts'
    },
    'raw_battery_voltage': {
        'long_name': 'Raw Battery Voltage',
        'comment': ('Raw internal battery voltage measured in counts. May actually reflect external voltage if ' +
                    'external power is applied'),
        'units': 'counts'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': ('Voltage of the internal battery pack. May actually reflect external voltage if ' +
                    'external power is applied'),
        'units': 'V',
        'ancillary_variables': 'raw_battery_voltage'
    },
    'raw_thermistor': {
        'long_name': 'Raw Thermistor Temperature',
        'comment': 'Thermistor resistivity measured in counts.',
        'units': 'counts'
    },
    'thermistor_temperature': {
        'long_name': 'Thermistor Temperature',
        'comment': ('Thermistor temperature refers to the internal instrument temperature of the pCO2 sensor, as ' +
                    'measured by the thermistor. It is used in the determination of pCO2.'),
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius',
        'ancillary_variables': 'raw_thermistor'
    },
    'k434': {
        'long_name': 'Blank Intensity Ratio at 434 nm',
        'comment': ('Ratio of the measured optical absorbance ratio at 434 nm where the sample volume is filled with ' +
                    'deionized water. These blank measurements are used to track and correct instrument drift over ' +
                    'the course of a deployment and are collected every few days.'),
        'units': '1',
        '_FillValue': np.nan,
        'ancillary_variables': 'ratio_434'
    },
    'k620': {
        'long_name': 'Blank Intensity Ratio at 620 nm',
        'comment': ('Ratio of the measured optical absorbance ratio at 620 nm where the sample volume is filled with ' +
                    'deionized water. These blank measurements are used to track and correct instrument drift over ' +
                    'the course of a deployment and are collected every few days.'),
        'units': '1',
        '_FillValue': np.nan,
        'ancillary_variables': 'ratio_620'
    },
    'pCO2': {
        'long_name': 'Seawater pCO2',
        'comment': ('Partial Pressure of CO2 in Seawater provides a measure of the amount of CO2 and HCO3 in ' +
                    'seawater. Specifically, it refers to the pressure that would be exerted by CO2 if all other ' +
                    'gases were removed. Partial pressure of a gas dissolved in seawater is understood as the ' +
                    'partial pressure in air that the gas would exert in a hypothetical air volume in equilibrium ' +
                    'with seawater.'),
        'standard_name': 'partial_pressure_of_carbon_dioxide_in_sea_water',
        'data_product_identifier': 'PCO2WAT_L1',
        'units': 'uatm',
        '_FillValue': np.nan,
        'ancillary_variables': 'ratio_434, ratio_620, thermistor_temperature, k434, k620'
    }
}
