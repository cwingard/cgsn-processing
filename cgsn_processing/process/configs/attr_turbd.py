#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_turbd
@file cgsn_processing/process/configs/attr_turbd.py
@author Paul Whelan
@brief Attributes for the TURBD variables
"""
import numpy as np
from cgsn_processing.process.common import FILL_INT

TURBD = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Seapoint Turbidity sensor Data',
        'summary': 'Moored turbidity time series data sets.',
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
        'comment': ('Derived from either the DCL data logger GPS referenced clock, or the internal instrument clock '
                    'if this is an IMM hosted instrument. For instruments attached to a DCL, the instrument''s '
                    'internal clock can be cross-compared to the GPS clock to determine the internal clock''s '
                    'offset and drift.')
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
    # attributes for all instances of the CTDBP, regardless of system used to log data or instrument(s) attached.
    # --> reported values
    'sensor_time': {
        'long_name': 'Turbidity sensor Date and Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01 00:00:00.00',
        'comment': ('Internal sensor clock date and time stamp, recorded when the instrument begins the measurement. It '
                    'is expected that this value will drift from the true time by some amount over the course of '
                    'a deployment. Cross-comparisons to other systems will be required to account for the offset '
                    'and drift.'),
        'calendar': 'gregorian'
    },
    'raw_signal_turbidity': {
        'long_name': 'Raw turbidity value',
        'standard_name': 'sea_water_turbidity',
        'units': 'NTU',
        'comment': ('Turbidity is a dimensionless quantity which is expressed in NTU '
                    '(Nephelometric Turbidity Units). Turbidity expressed in NTU is the proportion '
                    'of white light scattered back to a transceiver by the particulate load in a '
                    'body of water, represented on an arbitrary scale referenced against measurements '
                    'made in the laboratory on aqueous suspensions of formazine beads.'),
        'data_product_identifier': 'TURBWAT_L1',
        '_FillValue': np.nan
    },
}
