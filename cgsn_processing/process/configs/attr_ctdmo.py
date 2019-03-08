#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_imm
@file cgsn_processing/process/configs/attr_ctdmo.py
@author Christopher Wingard
@brief Attributes for dataset variables for instruments that are hosted via the inductive modem (IMM)
"""
import numpy as np

CTDMO = {
    # global attributes
    'global': {
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
        'comment': 'Derived from the SBE 37-IM MicroCAT internal clock.'
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

CTD = {
    # data from the status header
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
    'main_battery': {
        'long_name': 'Main Battery Voltage',
        'units': 'V',
        '_FillValue': np.nan
    },
    'lithium_battery': {
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
    'memory_free': {
        'long_name': 'Number of Free Samples',
        'comment': 'Number of free samples available for recording, representing the memory available in the unit',
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'pressure_range': {
        'long_name': 'Pressure Range',
        'comment': 'Pressure sensor range reported as the absolute pressure (atmospheric + in situ pressure)',
        'units': 'psi',
        '_FillValue': -9999999,
    },

    # Raw values reported by the SBE37, units are all in counts
    'raw_conductivity': {
        'long_name': 'Raw Conductivity',
        'units': 'counts',
        'comment': 'Raw conductivity measurement reported in counts.',
        'data_product_identifier': 'CONDWAT_L0',
        '_FillValue': -9999999,
    },
    'raw_temperature': {
        'long_name': 'Raw Temperature',
        'units': 'counts',
        'comment': 'Raw temperature measurement reported in counts.',
        'data_product_identifier': 'TEMPWAT_L0',
        '_FillValue': -9999999,
    },
    'raw_pressure': {
        'long_name': 'Raw Pressure',
        'units': 'counts',
        'comment': 'Raw pressure measurement reported in counts.',
        'data_product_identifier': 'PRESWAT_L0',
        '_FillValue': -9999999,
    },

    # measurements derived from the raw values listed above, as well as the latitude and longitude
    'conductivity': {
        'long_name': 'Seawater Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1',
        'comment': ('Seawater conductivity refers to the ability of seawater to conduct electricity. The presence of ',
                    'ions, such as salt, increases the electrical conducting ability of seawater. As such, ',
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of seawater.'),
        'data_product_identifier': 'CONDWAT_L1',
        'ancillary_variables': 'raw_conductivity',
        '_FillValue': np.nan
    },
    'temperature': {
        'long_name': 'Seawater Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius',
        'comment': 'Seawater temperature at the sensor.',
        'data_product_identifier': 'TEMPWAT_L1',
        'ancillary_variables': 'raw_temperature',
        '_FillValue': np.nan
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the column ',
                    'of seawater above it. It is calculated by subtracting one standard atmosphere from the absolute '
                    'pressure at the sensor to remove the weight of the atmosphere on top of the water column. The ',
                    'pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1',
        'ancillary_variables': 'pressure_range, raw_pressure',
        '_FillValue': np.nan
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of seawater. ',
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of ',
                    'seawater and adjusted for temperature and pressure. It is approximately equivalent to Absolute ',
                    'Salinity (the mass fraction of dissolved salt in seawater) but they are not interchangeable.'),
        'data_product_identifier': 'PRACSAL_L2',
        'ancillary_variables': 'conductivity, temperature, pressure',
        '_FillValue': np.nan
    },
    'density': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'comment': ('Seawater Density is defined as mass per unit volume and is calculated from the conductivity, ',
                    'temperature and depth of a seawater sample using the TEOS-10 equation.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, pressure, temperature, salinity',
        '_FillValue': np.nan
    }
}
