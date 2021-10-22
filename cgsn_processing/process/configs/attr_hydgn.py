#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_hydgn
@file cgsn_processing/process/configs/attr_hydgn.py
@author Christopher Wingard
@brief Attributes for the hydrogen gas variables
"""
HYDGN = {
    'global': {
        'title': 'Mooring Hydrogen Gas Lower Explosive Limit Concentration Data',
        'summary': ('Records the internal buoy well hydrogen gas concentration as a percentage of '
                    'the Lower Explosive Limit')
    },
    'hydrogen_concentration': {
        'long_name': 'LEL Hydrogen Concentration',
        'units': 'percent',
        'comment': ('Hydrogen concentration expressed as a percentage of the lower explosive limit (LEL), which '
                    'is 2% hydrogen gas concentration in air. LEL hydrogen concentrations less than 10% (or 0.2% '
                    'absolute) are considered acceptable for operations.')
    }
}
