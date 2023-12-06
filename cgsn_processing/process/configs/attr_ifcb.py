#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ifcb
@file cgsn_processing/process/configs/attr_ifcb.py
@author Paul Whelan
@brief Attributes for the IFCB variables
"""
import numpy as np
from cgsn_processing.process.common import FILL_INT

IFCB = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Data from the Imaging Flow Cytobot instrument from McLane Labs',
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

    'sampleNumber': {
        'long_name': 'Sample Number of current IFCB deployment',
        'standard_name': 'sample_number',
        'processing_level': 'parsed',
        'comment': 'Sample number since beginning of IFCB deployment'
    },

    'sampleType': {
        'long_name': 'Sample type',
        'standard_name': 'sample_type',
        'processing_level': 'parsed',
        'comment': 'Type of sample being run: Normal, beads, '
    },

    'triggerCount': {
        'long_name': 'Trigger count',
        'standard_name': 'trigger_count',
        'processing_level': 'parsed',
        'comment': 'Number of qualifying images detected in sample'
    },

    'roiCount': {
        'long_name': 'Image count',
        'standard_name': 'roi_count',
        'processing_level': 'parsed',
        'comment': 'Count of raw optical images in sample'
    },

    'humidity': {
        'long_name': 'Relative humidity',
        'standard_name': 'humidity',
        'units': 'percent',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Relative humidity'
    },

    'temperature': {
        'long_name': 'Temperature in degrees celsius',
        'standard_name': 'temperature',
        'units': 'degrees_Celsius',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Temperature in degrees celsius'
    },

    'runTime': {
        'long_name': 'Run time',
        'standard_name': 'run_time',
        'units': 'seconds',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Run time of sample in seconds'
    },

    'inhibitTime': {
        'long_name': 'Inhibit time',
        'standard_name': 'inhibit_time',
        'units': 'seconds',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Analysis time during which samples do not trigger'
    },

    'pump1State': {
        'long_name': 'Pump 1 state',
        'standard_name': 'pump1_state',
        'units': 'boolean',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Logical on/off state'
    },

    'pump2State': {
        'long_name': 'Pump 2 state',
        'standard_name': 'pump2_state',
        'units': 'boolean',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Logical on/off value'
    },

    'PMTAhighVoltage': {
        'long_name': 'Photomultiplier A high voltage',
        'standard_name': 'pmta_high_voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'High voltage level at photomultiplier A'
    },

    'PMTBhighVoltage': {
        'long_name': 'Photomultiplier A high voltage',
        'standard_name': 'pmtb_high_voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'High voltage level at photomultiplier B'
    },

    'Alt_FlashlampControlVoltage': {
        'long_name': 'Alternate flash lamp control voltage',
        'standard_name': 'alt_flashlamp_control_voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Control voltage at alternate flash lamp'
    },

    'pumpDriveVoltage': {
        'long_name': 'Pump drive voltage',
        'standard_name': 'pump_drive_voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Voltage at pump drive'
    },

    'altPMTAHighVoltage': {
        'long_name': 'Alternate photomultiplier A high voltage',
        'standard_name': 'alt_pmta_high_voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'High voltage level at alternate photomultiplier A'
    },

    'altPMTBHighVoltage': {
        'long_name': 'Alternate photomultiplier B high voltage',
        'standard_name': 'alt_pmtb_high_voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'High voltage level at alternate photomultiplier B'
    },

    'syringeSamplingSpeed': {
        'long_name': 'Syringe sampling speed',
        'standard_name': 'syringe_sampling_speed',
        'units': 'min syringe-1',
        '_FillValue': FILL_INT,
        # '_FillValue': np.nan,
        'processing_level': 'parsed',
        'comment': 'Syringe sampling speed in min/syringe'
    },

    'syringeOffset': {
        'long_name': 'Syringe offset',
        'standard_name': 'syringe_offset',
        'units': '?',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Offset in time? of syringe in ?'
    },

    'NumberSyringesToAutoRun': {
        'long_name': 'Number of syringes to auto-run',
        'standard_name': 'number_syringes_to_autorun',
        'units': 'counts',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Count of syringes to automatically run'
    },

    'SyringeSampleVolume': {
        'long_name': 'Syringe sample volume',
        'standard_name': 'syringe_sample_volume',
        'units': 'ml',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Sample volume of syringe in ml'
    },

    'altSyringeSampleVolume': {
        'long_name': 'Alternate syringe sample volume',
        'standard_name': 'alt_syringe_sample_volume',
        'units': 'ml',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Sample volume of alternate syringe in ml'
    },

    'sampleVolume2skip': {
        'long_name': 'sample volume to skip',
        'standard_name': 'sample_volume_to_skip',
        'units': 'ml',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Amount of sample volume to skip processing'
    },

    'focusMotorSmallStep_ms': {
        'long_name': 'Focus motor small step',
        'standard_name': 'focus_motor_small_step_ms',
        'units': '?',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Focus motor small step'
    },

    'focusMotorLargeStep_ms': {
        'long_name': 'Focus motor large step',
        'standard_name': 'focus_motor_large_step_ms',
        'units': '?',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Focus motor large step'
    },

    'laserMotorSmallStep': {
        'long_name': 'Laser motor small step',
        'standard_name': 'laser_motor_small_step',
        'units': '?',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Laser motor small step'
    },

    'laserMotorLargeStep': {
        'long_name': 'Laser motor large step',
        'standard_name': 'laser_motor_large_step',
        'units': '?',
        '_FillValue': FILL_INT,
        'processing_level': 'parsed',
        'comment': 'Laser motor large step'
    }
}
