#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_metbk
@file cgsn_processing/process/configs/attr_metbk.py
@author Christopher Wingard
@brief Attributes for the METBK variables
"""
import numpy as np

METBK = {
    'global': {
        'title': 'Bulk Meteorological (METBK) Measurements',
        'summary': ('Measures surface meteorology and provides the data required to compute '
                    'air-sea fluxes of heat, freshwater, and momentum.'),
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
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': ('Derived from the DCL data logger GPS referenced clock.')
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
    'barometric_pressure': {
        'long_name': 'Barometric Pressure',
        'standard_name': 'air_pressure',
        'units': 'mbar',
        'comment': ('Barometric Pressure is a measure of the weight of the column of air above the sensor. It is '
                    'also commonly referred to as atmospheric pressure.'),
        'data_product_identifier': 'BARPRES_L0',
        '_FillValue': np.nan
    },
    'relative_humidity': {
        'long_name': 'Relative Humidity',
        'standard_name': 'relative_humidity',
        'units': 'percent',
        'comment': ('Relative humidity is the ratio of the current absolute humidity to the highest possible '
                    'absolute humidity, which depends on the current air temperature.'),
        'data_product_identifier': 'RELHUMI_L1',
        '_FillValue': np.nan
    },
    'air_temperature': {
        'long_name': 'Air Temperature',
        'standard_name': 'air_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Air temperature refers to the temperature of the air surrounding the sensor; this is also '
                    'referred to as bulk temperature.'),
        'data_product_identifier': 'TEMPAIR_L1',
        '_FillValue': np.nan
    },
    'longwave_irradiance': {
        'long_name': 'Downwelling Longwave Irradiance',
        'standard_name': 'downwelling_longwave_flux_in_air',
        'units': 'W m-2',
        'comment': ('Downwelling longwave radiation flux at the surface. Significant sources of longwave radiation in '
                    'hydrologic applications include the atmosphere itself, and any clouds that may be present '
                    'locally in the atmosphere. Clouds usually have a higher heat content and higher temperature '
                    'than clear atmosphere, and therefore there is increased downwelling longwave radiation on '
                    'cloudy days'),
        'data_product_identifier': 'LONGIRR_L1',
        '_FillValue': np.nan
    },
    'precipitation_level': {
        'long_name': 'Precipitation Level',
        'standard_name': 'lwe_thickness_of_precipitation_amount',
        'units': 'mm',
        'comment': ('Rain gauge measurement. Values cycle from 0 to 50 mm as the water level rises and '
                    'then is siphoned off. To convert to rain rate, only positive increases greater than 0.25 mm '
                    'should be used.'),
        'data_product_identifier': 'PRECIPM_L1',
        '_FillValue': np.nan
    },
    'sea_surface_temperature': {
        'long_name': 'Sea Surface Temperature',
        'standard_name': 'sea_surface_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Sea surface temperature is the in-situ temperature of the seawater near the ocean surface.',
        'data_product_identifier': 'TEMPSRF_L1',
        '_FillValue': np.nan
    },
    'sea_surface_conductivity': {
        'long_name': 'Sea Surface Conductivity',
        'standard_name': 'sea_surface_conductivity',
        'units': 'S m-1',
        'comment': ('Sea surface conductivity refers to the ability of seawater to conduct electricity. The presence '
                    'of ions, such as salt, increases the electrical conducting ability of seawater. As such, '
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of '
                    'seawater measured near the sea surface.'),
        'data_product_identifier': 'CONDSRF_L1',
        '_FillValue': np.nan
    },
    'shortwave_irradiance': {
        'long_name': 'Downwelling Shortwave Irradiance',
        'standard_name': 'downwelling_shortwave_flux_in_air',
        'units': 'W m-2',
        'comment': ('Downwelling short-wave radiation at the surface has a component due to the direct solar beam, '
                    'and a diffuse component scattered from atmospheric constituents and reflected from clouds.'),
        'data_product_identifier': 'SHRTIRR_L1',
        '_FillValue': np.nan
    },
    'eastward_wind_velocity': {
        'long_name': 'Eastward Wind Velocity',
        'standard_name': 'eastward_wind',
        'units': 'm s-1',
        'comment': '"WINDAVG-VLE_L0',
        'data_product_identifier': 'Eastward wind velocity relative to magnetic North.',
        '_FillValue': np.nan
    },
    'northward_wind_velocity': {
        'long_name': 'Northward Wind Velocity',
        'standard_name': 'northward_wind',
        'units': 'm s-1',
        'comment': 'Northward wind velocity relative to magnetic North.',
        'data_product_identifier': '"WINDAVG-VLN_L0',
        '_FillValue': np.nan
    },
    # ---- derived values ----
    'sea_surface_salinity': {
        'long_name': 'Sea Surface Practical Salinity',
        'standard_name': 'sea_surface_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable.'),
        'data_product_identifier': 'SALSURF_L2',
        'ancillary_variables': 'sea_surface_conductivity, sea_surface_temperature',
        '_FillValue': np.nan
    },
    'sea_surface_density': {
        'long_name': 'Sea Surface In Situ Density',
        'standard_name': 'sea_surface_density',
        'units': 'kg m-3',
        'comment': ('Sea water density is the in situ density and is defined as mass per unit volume. It is '
                    'calculated from the conductivity, temperature and depth of a sea water sample.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, sea_surface_salinity, sea_surface_temperature',
        '_FillValue': np.nan
    }
}
