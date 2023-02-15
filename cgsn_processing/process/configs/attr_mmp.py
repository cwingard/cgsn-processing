#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_mmp
@file cgsn_processing/process/configs/attr_mmp.py
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
        'comment': 'Depth of the profiler calculated from the sensor (either engineering or CTD) pressure records.',
    }
}

MMP_ADATA = {
    'temperature',
    'heading',
    'pitch',
    'roll',
    'beam_0_velocity',
    'beam_1_velocity',
    'beam_2_velocity',
    'amplitude_beam_0',
    'amplitude_beam_1',
    'amplitude_beam_2'
}

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
    'motor_current',
    'battery_voltage',
    'pressure',
    'raw_par',
    'raw_backscatter',
    'raw_chlorophyll',
    'raw_cdom'
}
