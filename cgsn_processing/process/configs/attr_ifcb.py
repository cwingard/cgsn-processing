#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_ifcb
@file cgsn_processing/process/configs/attr_ifcb.py
@author Paul Whelan
@brief Attributes for the IFCB variables
"""
from cgsn_processing.process.common import FILL_INT

HDR = {
    'global': {
        'title': 'HDR Data from the Imaging FlowCytobot (IFCB)',
        'summary': ('Header (instrument settings, as well as a key to the format of the .adc file) data from the '
                    'Imaging FlowCytobot (IFCB) sensor produced by McLane Research Laboratories. The IFCB is an '
                    'in-situ automated submersible imaging flow cytometer that generates images of particles in-flow '
                    'taken from the aquatic environment.'),
    },
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
        'units': 'percent',
        '_FillValue': FILL_INT,
        'comment': 'Humidity internal to the instrument'
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

ADC = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'ADC Data from the Imaging FlowCytobot (IFCB)',
        'summary': ('Analog-to-digital (ADC) converter data from sensors for each event, and location pointers for '
                    'each event''s image data from the Imaging FlowCytobot (IFCB) sensor produced by McLane '
                    'Research Laboratories. The IFCB is an in-situ automated submersible imaging flow cytometer that '
                    'generates images of particles in-flow taken from the aquatic environment.'),
    },
    # parsed (raw) variables and attributes
    'triggerNumber': {
        'long_name': 'Trigger Number of image within current sample',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Trigger number within current IFCB sample'
    },
    'ADCtime': {
        'long_name': 'ADC time',
        'units': 's',
        'comment': 'offset time within sample of image detection'
        },
    'PMTA': {
        'long_name': 'PMTA',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube A value'
        },
    'PMTB': {
        'long_name': 'PMTB',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube B value'
        },
    'PMTC': {
        'long_name': 'PMTC',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube C value'
        },
    'PMTD': {
        'long_name': 'PMTD',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'photomultiplier tube D value'
        },
    'PeakA': {
        'long_name': 'Peak A',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube A'
        },
    'PeakB': {
        'long_name': 'Peak B',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube B'
        },
    'PeakC': {
        'long_name': 'Peak C',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube C'
        },
    'PeakD': {
        'long_name': 'Peak D',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Peak value of image for photomultiplier tube D'
        },
    'TimeOfFlight': {
        'long_name': 'Time Of Flight',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'GrabTimeStart': {
        'long_name': 'Grab Time Start',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'GrabTimeEnd': {
        'long_name': 'Grab Time End',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'RoiX': {
        'long_name': 'Image X Coordinate',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'RoiY': {
        'long_name': 'Image Y Coordinate',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'RoiWidth': {
        'long_name': 'Image Width',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'RoiHeight': {
        'long_name': 'Image Height',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'StartByte': {
        'long_name': 'Start byte in ROI file',
        # 'units': '', deliberately left blank, no units for this value
        'comment': 'Offset of image within corresponding ROI file'
        },
    'ComparatorOut': {
        'long_name': 'ComparatorOut',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'StartPoint': {
        'long_name': 'StartPoint',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'SignalLength': {
        'long_name': 'Signal Length',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'Status': {
        'long_name': 'Status',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'RunTime': {
        'long_name': 'Run Time',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        },
    'InhibitTime': {
        'long_name': 'Inhibit Time',
        # 'units': '', deliberately left blank, no units for this value
        'comment': ''
        }
}
