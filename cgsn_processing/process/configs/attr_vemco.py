#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_vemco
@file cgsn_processing/process/configs/attr_vemco.py
@author Christopher Wingard
@brief Attributes for the Vemco VR2C Acoustic Fish Tag Receiver
"""
VEMCO = {
    # global attributes
    'global': {
        'title': 'Vemco VR2C Acoustic Fish Tag Receiver',
        'summary': ('The Vemco VR2C Acoustic Fish Tag Receiver is a moored receiver that listens for acoustic '
                    'pings from tagged fish using coded tags operating at 69 kHz. The receiver is deployed '
                    'on a mooring and listens for tagged fish within a 500 m radius.'),
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
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.000Z',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'Derived from the data logger''s GPS conditioned, real-time clock'
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
    },
    # status and tag detection attributes
    'sensor_time': {
        'long_name': 'VR2C Date and Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.000Z',
        'comment': ('Internal Vemco VR2C clock date and time stamp, recorded when the instrument is polled. It '
                    'is expected that this value will drift from the true time by some amount over the course of '
                    'a deployment. Cross-comparisons to the DCL GPS based will be required to account for any offset '
                    'and drift.'),
        'calendar': 'gregorian'
    },
    'clock_offset': {
        'long_name': 'Clock Offset',
        'comment': 'Difference between the VR2C receiver''s internal clock and the GPS based DCL Date and Time.',
        'units': 'seconds'
    },
    'serial_number': {
        'long_name': 'Serial Number',
        'comment': 'Unique identifier for the VR2C receiver',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sequence': {
        'long_name': 'Sequence Number',
        'comment': 'Sequence number of the VR2C status or tag detections, increments from 000 to 999.',
        'units': 'counts'
    },
    'detection_count': {
        'long_name': 'Detection Count',
        'comment': 'Number of detections recorded since the last status message',
        'units': 'counts'
    },
    'ping_count': {
        'long_name': 'Ping Count',
        'comment': 'Number of pings recorded since the last status message',
        'units': 'counts'
    },
    'line_voltage': {
        'long_name': 'Line Voltage',
        'comment': 'Voltage of the external power line',
        'units': 'V'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': 'Voltage of the internal battery.',
        'units': 'V'
    },
    'battery_usage': {
        'long_name': 'Battery Usage',
        'comment': 'Percentage of battery life remaining.',
        'units': 'percent'
    },
    'current_consumption': {
        'long_name': 'Current Consumption',
        'comment': 'Current consumption of the receiver.',
        'units': 'mA'
    },
    'internal_temperature': {
        'long_name': 'Internal Temperature',
        'comment': 'Internal temperature of the receiver.',
        'units': 'degrees_Celsius'
    },
    'detection_memory_usage': {
        'long_name': 'Detection Memory Usage',
        'comment': 'Percentage of detection memory used.',
        'units': 'percent'
    },
    'raw_memory_usage': {
        'long_name': 'Raw Memory Usage',
        'comment': 'Percentage of raw memory used.',
        'units': 'percent'
    },
    'tilt_x': {
        'long_name': 'Tilt X',
        'comment': ('Tilt in the x-axis recorded in gravity units. If the X-axis is +1 and the Y and Z axes are 0, '
                    'the VR2C is vertical with the hydrophone pointing upwards.'),
        'units': 'gravity'
    },
    'tilt_y': {
        'long_name': 'Tilt Y',
        'comment': ('Tilt in the y-axis recorded in gravity units. If the X-axis is +1 and the Y and Z axes are 0, '
                    'the VR2C is vertical with the hydrophone pointing upwards.'),
        'units': 'gravity'
    },
    'tilt_z': {
        'long_name': 'Tilt Z',
        'comment': ('Tilt in the z-axis recorded in gravity units. If the X-axis is +1 and the Y and Z axes are 0, '
                    'the VR2C is vertical with the hydrophone pointing upwards.'),
        'units': 'gravity'
    },
    'code_space': {
        'long_name': 'Code Space',
        'comment': 'Code space used by the tag. Varies by manufacturer.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'tag_id': {
        'long_name': 'Tag ID',
        'comment': 'Unique identifier for the tag',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'sensor_data': {
        'long_name': 'Sensor Data',
        'comment': 'A2D data from the tag sensor, if present',
        'units': 'counts',
        '_FillValue': -9999999
    }
}
