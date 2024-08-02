#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_cspp
@file cgsn_processing/process/configs/attr_cspp.py
@author Christopher Wingard
@brief Attributes for the CSPP dataset variables
"""
import numpy as np
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_ctdbp import CTDBP
from cgsn_processing.process.configs.attr_dosta import DOSTA
from cgsn_processing.process.configs.attr_flort import FLORT
from cgsn_processing.process.configs.attr_nutnr import NUTNR
from cgsn_processing.process.configs.attr_optaa import OPTAA
from cgsn_processing.process.configs.attr_spkir import SPKIR
from cgsn_processing.process.configs.attr_velpt import VELPT


CSPP = {
    # attributes shared by all CSPP data sets.
    'profile_id': {
        'long_name': 'Profile ID',
        # 'units': '',    deliberately left blank, no units for this value,
        'comment': ('Profiler ID. Includes the profiler number and a date and time string to help distinguish '
                    'individual profiles.'),
        'cf_role': 'profile_id'
    }
}

ctdpf = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Conductivity, Temperature and Depth (CTD) Data from the uCSPP',
        'summary': ('Records the CTD data from the sensor mounted on the uncabled Coastal Surface Piercing '
                    'Profilers (uCSPP).')
    }
}
CSPP_CTDPF = dict_update(CTDBP, ctdpf)

dosta = {
    'global': {
        'title': 'uCSPP Dissolved Oxygen Records',
        'summary': ('Records the dissolved oxygen concentrations data from the sensor mounted on the uncabled '
                    'Coastal Surface Piercing Profilers (uCSPP).')
    }
}
CSPP_DOSTA = dict_update(DOSTA, dosta)

flort = {
    'global': {
        'title': 'uCSPP ECO Triplet Data Records',
        'summary': ('Records chlorophyll, optical backscatter and CDOM data from the sensor mounted on the uncabled '
                    'Coastal Surface Piercing Profilers (uCSPP).')
    }
}
CSPP_FLORT = dict_update(FLORT, flort)

nutnr = {
    'global': {
        'title': 'uCSPP SUNA Data Records',
        'summary': ('Records the nitrate concentration from the sensor mounted on the uncabled Coastal Surface '
                    'Piercing Profilers (uCSPP).')
    }
}
CSPP_NUTNR = dict_update(NUTNR, nutnr)

optaa = {
    'global': {
        'title': 'uCSPP AC-S Data Records',
        'summary': ('Records the nitrate concentration from the sensor mounted on the uncabled Coastal Surface '
                    'Piercing Profilers (uCSPP).')
    }
}
CSPP_OPTAA = dict_update(OPTAA, optaa)

CSPP_PARAD = {
    'global': {
        'title': 'uCSPP Downwelling PAR Data Records',
        'summary': ('Records the downwelling PAR data from the sensor mounted on the uncabled Coastal Surface '
                    'Piercing Profilers (uCSPP).')
    },
    'raw_par_measurement': {
        'long_name': 'Raw PAR Measurement',
        'units': 'counts',
        'comment': 'Photosynthetically Active Radiation (PAR) unprocessed sensor reading.',
        'data_product_identifier': 'OPTPARW_L0'
    },
    'par': {
        'long_name': 'Photosynthetically Active Radiation',
        'standard_name': 'downwelling_photosynthetic_photon_flux_in_sea_water',
        'units': 'umol m-2 s-1',
        'comment': ('Photosynthetically Active Radiation (PAR), or photosynthetic photon flux density, is a measure '
                    'of the density of photons per unit area that are in the spectral range of light (400-700 '
                    'nanometers) used by primary producers for photosynthesis.'),
        'data_product_identifier': 'OPTPARW_L1',
        'ancillary_variables': 'raw_par_measurement'
    }
}

spkir = {
    'global': {
        'title': 'uCSPP Downwelling Spectral Irradiance Data Records',
        'summary': ('Records the 7 wavelengths of downwelling irradiance data from the sensor mounted on the '
                    'uncabled Coastal Surface Piercing Profilers (uCSPP).')
    }
}
CSPP_SPKIR = dict_update(SPKIR, spkir)

velpt = {
    'global': {
        'title': 'uCSPP Point Velocity Data Records',
        'summary': ('Records a profile of relative (seawater + profiler) point velocity data from the sensor mounted '
                    'on the uncabled Coastal Surface Piercing Profilers (uCSPP).')
    },
    'velocity_east': {
        'long_name': 'Estimated Eastward Seawater Velocity',
        'units': 'm s-1',
        'comment': ('This is the eastward seawater velocity component uncorrected for magnetic declination as '
                    'reported by the instrument in m/s.'),
        'data_product_identifier': 'VELPTMN-VLE_L0',
        'ancillary_variables': 'error_code status_code'
    },
    'velocity_north': {
        'long_name': 'Estimated Northward Seawater Velocity',
        'units': 'm s-1',
        'comment': ('This is the northward seawater velocity component uncorrected for magnetic declination as '
                    'reported by the instrument in m/s.'),
        'data_product_identifier': 'VELPTMN-VLN_L0',
        'ancillary_variables': 'error_code status_code'
    },
    'velocity_vertical': {
        'long_name': 'Vertical Seawater Velocity',
        'standard_name': 'upward_sea_water_velocity',
        'units': 'm s-1',
        'comment': 'The vertical seawater velocity component as reported by the instrument in m/s.',
        'data_product_identifier': 'VELPTMN-VLU_L0',
        'ancillary_variables': 'error_code status_code'
    }
}
CSPP_VELPT = dict_update(VELPT, velpt)

CSPP_WINCH = {
    'global': {
        'title': 'uCSPP Winch Controller Data Records',
        'summary': ('Records data from the uCSPP winch controller data files (winch motor status, attitude sensor '
                    'data, and pressure sensor data).')
    },
    # from the WC_WM files
    'encoder_counts': {
        'long_name': 'Encoder Counts',
        'units': 'counts',
        'comment': 'The number of encoder counts from the winch motor.'
    },
    'voltage': {
        'long_name': 'Motor Voltage',
        'units': 'V',
        'comment': 'The voltage supplied to the winch motor.'
    },
    'current': {
        'long_name': 'Motor Current',
        'units': 'A',
        'comment': 'The current supplied to the winch motor.'
    },
    'status_string': {
        'long_name': 'Status String',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'The status string from the winch motor.'
    },
    'raw_velocity': {
        'long_name': 'Raw Velocity',
        'units': 'cm s-1',
        'comment': 'The raw velocity from the winch motor.'
    },
    'temperature': {
        'long_name': 'Motor Temperature',
        'units': 'degrees_Celsius',
        'comment': 'The temperature of the winch motor.'
    },
    'raw_time': {
        'long_name': 'Raw Time',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'The raw time from the winch motor.'
    },
    'raw_discharge': {
        'long_name': 'Raw Discharge',
        # 'units': '',    deliberately left blank, no units for this value
        'comment': 'The raw discharge from the winch motor.'
    },
    'rope_on_drum': {
        'long_name': 'Rope on Drum',
        'units': 'm',
        'comment': 'The amount of line on the winch drum.'
    },
    # from the WC_SBE files
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1'
    },
    'velocity': {
        'long_name': 'Profiler Ascent Velocity',
        'standard_name': 'platform_speed_wrt_sea_water',
        'units': 'cm s-1',
        'comment': ('The velocity of the profiler as it ascends through the water column. The profiler is '
                    'attached to the winch and is raised and lowered by the winch motor.'),
    },
    # from the WC_HMR files
    'heading': {
        'long_name': 'Heading',
        'standard_name': 'platform_orientation',
        'units': 'degrees',
        'comment': ('The heading of the profiler control can, used to track profiler rotations as it ascends through '
                    'the water column.')
    },
    'pitch': {
        'long_name': 'Pitch',
        'standard_name': 'platform_pitch',
        'units': 'degrees',
        'comment': 'The pitch of the profiler control can.'
    },
    'roll': {
        'long_name': 'Roll',
        'standard_name': 'platform_roll',
        'units': 'degrees',
        'comment': 'The roll of the profiler control can.'
    }
}
