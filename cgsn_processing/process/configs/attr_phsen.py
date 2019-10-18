#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""
import numpy as np

GLOBAL = {
    'global': {
        'title': 'Seawater pH',
        'summary': (
            'Measurements of the seawater pH using the Sunburst Sensors SAMI2-pH Instrument.'
        ),
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


PHSEN = {
    'dcl_date_time_string': {
        'long_name': 'DCL Date and Time Stamp',
        'comment': 'Data logger time stamp, recorded when instrument begins measurement cycle.',
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
    'measurements': {
        'long_name': 'Measurements Array',
        'comment': 'Dimensional indexing array created for the reference and light measurements.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'blank_refrnc_434': {
        'long_name': 'DI Blank Reference Intensity at 434 nm',
        'comment': ('Optical absorbance reference intensity at 434 nm. Measured with deionized water. Reference and ' +
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower ' +
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'blank_signal_434': {
        'long_name': 'DI Blank Signal Intensity at 434 nm',
        'comment': ('Optical absorbance signal intensity at 434 nm. Measured with deionized water. Reference and ' +
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower ' +
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'blank_refrnc_578': {
        'long_name': 'DI Blank Reference Intensity at 578 nm',
        'comment': ('Optical absorbance reference intensity at 578 nm. Measured with deionized water. Reference and ' +
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower ' +
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'blank_signal_578': {
        'long_name': 'DI Blank Signal Intensity at 578 nm',
        'comment': ('Optical absorbance signal intensity at 578 nm. Measured with deionized water. Reference and ' +
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower ' +
                    'intensities will result in higher noise in the absorbance and pH measurements.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'reference_434': {
        'long_name': 'Reference Intensity at 434 nm',
        'comment': ('Optical absorbance reference intensity at 434 nm. Reference and signal intensities range ' +
                    'between 0 and 4096. Values should be greater than ~1500. Lower intensities will result in ' +
                    'higher noise in the absorbance and pH measurements.'),
        'units': 'counts'
    },
    'signal_434': {
        'long_name': 'Signal Intensity at 434 nm',
        'comment': ('Optical absorbance signal intensity at 434 nm. Reference and signal intensities range between 0 ' +
                    'and 4096. Values should be greater than ~1500. Lower intensities will result in higher noise in ' +
                    'the absorbance and pH measurements.'),
        'data_product_identifier': 'PH434SI_L0',
        'units': 'counts'
    },
    'reference_578': {
        'long_name': 'Reference Intensity at 578 nm',
        'comment': ('Optical absorbance reference intensity at 578 nm. Reference and signal intensities range ' +
                    'between 0 and 4096. Values should be greater than ~1500. Lower intensities will result in ' +
                    'higher noise in the absorbance and pH measurements.'),
        'units': 'counts'
    },
    'signal_578': {
        'long_name': 'Signal Intensity at 578 nm',
        'comment': ('Optical absorbance signal intensity at 578 nm. Reference and signal intensities range between 0 ' +
                    'and 4096. Values should be greater than ~1500. Lower intensities will result in higher noise in ' +
                    'the absorbance and pH measurements.'),
        'data_product_identifier': 'PH578SI_L0',
        'units': 'counts'
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
        'comment': 'Data and control record type. For the SAMI2-pH sensor, the record type is 10',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'record_time': {
        'long_name': 'Instrument Timestamp',
        'comment': 'Derived from the SAMI2-pH internal clock.',
        'units': 'seconds since 1970-01-01',
        'calendar': 'gregorian'
    },
    'raw_thermistor_start': {
        'long_name': 'Raw Thermistor Temperature, Measurement Start',
        'comment': 'Thermistor resistivity measured in counts at the start of the measurement cycle.',
        'units': 'counts'
    },
    'raw_thermistor_end': {
        'long_name': 'Raw Thermistor Temperature, Measurement End',
        'comment': 'Thermistor resistivity measured in counts at the end of the measurement cycle.',
        'units': 'counts'
    },
    'raw_battery_voltage': {
        'long_name': 'Raw Battery Voltage',
        'comment': ('Raw internal battery voltage measured in counts. May actually reflect external voltage if ' +
                    'external power is applied'),
        'units': 'counts'
    },
    'thermistor_temperature_start': {
        'long_name': 'Thermistor Temperature, Measurement Start',
        'comment': ('Thermistor temperature refers to the internal instrument temperature of the pH sensor, as ' +
                    'measured by the thermistor. It is used to determine salinity and temperature dependent molar ' +
                    'absorptivities in the seawater sample in order to make an accurate pH estimation. This ' +
                    'variable represents the thermistor temperature measured at the beginning of the measurement ' +
                    'cycle'),
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius',
        'ancillary_variables': 'raw_thermistor_start'
    },
    'thermistor_temperature_end': {
        'long_name': 'Thermistor Temperature, Measurement End',
        'comment': ('Thermistor temperature refers to the internal instrument temperature of the pH sensor, as ' +
                    'measured by the thermistor. It is used to determine salinity and temperature dependent molar ' +
                    'absorptivities in the seawater sample in order to make an accurate pH estimation. This ' +
                    'variable represents the thermistor temperature measured at the end of the measurement cycle'),
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius',
        'ancillary_variables': 'raw_thermistor_end'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': ('Voltage of the internal battery pack. May actually reflect external voltage if ' +
                    'external power is applied'),
        'units': 'V',
        'ancillary_variables': 'raw_battery_voltage'
    },
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'comment': ('Difference between the internal clock and the external GPS-based data logger clock. Offset ' +
                    'can be used to determine instrument clock offset and drift over the course of a deployment'),
        'units': 'seconds',
        'ancillary_variables': 'record_time, time'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of seawater. ' +
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of ' +
                    'seawater and adjusted for temperature and pressure. It is approximately equivalent to Absolute ' +
                    'Salinity (the mass fraction of dissolved salt in seawater) but they are not interchangeable. ' +
                    'Data from a co-located CTD, if available. Otherwise, uses a default value of 34 psu.'),
        'data_product_identifier': 'PRACSAL_L2'
    },
    'pH': {
        'long_name': 'Seawater pH',
        'comment': ('pH is a measurement of the concentration of hydrogen ions in a solution. pH ranges from acidic ' +
                    'to basic on a scale from 0 to 14 with 7 being neutral.'),
        'standard_name': 'sea_water_ph_reported_on_total_scale',
        'data_product_identifier': 'PHWATER_L2',
        'units': '1',
        '_FillValue': np.nan,
        'ancillary_variables': ('blank_refrnc_434, blank_signal_434, blank_refrnc_578, blank_signal_578, ' +
                                'reference_434, signal_434, reference_578, signal_578, thermistor_temperature_start, ' +
                                'thermistor_temperature_end, salinity')
    }
}
