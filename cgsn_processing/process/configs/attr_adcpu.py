#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_adcpu
@file cgsn_processing/process/configs/attr_adcpu.py
@author Paul Whelan
@brief Attributes for the Nortek Aquadopp 2 (ADCPU)
"""
import numpy as np

ADCPU = {
    # global attributes
    'global': {
        'title': '3D Point Velocity Measurements from the Nortek Aquadopp 2',
        'summary': ('The Nortek Aquadopp 2  ' +
                    '...'),
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
        'units': 'seconds since 1970-01-01 00:00:00Z',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': 'Instrument reported date and time'
    },
    'cell_number': {
        'long_name': 'Cell number',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'Instrument reported cell number'
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
    'instrument_name': {
        'long_name': 'Instrument name',
        'comment': 'Name of the instrument in use',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'instrument_type': {
        'long_name': 'Instrument type',
        'comment': '0-Aquadopp 1-Aquadopp profiler 2-Signature',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'number_beams': {
        'long_name': 'Number Beams',
        'comment': 'Contains the number of beams used to calculate velocity data',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'number_cells': {
        'long_name': 'Number Cells',
        'comment': 'Contains the number of cells over which the Aquadopp 2 collects data',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'cell_size': {
        'long_name': 'Cell Size',
        'comment': 'Contains the depth of one cell length',
        'units': 'm'
    },
    'coordinate_system': {
        'long_name': 'Coordinate system used: 0-ENU, 1-XYZ, 2-BEAM',
        'comment': 'Index indicating the coordinate system in use',
        # 'units': '',     deliberately left blank, no units for this value
    },
    'blanking': {
        'long_name': 'Blank After Transmit Distance',
        'comment': ('Contains the blanking distance used by the Aquadopp 2 to allow the transmit circuits time '
                    'to recover before receive cycle begins'),
        'units': 'm'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': 'Voltage of either the internal battery pack or externally supplied power, whichever is greater.',
        'units': 'V'
    },
    'sound_speed': {
        'long_name': 'Speed of Sound',
        'comment': ('Estimated speed of sound derived internally by the VEL3D from the temperature sensor ' +
                    'measurements and an assumed constant salinity of 33 psu.'),
        'units': 'm s-1'
    },
    'heading': {
        'long_name': 'Heading',
        'comment': 'Measured heading of the VEL3D, uncorrected for magnetic declination.',
        'units': 'degrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'comment': 'Measured pitch of the VEL3D.',
        'units': 'degrees'
    },
    'roll': {
        'long_name': 'Roll',
        'comment': 'Measured roll of the VEL3D.',
        'units': 'degrees'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'comment': 'In-situ sea water temperature measured at the base of the transducer stalk.',
        'units': 'degrees_Celsius'
    },
    'error_code': {
        'long_name': 'Instrument Error Codes',
        'flag_masks': np.array([1, 2, 4, 8, 16, 64], dtype=np.uint8),
        'flag_meanings': ('compass_error measurement_error sensor_data_error tag_bit_error ' +
                          'flash_error ct_sensor_read_error'),
        'comment': 'Integer representation of the instrument error codes.'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'status_code': {
        'long_name': 'Instrument Status Codes',
        'flag_masks': np.array([1, 2, 4, 8, 48, 48, 48, 48, 192, 192, 192, 192], dtype=np.uint8),
        'flag_values': np.array([1, 2, 4, 8, 0, 16, 32, 48, 0, 64, 128, 192], dtype=np.uint8),
        'flag_meanings': ('orientation_down scaling_factor_0.1 pitch_out_of_range roll_out_of_range ' +
                          'wake_bad_power wake_break_received wake_power_applied wake_rtc_alarm ' +
                          'power_level_high power_level_1 power_level_2 power_level_low'),
        'comment': 'Integer representation of the instrument status codes.'
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pressure': {
        'long_name': 'Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'comment': 'Sea water pressure measured at the base of the transducer stalk.',
        'units': 'dbar'
    },
    'analog_in_1': {
        'long_name': 'Analog input 1',
        'comment': 'Analog input 1 data values',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'analog_in_2': {
        'long_name': 'Analog input 2',
        'comment': 'Analog input 2 data values',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'velocity_beam_1': {
        'long_name': 'Sea Water Velocity axis 1',
        'comment': 'sea water velocity axis 1 uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLE_L0',
        'units': 'm s-1',
    },
    'velocity_beam_2': {
        'long_name': 'Sea Water Velocity axis 2',
        'comment': 'Sea water velocity axis 2 uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLN_L0',
        'units': 'm s-1',
    },
    'velocity_beam_3': {
        'long_name': 'Sea Water Velocity axis 3',
        'comment': 'Sea water velocity axis 3 uncorrected for magnetic declination.',
        'data_product_identifier': 'VELPTTU-VLU_L0',
        'units': 'm s-1',
    },
    'velocity_east_corrected': {
        'long_name': 'Eastward Sea Water Velocity',
        'standard_name': 'eastward_sea_water_velocity',
        'comment': 'Eastward sea water velocity corrected for magnetic declination and scaled to m/s.',
        'data_product_identifier': 'VELPTTU-VLE_L1',
        'units': 'm s-1',
    },
    'velocity_north_corrected': {
        'long_name': 'Northward Sea Water Velocity',
        'standard_name': 'northward_sea_water_velocity',
        'comment': 'Northward sea water velocity corrected for magnetic declination and scaled to m/s.',
        'data_product_identifier': 'VELPTTU-VLN_L1',
        'units': 'm s-1',
    },
    'velocity_vertical': {
        'long_name': 'Upward Sea Water Velocity',
        'standard_name': 'upward_sea_water_velocity',
        'comment': 'Vertical sea water velocity component.',
        'data_product_identifier': 'VELPTTU-VLU_L0',
        'units': 'm s-1',
    },
    'speed': {
        'long_name': 'Speed, of what?',
        'comment': 'Speed of ?',
        'units': 'm s-1',
    },
    'direction': {
        'long name': 'Direction, of what?',
        'comment': 'Direction of ?',
        'units': 'degrees',
    },
    'amplitude_beam_1': {
        'long_name': 'Velocity Amplitude Beam 1',
        'comment': ('Raw measurement, for beam 1, of the difference in frequency between the transmitted ' +
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'amplitude_beam_2': {
        'long_name': 'Velocity Amplitude Beam 2',
        'comment': ('Raw measurement, for beam 2, of the difference in frequency between the transmitted ' +
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'amplitude_beam_3': {
        'long_name': 'Velocity Amplitude Beam 3',
        'comment': ('Raw measurement, for beam 3, of the difference in frequency between the transmitted ' +
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'counts'
    },
    'correlation_beam_1': {
        'long_name': 'Percent Correlation Beam 1',
        'comment': ('Percent correlation, for beam 1, is a measure of the similarity of two pulse echoes being ' +
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between ' +
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high ' +
                    'correlation because it gives us confidence the system measured the two pulses it originally ' +
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    },
    'correlation_beam_2': {
        'long_name': 'Percent Correlation Beam 2',
        'comment': ('Percent correlation, for beam 2, is a measure of the similarity of two pulse echoes being ' +
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between ' +
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high ' +
                    'correlation because it gives us confidence the system measured the two pulses it originally ' +
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    },
    'correlation_beam_3': {
        'long_name': 'Percent Correlation Beam 3',
        'comment': ('Percent correlation, for beam 3, is a measure of the similarity of two pulse echoes being ' +
                    'measured by the Doppler instrument. Zero correlation means nothing at all is similar between ' +
                    'the two echoes, where as a correlation of 100 means the two echoes are identical. We want high ' +
                    'correlation because it gives us confidence the system measured the two pulses it originally ' +
                    'sent out and is determining a valid phase shift.'),
        'units': 'percent'
    }
}

# Note: SHARED is swiped from the attr_common.py module in C. Wingard's upgrading branch of bitbucket.
#       When that branch is integrated, this should be deprecated in favor of the attr_common.py module
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