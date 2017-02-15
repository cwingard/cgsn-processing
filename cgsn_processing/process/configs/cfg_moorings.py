#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_pwrsys
@file cgsn_processing/process/configs/attr_pwrsys.py
@author Christopher Wingard
@brief Attributes for the PWRSYS variables
"""
from munch import Munch

moorings = {
    'ce02shsm': {
        'D00001': {
            'lat': 44.00000,
            'lng': -124.00000,
            'buoy': {},
            'nsif': {
                'dosta': '',
                'flort': '',
                'optaa': '',
                'spkir': ''
            }
        },
        'D00002': {
            'lat': 44.00000,
            'lng': -124.00000,
            'buoy': {
                'depth': 0.0
            },
            'nsif': {
                'depth': 7.0,
                'dosta': '',
                'flort': '',
                'optaa': '',
                'spkir': ''
            }
        },
        'D00003': {
            'lat': 44.00000,
            'lng': -124.00000,
            'buoy': {
                'depth': 0.0
            },
            'nsif': {
                'depth': 7.0,
                'dosta': '',
                'flort': '',
                'optaa': '',
                'spkir': ''
            }
        },
        'D00004': {
            'lat': 44.00000,
            'lng': -124.00000,
            'buoy': {
                'depth': 0.0
            },
            'nsif': {
                'depth': 7.0,
                'dosta': '',
                'flort': '',
                'optaa': 'OPTAAD/CGINS-OPTAAD-00168__20160926',
                'spkir': ''
            }
        },
    },
}

moorings = Munch.fromDict(moorings)
