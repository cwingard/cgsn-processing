#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_presf
@file cgsn_processing/process/configs/attr_presf.py
@author Joe Futrelle and Christopher Wingard
@brief Attributes for the PRESF variables
"""
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_superv import SUPERV

common = {
    # variables common to all SBD messages, pulled out of the email message body
    'momsn': {
        'long_name': 'Mobile-Originated Message Sequence Number',
        'units': 'count',
        'comment': ('The mobile-originated message sequence number (MOMSN) is a unique identifier for each message '
                    'transmitted by the Iridium Short Burst Data (SBD) system. The MOMSN increments by one for each '
                    'message transmitted by the beacon.')
    },
    'status_code': {
        'long_name': 'MO Status Code',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'flag_values': [0, 1, 2, 10, 12, 13, 14, 15],
        'flag_meanings': ('transfer_ok transfer_ok_mt_message_too_large_for_single_session '
                          'transfer_ok_location_unacceptable session_timeout message_too_large_for_single_session '
                          'rf_link_loss imei_protocol_anomaly prohibited_access'),
        'comment': ('Provides an indication of success of the SBD session between the IMEI and the Iridium Gateway '
                    'associated with the over-the-air payload delivery.')
    },
    'transfer_bytes': {
        'long_name': 'Transfer Bytes',
        'units': 'bytes',
        'comment': 'Indicates the number of bytes transferred during the Iridium SBD transmission.'
    },
    'estimated_latitude': {
        'long_name': 'Estimated Latitude',
        'units': 'degrees_north',
        'comment': ('Provides the geographic location of the SBD modem. The latitude and longitude provide a center '
                    'point and the cep_radius provides the radius of a circle around that center point. The reported '
                    'position is accurate (within the reported circle) 80 percent of the time.')
    },
    'estimated_longitude': {
        'long_name': 'Estimated Longitude',
        'units': 'degrees_east',
        'comment': ('Provides the geographic location of the SBD modem. The latitude and longitude provide a center '
                    'point and the cep_radius provides the radius of a circle around that center point. The reported '
                    'position is accurate (within the reported circle) 80 percent of the time.')
    },
    'cep_radius': {
        'long_name': 'Circular Error Probable Radius',
        'units': 'km',
        'comment': ('The circular error probable (CEP) radius indicates the accuracy of the estimated geographic '
                    'location of the SBD beacon reported in kilometers.'),
    }
}

xeos = {
    'global': {
        'title': 'GPS Location Beacons',
        'summary': ('Xeos Technologies GPS beacons used to determine the location of the mooring during a deployment. '
                    'Beacons attached to the tower have a watch circle (radius varies based on site depth) enabled '
                    'to alert if they go adrift. Beacons attached to subsurface elements will only report their '
                    'location when they are on the surface. Normally, this only occurs when the mooring is being '
                    'deployed or recovered.')
    },
    'watch_circle_status': {
        'long_name': 'Watch Circle Status',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'flag_values': [0, 1, 2],
        'flag_meanings': 'disabled enabled alarm',
        'comment': ('The watch circle status indicates the watch circle mode: disabled, enabled, or alarm. The watch '
                    'circle is a circular region around the beacon center point with a user-defined radius (based on '
                    'the site depth) in meters. When the watch circle is enabled, the beacon will send an alarm '
                    'message if it moves outside the watch circle.')
    },
    'subsurface_beacon': {
        'long_name': 'Subsurface Beacon Flag',
        'standard_name': 'status_flag',
        # 'units': '',    deliberately left blank, no units for this value
        'flag_values': [0, 1],
        'flag_meanings': 'surface subsurface',
        'comment': ('The subsurface beacon flag indicates whether the beacon is attached to a subsurface element '
                    '(e.g., a subsurface mooring float, 1) or to the tower (0).')
    },
    'precise_latitude': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'comment': ('Indicates the actual latitude of the mooring, compared to the deployment location or Iridium '
                    'estimated location, using data from the GPS antenna at the time of the Iridium SBD transmission.')
    },
    'precise_longitude': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'comment': ('Indicates the actual longitude of the mooring, compared to the deployment location or Iridium '
                    'estimated location, using data from the GPS antenna at the time of the Iridium SBD transmission.')
    },
    'distance_from_center': {
        'long_name': 'Distance from Center',
        'units': 'km',
        'comment': ('The distance from center indicates the distance between the beacon and the center of the watch '
                    'circle in kilometers.')
    },
    'time_in_circle': {
        'long_name': 'Time in Circle',
        'units': 'days',
        'comment': ('The time in circle indicates the amount of time the beacon has been inside the watch circle '
                    'since the last Iridium SBD transmission.')
    },
    'signal_strength': {
        'long_name': 'Signal Strength',
        'units': 'dB',
        'comment': 'The signal strength indicates the signal strength of the Iridium SBD transmission in dB.'
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'units': 'V',
        'comment': ('The battery voltage indicates the battery voltage of the beacon at the time of the Iridium SBD '
                    'transmission.')
    }
}
XEOS = dict_update(common, xeos)

cpm = {
    'global': {
        'title': 'CPM Supervisor Data via Iridium SBD Messaging',
        'summary': ('Subset of the CPM supervisor data transmitted via Iridium Short Burst Data (SBD) messaging. The '
                    'CPM supervisor monitors and controls the CPM and its attached subsystems. The data are '
                    'transmitted at a user-defined interval in text files attached to an email message.'),
    },
    'sbd_signal_strength': {
        'long_name': 'Satellite Signal Strength Indicator',
        # 'units': '',  # deliberately left blank, no units for this value
        'flag_values': [0, 1, 2, 3, 4, 5],
        'flag_meanings': 'no_signal weak_signal moderate_signal good_signal excellent_signal',
        'comment': ('The signal strength indicates the signal strength of the Iridium SBD transmission from 0 '
                    '(no signal) to 5 (excellent signal). Signal strength of 1 or higher should permit an SBD call '
                    'to be made.')
    }
}
attrs = dict_update(SUPERV['cpm'], SUPERV['common'])
cpm = dict_update(cpm, common)
CPM = dict_update(cpm, attrs)

stc = {
    'global': {
        'title': 'STC Supervisor Data via Iridium SBD Messaging',
        'summary': ('Subset of the STC supervisor data transmitted via Iridium Short Burst Data (SBD) messaging. The '
                    'STC supervisor monitors and controls the STC and its attached subsystems and instruments. The '
                    'data are transmitted at a user-defined interval in text files attached to an email message.'),
    }
}
attrs = dict_update(SUPERV['stc'], SUPERV['common'])
stc = dict_update(stc, common)
STC = dict_update(stc, attrs)
