#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mmp
@file cgsn_processing/process/configs/attr_mmp_coastal.py
@author Joe Futrelle and Christopher Wingard
@brief Attributes for the MMP variables
"""
import numpy as np
from cgsn_processing.process.common import dict_update
from cgsn_processing.process.configs.attr_common import CTD
from cgsn_processing.process.configs.attr_common import CO_LOCATED
from cgsn_processing.process.configs.attr_flort import FLORT

MMP = {
    # standard attributes used by all MMP datasets
    'global': {
        'title': 'McLane Moored Profiler Data',
        'summary': 'Datasets from the McLane Moored Profiler (MMP).',
    },
    'profile_id': {
        'cf_role': 'profile_id',
        'long_name': 'Profile ID',
        'comment': ('The profile ID is the sequential number assigned to the profile by the MMP software. Combined '
                    'with the deployment ID')
    },
    'profiler_depth': {
        'long_name': 'Profiler Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Depth of the profiler calculated from the CTD pressure record.',
    }
}

MMP_ADATA = {
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'comment': 'In-situ sea water temperature measured at in the center of the transducer head.',
        'units': 'degrees_Celsius'
    },
    'heading': {
        'long_name': 'Heading',
        'comment': 'Measured heading of the Aquadopp II, uncorrected for magnetic declination.',
        'units': 'degrees'
    },
    'pitch': {
        'long_name': 'Pitch',
        'comment': 'Measured pitch of the Aquadopp II.',
        'units': 'degrees'
    },
    'roll': {
        'long_name': 'Roll',
        'comment': 'Measured roll of the Aquadopp II.',
        'units': 'degrees'
    },
    'beams': {
        'long_name': 'Beam Mapping',
        'comment': ('An array of 5 values defining which physical beam (1 thru 4) is assigned to the 1st through the '
                    '3rd data sets (the 5th beam and the 4th and 5th data sets are not used). The Aquadopp II assigns '
                    'physical beams 1, 2 and 4 during an upcast to the 1st, 2nd and 3rd data sets, respectively. '
                    'During a downcast, physical beams 2, 3, and 4 are assigned to the 1st thru 3rd data sets. The '
                    'velocity and amplitude parameters are named to correspond to the 1st, 2nd, and 3rd data sets. '
                    'With the mapping provided by this parameter, the user can determine which physical beam is '
                    'assigned to each data set.'),
        # 'units': '',    deliberately left blank, no units for this value
    },
    'beam_0_velocity': {
        'long_name': 'Velocity Data Set 1',
        'comment': ('The first velocity data set, mapped to a physical beam based on the data set description. Values'
                    'are beam velocities converted to m/s.'),
        'data_product_identifier': 'VELPTMN-1ST_L0',
        'units': 'm s-1',
    },
    'beam_1_velocity': {
        'long_name': 'Velocity Data Set 2',
        'comment': ('The second velocity data set, mapped to a physical beam based on the data set description. Values'
                    'are beam velocities converted to m/s.'),
        'data_product_identifier': 'VELPTMN-2ND_L0',
        'units': 'm s-1',
    },
    'beam_2_velocity': {
        'long_name': 'Velocity Data Set 3',
        'comment': ('The third velocity data set, mapped to a physical beam based on the data set description. Values'
                    'are beam velocities converted to m/s.'),
        'data_product_identifier': 'VELPTMN-3RD_L0',
        'units': 'm s-1',
    },
    'amplitude_0': {
        'long_name': 'Amplitude Data Set 1',
        'comment': ('Raw measurement, for the first data set, of the difference in frequency between the transmitted '
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'count'
    },
    'amplitude_1': {
        'long_name': 'Amplitude Data Set 2',
        'comment': ('Raw measurement, for the second data set, of the difference in frequency between the transmitted '
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'count'
    },
    'amplitude_2': {
        'long_name': 'Amplitude Data Set 3',
        'comment': ('Raw measurement, for the third data set, of the difference in frequency between the transmitted '
                    'and the received pulse, which is proportional to the velocity of the water.'),
        'units': 'count'
    },
    'relative_velocity_east': {
        'long_name': 'Eastward Sea Water Velocity',
        'standard_name': 'eastward_sea_water_velocity',
        'comment': ('Eastward sea water velocity corrected for magnetic declination and scaled to m/s. Note, '
                    'this is a relative velocity, not an absolute velocity, as the movement of the profiler '
                    'during ascent/descent has not been removed.'),
        'data_product_identifier': 'VELPTMN-VLE_L1',
        'units': 'm s-1',
        'ancillary_variables': 'beams beam_0_velocity beam_1_velocity beam_2_velocity heading pitch roll'
    },
    'relative_velocity_north': {
        'long_name': 'Northward Sea Water Velocity',
        'standard_name': 'northward_sea_water_velocity',
        'comment': ('Northward sea water velocity corrected for magnetic declination and scaled to m/s. Note, '
                    'this is a relative velocity, not an absolute velocity, as the movement of the profiler '
                    'during ascent/descent has not been removed.'),
        'data_product_identifier': 'VELPTMN-VLN_L1',
        'units': 'm s-1',
        'ancillary_variables': 'beams beam_0_velocity beam_1_velocity beam_2_velocity heading pitch roll'
    },
    'relative_velocity_vertical': {
        'long_name': 'Upward Sea Water Velocity',
        'standard_name': 'upward_sea_water_velocity',
        'comment': ('Vertical sea water velocity component scaled to m/s. Note, this is a relative velocity, not an '
                    'absolute velocity, as the movement of the profiler during ascent/descent has not been removed.'),
        'data_product_identifier': 'VELPTMN-VLU_L1',
        'units': 'm s-1',
        'ancillary_variables': 'beams beam_0_velocity beam_1_velocity beam_2_velocity heading pitch roll'
    }
}

MMP_CDATA = {
    # note, the CTD data is same as the CTD data in attr_common.py, but the oxygen data is slightly different
    # from the DOSTA data as the oxygen sensor is different. Set the oxygen attributes here and then add the common CTD
    # attributes to the dictionary
    'raw_oxygen': {
        'long_name': 'Raw Oxygen Concentration',
        'units': 'Hz',
        'comments': ('Raw oxygen measurement, recorded as a frequency from the SBE 43F by the SBE 52-MP used on the '
                     'McLane Moored Profilers.')
    },
    'oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'the SBE 43F Dissolved Oxygen Sensor.'),
        'data_product_identifier': 'DOCONCS_L1',
        '_FillValue': np.nan
    },
    'oxygen_concentration_corrected': {
        'long_name': 'Corrected Dissolved Oxygen Concentration',
        'standard_name': 'moles_of_oxygen_per_unit_mass_in_sea_water',
        'units': 'umol kg-1',
        'comments': ('The dissolved oxygen concentration from the Fast Response Dissolved Oxygen Instrument is a '
                     'measure of the concentration of gaseous oxygen mixed in seawater. This data product corrects '
                     'the dissolved oxygen concentration for the effects of salinity, temperature, and pressure with '
                     'data from a co-located CTD.'),
        'data_product_identifier': 'DOXYGEN_L2',
        '_FillValue': np.nan
    }
}
MMP_CDATA = dict_update(MMP_CDATA, CTD)

MMP_EDATA = {
    'motor_current': {
        'long_name': 'Motor Current',
        'units': 'mA',
        'comment': ('The current draw of the motor as it moves the MMP up or down the wire. The motor current is '
                    'a measure of the power required to move the profiler through the water column.'),
    },
    'battery_voltage': {
        'long_name': 'Battery Voltage',
        'comment': ('Voltage of the internal battery pack. The battery voltage is used to monitor the health of the '
                    'battery pack and to determine the amount of power available to the MMP.'),
        'units': 'V'
    },
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
    # attributes for the PAR sensor
    'raw_par': {
        'long_name': 'Raw PAR Measurement',
        'units': 'mV',
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
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_par'
    }
    # attributes for FLORT sensor will be added below
}
MMP_EDATA = dict_update(MMP_EDATA, FLORT)       # add the FLORT attributes to the MMP attributes
MMP_EDATA = dict_update(MMP_EDATA, CO_LOCATED)  # add the co-located CTD attributes to the MMP attributes
