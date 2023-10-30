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

CSPP_CTDPF = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Conductivity, Temperature and Depth (CTD) Data from the uCSPP',
        'summary': ('Records the CTD data from the sensor mounted on the uncabled Coastal Surface Piercing '
                    'Profilers (uCSPP).')
    },
    # --> reported values
    'conductivity': {
        'long_name': 'Sea Water Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1',
        'comment': ('Sea water conductivity refers to the ability of seawater to conduct electricity. The presence '
                    'of ions, such as salt, increases the electrical conducting ability of seawater. As such, '
                    'conductivity can be used as a proxy for determining the quantity of salt in a sample of '
                    'seawater.'),
        'data_product_identifier': 'CONDWAT_L1',
        '_FillValue': np.nan
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Sea water temperature is the in situ temperature of the sea water.',
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': np.nan
    },
    'pressure': {
        'long_name': 'Seawater Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Seawater Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': np.nan
    },
    # --> derived values
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable.'),
        'data_product_identifier': 'PRACSAL_L2',
        'ancillary_variables': 'conductivity, temperature, pressure',
        '_FillValue': np.nan
    },
    'density': {
        'long_name': 'In-Situ Sea Water Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'comment': ('Sea water Density is the in situ density and is defined as mass per unit volume. It is '
                    'calculated from the conductivity, temperature and depth of a sea water sample.'),
        'data_product_identifier': 'DENSITY_L2',
        'ancillary_variables': 'lon, lat, salinity, temperature, pressure',
        '_FillValue': np.nan
    }
}

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
                    'nanometers) used by primary producers photosynthesis.'),
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
    }
}
CSPP_VELPT = dict_update(VELPT, velpt)

CSPP_WINCH = {
    'global': {
        'title': 'uCSPP Winch Controller Data Records',
        'summary': ('Records data from the uCSPP winch controller data files (winch motor status, attitude sensor '
                    'data, and pressure sensor data).')
    },
    'encoder_counts': {
        'units': 'counts'
    },
    'current': {
        'units': 'A'
    },
    'status_string': {
        'units': '1'
    },
    'raw_velocity': {
        'units': 'cm s-1'
    },
    'temperature': {
        'units': 'degrees_Celsius'
    },
    'voltage': {
        'units': 'V'
    },
    'raw_time': {
        'units': '1'
    },
    'raw_discharge': {
        'units': '1'
    },
    'rope_on_drum': {
        'units': 'm'
    },

    'pressure': {
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'velocity': {
        'units': 'cm s-1'
    },

    'heading': {
        'units': 'degrees'
    },
    'pitch': {
        'units': 'degrees'
    },
    'roll': {
        'units': 'degrees'
    }
}
