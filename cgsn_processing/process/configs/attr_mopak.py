#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mopak
@file cgsn_processing/process/configs/attr_mopak.py
@author Christopher Wingard
@brief Attributes for the hydrogen gas variables
"""

MOPAK = {
    'global': {
        'title': 'Mooring 3D Accelerometer Data collected in bursts at 10 Hz',
        'summary': 'Records the motion and orientation of the mooring via a 3D accelerometer.',
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
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
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Name',
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'Derived from the file start time and the timer data',
        'ancillary_variables': 'timer'
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
    'acceleration_x': {
        'long_name': 'X-axis Acceleration Vector',
        'units': 'gravity',
        'comment': ('This is a vector quantifying the direction and magnitude of the acceleration that the '
                    'mooring is exposed to. This quantity is fully temperature compensated and scaled into '
                    'physical units of g (1 g = 9.80665 m/sec^2). It is expressed in terms of the MOPAK’s '
                    'local coordinate system (in this case the X-axis).')
    },
    'acceleration_y': {
        'long_name': 'Y-axis Acceleration Vector',
        'units': 'gravity',
        'comment': ('This is a vector quantifying the direction and magnitude of the acceleration that the '
                    'mooring is exposed to. This quantity is fully temperature compensated and scaled into '
                    'physical units of g (1 g = 9.80665 m/sec^2). It is expressed in terms of the MOPAK’s '
                    'local coordinate system (in this case the Y-axis).')
    },
    'acceleration_z': {
        'long_name': 'Z-axis Acceleration Vector',
        'units': 'gravity',
        'comment': ('This is a vector quantifying the direction and magnitude of the acceleration that the '
                    'mooring is exposed to. This quantity is fully temperature compensated and scaled into '
                    'physical units of g (1 g = 9.80665 m/sec^2). It is expressed in terms of the MOPAK’s '
                    'local coordinate system (in this case the Z-axis).')
    },
    'angular_rate_x': {
        'long_name': 'X-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the rate of rotation of the mooring. This quantity is '
                    'is fully temperature compensated and scaled into units of radians/second. It is '
                    'expressed in terms of the MOPAK’s local coordinate system (in this case the X-axis) '
                    'in units of radians/second.')
    },
    'angular_rate_y': {
        'long_name': 'Y-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the rate of rotation of the mooring. This quantity is '
                    'is fully temperature compensated and scaled into units of radians/second. It is '
                    'expressed in terms of the MOPAK’s local coordinate system (in this case the Y-axis) '
                    'in units of radians/second.')
    },
    'angular_rate_z': {
        'long_name': 'Z-axis Angular Rate',
        'units': 'radians/s',
        'comment': ('This is a vector quantifying the rate of rotation of the mooring. This quantity is '
                    'is fully temperature compensated and scaled into units of radians/second. It is '
                    'expressed in terms of the MOPAK’s local coordinate system (in this case the Z-axis) '
                    'in units of radians/second.')
    },
    'magnetometer_x': {
        'long_name': 'X-axis Magnetometer',
        'units': 'gauss',
        'comment': ('This is a vector which gives the instantaneous magnetometer direction and magnitude. It '
                    'is fully temperature compensated and is expressed in terms of the MOPAK’s local '
                    'coordinate system (in this case the X-axis) in units of Gauss.')
    },
    'magnetometer_y': {
        'long_name': 'Y-axis Magnetometer',
        'units': 'gauss',
        'comment': ('This is a vector which gives the instantaneous magnetometer direction and magnitude. It '
                    'is fully temperature compensated and is expressed in terms of the MOPAK’s local '
                    'coordinate system (in this case the Y-axis) in units of Gauss.')
    },
    'magnetometer_z': {
        'long_name': 'Z-axis Magnetometer',
        'units': 'gauss',
        'comment': ('This is a vector which gives the instantaneous magnetometer direction and magnitude. It '
                    'is fully temperature compensated and is expressed in terms of the MOPAK’s local '
                    'coordinate system (in this case the Z-axis) in units of Gauss.')
    },
    'timer': {
        'long_name': 'Timer',
        'units': 's',
        'comment': ('The time, in seconds, since the system started up. This is a relative measure of time '
                    'that is used, along with the file start time, to calculate the time in seconds since '
                    '1970-01-01.')
    }
}
