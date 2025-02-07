#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ifcb_adc
@file cgsn_processing/process/configs/attr_ifcb_adc.py
@author Paul Whelan
@brief Attributes for the IFCB ADC file variables
"""
import numpy as np

IFCB_ADC = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'ADC data from the Imaging Flow Cytobot instrument from McLane Labs',
        'summary': (
            'Measures and generates images of particles in-flow using the McLane Labs '
            'Imaging FlowCytobot sensor.'
        ),
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes, (CGSN)',
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
        'comment': ('Derived from the internal instrument clock.')
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('Mooring deployment longitude, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('Mooring deployment latitude, surveyed after deployment to determine the anchor location and '
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

    # parsed (raw) variables and attributes

    'triggerNumber': {
        'long_name': 'Trigger Number of image within current sample',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'Trigger number within current IFCB sample'
    },

    'ADCtime': {
        'long_name': 'ADC time',
        'units': 's',
        'comment': 'offset time within sample of image detection'
        },

    'PMTA': {
        'long_name': 'PMTA',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube A value'
        },

    'PMTB': {
        'long_name': 'PMTB',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube B value'
        },

    'PMTC': {
        'long_name': 'PMTC',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube C value'
        },

    'PMTD': {
        'long_name': 'PMTD',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube D value'
        },

    'PeakA': {
        'long_name': 'Peak A',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube A'
        },

    'PeakB': {
        'long_name': 'Peak B',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube B'
        },

    'PeakC': {
        'long_name': 'Peak C',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube C'
        },

    'PeakD': {
        'long_name': 'Peak D',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube D'
        },

    'TimeOfFlight': {
        'long_name': 'Time Of Flight',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'GrabTimeStart': {
        'long_name': 'Grab Time Start',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'GrabTimeEnd': {
        'long_name': 'Grab Time End',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'RoiX': {
        'long_name': 'Image X Coordinate',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'RoiY': {
        'long_name': 'Image Y Coordinate',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'RoiWidth': {
        'long_name': 'Image Width',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'RoiHeight': {
        'long_name': 'Image Height',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'StartByte': {
        'long_name': 'Start byte in ROI file',
#        'units': '', deliberately left blank, no units for this value
        'comment': 'Offset of image within corresponding ROI file'
        },

    'ComparatorOut': {
        'long_name': 'ComparatorOut',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'StartPoint': {
        'long_name': 'StartPoint',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'SignalLength': {
        'long_name': 'Signal Length',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'Status': {
        'long_name': 'Status',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'RunTime': {
        'long_name': 'Run Time',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        },

    'InhibitTime': {
        'long_name': 'Inhibit Time',
#        'units': '', deliberately left blank, no units for this value
        'comment': ''
        }

}
