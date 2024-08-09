#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_common
@file cgsn_processing/process/configs/attr_common.py
@author Christopher Wingard
@brief Common set of attributes shared by all (or most) datasets, setting
    global and standardized variables and their attributes to minimize
    code redundancy.
"""
import numpy as np

SHARED = {
    'global': {
        'project': 'NSF Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN) and the Endurance Array (EA)',
        'acknowledgement': 'National Science Foundation',
        'references': 'https://oceanobservatories.org',
        'creator_name': 'NSF Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'https://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.7'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        # units set via encoding in the to_netcdf method (see update_dateset in cgsn_processing/process/common.py)
        'axis': 'T',
        'comment': ('Derived from either the DCL data logger GPS referenced clock, or the internal instrument clock. '
                    'For instruments attached to a DCL, the instrument''s internal clock can be cross-compared to '
                    'the GPS clock to determine the internal clock''s offset and drift.')
    },
    'sensor_time': {
        'long_name': 'Sensor Time',
        'standard_name': 'time',
        # units set via encoding in the to_netcdf method (see update_dateset in cgsn_processing/process/common.py)
        'comment': ('Date and time from the sensor''s internal clock. It is expected that this value will drift from '
                    'the true time by some amount over the course of a deployment. Cross-comparisons to GPS based '
                    'clocks will be required to account for any offset and drift in the sensor.'),
    },
    'station_name': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Name',
        'standard_name': 'platform_name'
    },
    'lon': {
        'long_name': 'Deployment Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Deployment Latitude',
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
        'comment': ('Depth of the instrument, either from the deployment depth (e.g. 7 m for an NSIF) or the '
                    'instrument pressure record converted to depth.'),
        'positive': 'down',
        'axis': 'Z'
    }
}

CTD = {
    # We have multiple CTDs, all of which share the same set of variables, so we can define them here instead of
    # repeating them in each CTD module.
    'conductivity': {
        'long_name': 'Seawater Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1',
        'comment': ('Seawater conductivity refers to the ability of seawater to conduct electricity. The presence of '
                    'ions, such as salt, increases the electrical conducting ability of seawater. As such, '
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of '
                    'seawater.'),
        'data_product_identifier': 'CONDWAT_L1',
        '_FillValue': np.nan
    },
    'temperature': {
        'long_name': 'Seawater Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Seawater temperature at the sensor.',
        'data_product_identifier': 'TEMPWAT_L1',
        'ancillary_variables': 'raw_temperature',
        '_FillValue': np.nan
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the column '
                    'of seawater above it. It is calculated by subtracting one standard atmosphere from the absolute '
                    'pressure at the sensor to remove the weight of the atmosphere on top of the water column. The '
                    'pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': np.nan
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of seawater. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'seawater and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in seawater) but they are not interchangeable.'),
        'data_product_identifier': 'PRACSAL_L2',
        'ancillary_variables': 'conductivity, temperature, pressure',
        '_FillValue': np.nan
    },
    'density': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'comment': ('Seawater Density is defined as mass per unit volume and is calculated from the conductivity, '
                    'temperature and depth of a seawater sample using the TEOS-10 equation.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, pressure, temperature, salinity',
        '_FillValue': np.nan
    }
}

CO_LOCATED = {
    # co-located CTD data that gets merged into different instrument data streams prior to computing different
    # variables (e.g. dissolved oxygen, pH, etc.). Using a common set of attributes for the CTD data to minimize
    # redundancy.
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
    'ctd_density': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'comment': ('Seawater Density is defined as mass per unit volume and is calculated from the conductivity, '
                    'temperature and depth of a seawater sample using the TEOS-10 equation.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, pressure, temperature, salinity',
        '_FillValue': np.nan
    }
}
