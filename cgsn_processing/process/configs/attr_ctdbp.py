#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ctdbp
@file cgsn_processing/process/configs/attr_ctdbp.py
@author Christopher Wingard
@brief Attributes for the CTDBP variables
"""
import numpy as np

GLOBAL = {
    # global attributes
    'global': {
        'title': 'CTD',
        'summary': ('CTD Data'),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
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

CTDBP = {
    # attributes for all instances of the CTDBP, regardless of system used to log data or instrument(s) attached.
    # --> reported values
    'sensor_time': {
        'long_name': 'CTD Date and Time',
        'standard_name': 'time',
        'comment': ('Internal CTD clock date and time stamp, recorded when the instrument begins the measurement. It ' +
                    'is expected that this value will drift from the true time by some degree over the course of ' +
                    'a deployment. Cross-comparisons to other systems will be required to account for the offset ' +
                    'and drift.'),
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'calendar': 'gregorian'
    },
    'conductivity': {
        'long_name': 'Seawater Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1',
        'comment': ('Seawater conductivity refers to the ability of seawater to conduct electricity. The presence of ' +
                    'ions, such as salt, increases the electrical conducting ability of seawater. As such, ' +
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of ' +
                    'seawater.'),
        'data_product_identifier': 'CONDWAT_L1',
        '_FillValue': np.nan
    },
    'temperature': {
        'long_name': 'Seawater Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius',
        'comment': 'Seawater temperature at the sensor.',
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': np.nan
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': (
                    'Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the column ' +
                    'of seawater above it. It is calculated by subtracting one standard atmosphere from the absolute ' +
                    'pressure at the sensor to remove the weight of the atmosphere on top of the water column. The ' +
                    'pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': np.nan
    },
    # --> derived values
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of seawater. ' +
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of ' +
                    'seawater and adjusted for temperature and pressure. It is approximately equivalent to Absolute ' +
                    'Salinity (the mass fraction of dissolved salt in seawater) but they are not interchangeable.'),
        'data_product_identifier': 'PRACSAL_L2',
        'ancillary_variables': 'conductivity, temperature, pressure',
        '_FillValue': np.nan
    },
    'density': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'comment': ('Seawater Density is defined as mass per unit volume and is calculated from the conductivity, ' +
                    'temperature and depth of a seawater sample using the TEOS-10 equation.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, pressure, temperature, salinity',
        '_FillValue': np.nan
    },

    # attributes associated with the status message output from a CTDBP connected to an inductive modem (IMM)
    'status_time': {
        'long_name': 'Status Update Time',
        '_FillValue': np.nan,
        'units': 'seconds since 1970-01-01 00:00:00 0:00',
        'calendar': 'gregorian',
        'comment': 'Date and time the CTD status was queried.'
    },
    'serial_number': {
        'long_name': 'Serial Number',
        '_FillValue': -9999999,
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'main_battery_voltage': {
        'long_name': 'Main Battery Voltage',
        'units': 'V',
        '_FillValue': np.nan
    },
    'lithium_battery_voltage': {
        'long_name': 'Lithium Battery Voltage',
        'units': 'V',
        '_FillValue': np.nan
    },
    'samples_recorded': {
        'long_name': 'Number of Samples Recorded',
        'comment': 'Number of samples recorded during the deployment',
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'sample_slots_free': {
        'long_name': 'Number of Free Sample Slots Remaining',
        'comment': 'Number of free samples available for recording, representing the memory available in the unit',
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'main_current': {},
    'pump_current': {},
    'oxy_current': {},
    'eco_current': {},

    # attributes associated with a CTDBP hosted by a DCL
    'time_offset': {
        'long_name': 'Internal Clock Offset',
        'comment': ('Difference between the internal CTD clock and the external GPS-based data logger clock. Can ' +
                    'be used to determine instrument clock offset and drift over the course of a deployment'),
        'units': 'seconds',
        'ancillary_variables': 'ctd_time, time'
    },

    # Values recorded by the different CTDBP configurations
    # --> with an Aanderaa Optode (DOSTA)
    'oxygen_concentration': {
        'units': 'umol/L'
    },

    # --> with WET Labs ECO Triplet (FLORT)
    'raw_backscatter': {
        'units': 'counts'
    },
    'raw_chlorophyll': {
        'units': 'counts'
    },
    'raw_cdom': {
        'units': 'counts'
    },

    # --> with an Aanderaa Optode (DOSTA) and a WET Labs FLNTU (FLORD) (IMM Hosted)
    'raw_oxy_calphase': {},
    'raw_oxy_temp': {},
    'raw_chlorophyll': {},
    'raw_backscatter': {}
}
