#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_co2pro
@file cgsn_processing/process/configs/attr_co2pro.py
@author Christopher Wingard
@brief Attributes for the Pro-Oceanus pCO2-Pro CV variables
"""
CPHOX = {
    # global attributes
    'global': {
        'title': 'Sea-Bird Electronics Deep SeapHOx V2 Data',
        'summary': ('In-situ pH data from the Sea-Bird Electronics Deep SeapHOx V2 instrument. The SeapHOx is a '
                    'combined CTD, dissolved oxygen and pH sensor.'),
        'project': 'Ocean Observatories Initiative',
        'institution': 'OOI Endurance Array',
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
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'Derived from the GPS referenced clock used by DCL data logger'
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
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
    # variable attributes -- reported
    'serial_number': {
        'long_name': 'Serial Number',
        # 'units': '',    # deliberately left blank, no units for this value,
        'comment': 'Serial number of the SeapHOx instrument. Used to uniquely identify the instrument.'
    },
    'sensor_time': {
        'long_name': 'Sensor Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'comment': ('Internal SeapHOX clock date and time stamp, recorded when the instrument begins the measurement. '
                    'It is expected that this value will drift from the true time by some amount over the course of '
                    'a deployment. Cross-comparisons to other systems will be required to account for the offset '
                    'and drift.'),
    },
    'sample_number': {
        'long_name': 'Sample Number',
        'comment': 'Sample number from the SeapHOx instrument.',
        'units': 'count'
    },
    'error_flag': {
        'long_name': 'Error Flag',
        # 'units': '',    # deliberately left blank, no units for this value,
        'comment': ('Error flag from the SeapHOx instrument. A value of 0 indicates no error. At this time, the '
                    'meaning of other values is not known.'),
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Sea water temperature is the in situ temperature of the sea water.',
        'data_product_identifier': 'TEMPWAT_L1',
    },
    'seawater_ph': {
        'long_name': 'Sea Water pH, Total Scale',
        'standard_name': 'sea_water_ph_reported_on_total_scale',
        'units': '1',
        'comment': ('pH of the sea water, reported on the total scale. The pH is a measure of the acidity or '
                    'basicity of the sea water, where a pH of 7 is neutral, a pH less than 7 is acidic, and a pH '
                    'greater than 7 is basic.'),
        'data_product_identifier': 'PHWATER_L2'
    },
    'external_reference': {
        'long_name': 'External Reference Voltage',
        'units': 'V',
        'comment': ('External reference voltage from the SeapHOx instrument. This value is used to calculate the '
                    'pH of the sea water.')
    },
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable.'),
        'data_product_identifier': 'PRACSAL_L2',
        'ancillary_variables': 'conductivity, temperature, pressure'
    },
    'conductivity': {
        'long_name': 'Sea Water Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1',
        'comment': ('Sea water conductivity refers to the ability of seawater to conduct electricity. The presence '
                    'of ions, such as salt, increases the electrical conducting ability of seawater. As such, '
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of '
                    'seawater.'),
        'data_product_identifier': 'CONDWAT_L1'
    },
    'oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'units': 'mL L-1',
        'comment': ('Concentration of dissolved oxygen per unit volume, as measured by an optode oxygen sensor. '
                    'Computed on-board the sensor using internal calibration coefficients.'),
        'data_product_identifier': 'DOCONCS_L1'
    },
    'internal_humidity': {
        'long_name': 'Internal Humidity',
        'units': 'percent',
        'comment': 'Internal humidity of the SeapHOx instrument.'
    },
    'internal_temperature': {
        'long_name': 'Internal Temperature',
        'units': 'degree_Celsius',
        'comment': 'Internal temperature of the SeapHOx instrument.'
    },
    # variable attributes -- derived values
    'oxygen_molar_concentration': {
        'long_name': 'Dissolved Oxygen Molar Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'an optode oxygen sensor. Computed on-board the sensor using internal calibration coefficients.'),
        'data_product_identifier': 'DOCONCS_L1'
    },
    'oxygen_concentration_per_kg': {
        'long_name': 'Dissolved Oxygen per Unit Mass',
        'standard_name': 'moles_of_oxygen_per_unit_mass_in_sea_water',
        'units': 'umol kg-1',
        'comment': ('Concentration of dissolved oxygen per unit mass in the sea water, adjusted to the potential '
                    'density per directions outlined in the Sea-Bird Electronics SBE63 Manual.'),
        'data_product_identifier': 'DOXYGEN_L2'
    },
    'estimated_alkalinity': {
        'long_name': 'Estimated Alkalinity',
        'units': 'umol kg-1',
        'comment': ('Estimated alkalinity of the sea water, reported in umol/kg. The alkalinity is estimated using '
                    'the SeapHOx temperature and salinity data and an equation from Lee et al. (2006, '
                    'doi:10.1029/2006GL027207.')
    },
    'estimated_ph': {
        'long_name': 'Estimated pH, Total Scale',
        'units': '1',
        'comment': ('Estimated pH of the sea water, reported on the total scale. The pH is a measure of the acidity '
                    'or basicity of the sea water, where a pH of 7 is neutral, a pH less than 7 is acidic, and a pH '
                    'greater than 7 is basic. The pH is estimated using the SeapHOx oxygen and temperature data and '
                    'an equation from Juranek et al. (2011, doi:10.1029/2011GL048580).')
    }
}
