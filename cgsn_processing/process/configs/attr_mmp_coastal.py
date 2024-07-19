#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mmp
@file cgsn_processing/process/configs/attr_mmp_coastal.py
@author Joe Futrelle
@brief Attributes for the MMP variables
"""
import numpy as np

MMP = {
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

MMP_ADATA = dict({
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
})

MMP_CDATA = {
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
    'raw_oxygen': {
        'long_name': 'Raw Oxygen Concentration',
        'units': 'Hz',
        'comments': ('Raw oxygen measurement, recorded as a frequency from the SBE 43F by the SBE 52-MP used on the '
                     'McLane Moored Profilers.')
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
    'raw_par': {
        'long_name': 'Raw PAR Measurement',
        'units': 'mV',
        'comment': 'Photosynthetically Active Radiation (PAR) unprocessed sensor reading.',
        'data_product_identifier': 'OPTPARW_L0'
    },
    'raw_signal_beta': {
        'long_name': 'Raw Optical Backscatter at 700 nm',
        'units': 'count',
        'comment': 'Raw optical backscatter measurements at 700 nm.',
        'data_product_identifier': 'FLUBSCT_L0'
    },
    'raw_signal_chl': {
        'long_name': 'Raw Chlorophyll Fluorescence',
        'units': 'count',
        'comment': 'Raw chlorophyll fluorescence (470 nm excitation/ 695 nm emission) measurements.',
        'data_product_identifier': 'CHLAFLO_L0'
    },
    'raw_signal_cdom': {
        'long_name': 'Raw DOM Fluorescence',
        'units': 'count',
        'comment': 'Raw DOM fluorescence (370 nm excitation/ 460 nm emission) measurements.',
        'data_product_identifier': 'CDOMFLO_L0'
    },
    # dataset attributes --> co-located CTD data
    'ctd_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. Measurements are from a '
                    'co-located CTD'),
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': np.nan
    },
    'ctd_salinity': {
        'long_name': 'Sea Water Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': ('Salinity is generally defined as the concentration of dissolved salt in a parcel of sea water. '
                    'Practical Salinity is a more specific unitless quantity calculated from the conductivity of '
                    'sea water and adjusted for temperature and pressure. It is approximately equivalent to Absolute '
                    'Salinity (the mass fraction of dissolved salt in sea water), but they are not interchangeable. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRACSAL_L2',
        '_FillValue': np.nan
    },
    # dataset attributes --> derived values
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
    },
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll Concentration',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'ug L-1',
        'comment': ('Estimated chlorophyll concentration based upon a calibration curve derived from a fluorescent '
                    'proxy approximately equal to 25 ug/l of a Thalassiosira weissflogii phytoplankton culture. '
                    'This measurement is considered to be an estimate only of the true chlorophyll concentration.'),
        'data_product_identifier': 'CHLAFLO_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_chl'
    },
    'fluorometric_cdom': {
        'long_name': 'Fluorometric CDOM Concentration',
        'standard_name': ('concentration_of_colored_dissolved_organic_matter_in_sea_water_expressed_as_equivalent'
                          '_mass_fraction_of_quinine_sulfate_dihydrate'),
        'units': 'ppb',
        'comment': ('More commonly referred to as Chromophoric Dissolved Organic Matter (CDOM). CDOM plays an '
                    'important role in the carbon cycling and biogeochemistry of coastal waters. It occurs '
                    'naturally in aquatic environments primarily as a result of tannins released from decaying '
                    'plant and animal matter, and can enter coastal areas in river run-off containing organic '
                    'materials leached from soils.'),
        'data_product_identifier': 'CDOMFLO_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_cdom'
    },
    'beta_700': {
        'long_name': 'Volume Scattering Function at 700 nm',
        'standard_name': 'volume_scattering_function_of_radiative_flux_in_sea_water',
        'units': 'm-1 sr-1',
        'comment': ('Radiative flux is the sum of shortwave and longwave radiative fluxes. Scattering of '
                    'radiation is its deflection from its incident path without loss of energy. The volume '
                    'scattering function is the intensity (flux per unit solid angle) of scattered radiation per '
                    'unit length of scattering medium, normalised by the incident radiation flux.'),
        'data_product_identifier': 'FLUBSCT_L1',
        '_FillValue': np.nan,
        'ancillary_variables': 'raw_signal_beta'
    },
    'bback': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'units': 'm-1',
        'comment': ('Total (particulate + water) optical backscatter at 700 nm, derived from the Volume '
                    'Scattering Function and corrected for effects of temperature and salinity.'),
        'data_product_identifier': 'FLUBSCT_L2',
        '_FillValue': np.nan,
        'ancillary_variables': 'beta_700 ctd_temperature ctd_salinity'
    }
}
