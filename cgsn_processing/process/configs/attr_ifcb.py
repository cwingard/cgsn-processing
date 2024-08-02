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
    'global': {
        'title': 'Data from the Imaging Flow Cytobot instrument from McLane Labs',
        'summary': (
            'Measures and generates images of particles in-flow using the McLane Labs '
            'Imaging FlowCytobot sensor.'
        )
    },
    # parsed (raw) variables and attributes
    'sampleNumber': {
        'long_name': 'Sample Number of current IFCB deployment',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Sample number since beginning of IFCB deployment'
    },
    'sampleType': {
        'long_name': 'Sample type',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Type of sample being run: Normal, beads, '
    },
    'triggerCount': {
        'long_name': 'Trigger count',
        'units': 'counts',
        'comment': 'Number of qualifying images detected in sample'
    },
    'roiCount': {
        'long_name': 'Image count',
        'units': 'counts',
        'comment': 'Count of raw optical images in sample'
    },
    'humidity': {
        'long_name': 'Relative humidity',
        'standard_name': 'relative_humidity',
        'units': 'percent',
        '_FillValue': FILL_INT,
        'comment': 'Relative humidity'
    },
    'temperature': {
        'long_name': 'Temperature in degrees celsius',
        'standard_name': 'temperature',
        'units': 'degrees_Celsius',
        '_FillValue': FILL_INT,
        'comment': 'Temperature in degrees celsius'
    },
    'runTime': {
        'long_name': 'Run time',
        'units': 'seconds',
        '_FillValue': FILL_INT,
        'comment': 'Run time of sample in seconds'
    },
    'inhibitTime': {
        'long_name': 'Inhibit time',
        'units': 'seconds',
        '_FillValue': FILL_INT,
        'comment': 'Analysis time during which samples do not trigger'
    },
    'pump1State': {
        'long_name': 'Pump 1 state',
        'units': 'boolean',
        'comment': 'Logical on/off state'
    },
    'pump2State': {
        'long_name': 'Pump 2 state',
        'units': 'boolean',
        'comment': 'Logical on/off state'
    },
    'PMTAhighVoltage': {
        'long_name': 'Photomultiplier A high voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'comment': 'High voltage level at photomultiplier A'
    },
    'PMTBhighVoltage': {
        'long_name': 'Photomultiplier B high voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'comment': 'High voltage level at photomultiplier B'
    },
    'Alt_FlashlampControlVoltage': {
        'long_name': 'Alternate flash lamp control voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'comment': 'Control voltage at alternate flash lamp'
    },
    'pumpDriveVoltage': {
        'long_name': 'Pump drive voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'comment': 'Voltage at pump drive'
    },
    'altPMTAHighVoltage': {
        'long_name': 'Alternate photomultiplier A high voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'comment': 'High voltage level at alternate photomultiplier A'
    },
    'altPMTBHighVoltage': {
        'long_name': 'Alternate photomultiplier B high voltage',
        'units': 'volts',
        '_FillValue': FILL_INT,
        'comment': 'High voltage level at alternate photomultiplier B'
    },
    'syringeSamplingSpeed': {
        'long_name': 'Syringe sampling speed',
        'units': 'min syringe-1',
        '_FillValue': FILL_INT,
        # '_FillValue': np.nan,
        'comment': 'Syringe sampling speed in min/syringe'
    },
    'syringeOffset': {
        'long_name': 'Syringe offset',
        # 'units': '', deliberately left blank, no units for this value
        '_FillValue': FILL_INT,
        'comment': 'Offset in time? of syringe in ?'
    },
    'NumberSyringesToAutoRun': {
        'long_name': 'Number of syringes to auto-run',
        'units': 'counts',
        '_FillValue': FILL_INT,
        'comment': 'Count of syringes to automatically run'
    },
    'SyringeSampleVolume': {
        'long_name': 'Syringe sample volume',
        'units': 'ml',
        '_FillValue': FILL_INT,
        'comment': 'Sample volume of syringe in ml'
    },
    'altSyringeSampleVolume': {
        'long_name': 'Alternate syringe sample volume',
        'units': 'ml',
        '_FillValue': FILL_INT,
        'comment': 'Sample volume of alternate syringe in ml'
    },
    'sampleVolume2skip': {
        'long_name': 'sample volume to skip',
        'units': 'ml',
        '_FillValue': FILL_INT,
        'comment': 'Amount of sample volume to skip processing'
    },
    'focusMotorSmallStep_ms': {
        'long_name': 'Focus motor small step',
        '_FillValue': FILL_INT,
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Focus motor small step'
    },
    'focusMotorLargeStep_ms': {
        'long_name': 'Focus motor large step',
        # 'units': '', deliberately left blank, no units for this value
        '_FillValue': FILL_INT,
        'comment': 'Focus motor large step'
    },
    'laserMotorSmallStep_ms': {
        'long_name': 'Laser motor small step',
        # 'units': '', deliberately left blank, no units for this value
        '_FillValue': FILL_INT,
        'comment': 'Laser motor small step'
    },
    'laserMotorLargeStep_ms': {
        'long_name': 'Laser motor large step',
        # 'units': '', deliberately left blank, no units for this value
        '_FillValue': FILL_INT,
        'comment': 'Laser motor large step'
    }
}
