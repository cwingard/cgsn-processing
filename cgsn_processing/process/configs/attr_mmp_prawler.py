#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mmp_prawler
@file cgsn_processing/process/configs/attr_mmp_prawler.py
@author Paul Whelan
@brief Attributes for the MMP Prawler variables
"""

PRAWLER = {
    'global': {
        'title': 'Prawler MMP Data',
        'summary': 'Prawler profiler engineering and science profile data ',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN) and the Endurance Array (EA)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.7'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': 'Mooring deployment id'
    },    
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'instrument time'
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
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
    'depth': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'coordinates': 'time',
        'positive': 'down'
    },
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'coordinates': 'time',
        'positive': 'down'
        },
    'temperature': {
        'long_name': 'Sea Surface Temperature',
        'standard_name': 'sea_surface_temperature',
        'units': 'degrees_Celsius',
        'coordinates': 'time'
    },
    'conductivity': {
        'long_name': 'Sea Surface Conductivity',
        'standard_name': 'sea_surface_conductivity',
        'units': 'S m-1',
        'coordinates': 'time'
    },
    'optode_temperature': {
        'long_name': 'Optode Temperature',
        'units': 'degrees_Celsius',
        'coordinates': 'time'
    },
    'optode_dissolved_oxygen': {
        'long_name': 'Optode dissolved oxygen',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'coordinates': 'time'
    },
    'flu_beta_count': {
        'long_name': 'Fluorometer beta count',
        'units': 'counts',
        'coordinates': 'time'
    },
    'flu_chl_count': {
        'long_name': 'Fluorometer chlorophyll a count',
        'units': 'counts',
        'coordinates': 'time'
    },
    'flu_cdom_count': {
        'long_name': 'Fluorometer CDOM count',
        'units': 'counts',
        'coordinates': 'time'
    },
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'mg L-1'
    },
    'fluorometric_cdom': {
        'long_name': 'Fluorometric CDOM',
        'units': 'ppm'
    },
    'beta_700': {
        'long_name': 'Volume Scattering Function at 700 nm',
        'standard_name': 'volume_scattering_function_of_radiative_flux_in_sea_water',
        'units': 'm-1 sr-1'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'bback': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'units': 'm-1'
    }
}

PRAWLER_NO_FLORT = {
    'global': {
        'title': 'Prawler MMP Data',
        'summary': 'Prawler profiler engineering and science profile data ',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN) and the Endurance Array (EA)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeries',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.7'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': 'Mooring deployment id'
    },    
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'instrument time'
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Identifier'
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
    'depth': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'coordinates': 'time',
        'positive': 'down'
    },
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'coordinates': 'time',
        'positive': 'down'
        },
    'temperature': {
        'long_name': 'Sea Surface Temperature',
        'standard_name': 'sea_surface_temperature',
        'units': 'degrees_Celsius',
        'coordinates': 'time'
    },
    'conductivity': {
        'long_name': 'Sea Surface Conductivity',
        'standard_name': 'sea_surface_conductivity',
        'units': 'S m-1',
        'coordinates': 'time'
    },
    'optode_temperature': {
        'long_name': 'Optode Temperature',
        'units': 'degrees_Celsius',
        'coordinates': 'time'
    },
    'optode_dissolved_oxygen': {
        'long_name': 'Optode dissolved oxygen',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'coordinates': 'time'
    }
}

PRAWLER_SUMMARY = {
}
PRAWLER_ENG = {
}
PRAWLER_SCI = {
}
