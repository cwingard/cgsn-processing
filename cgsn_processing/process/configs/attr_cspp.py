#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_cspp
@file cgsn_processing/process/configs/attr_cspp.py
@author Christopher Wingard
@brief Attributes for the CSPP dataset variables
"""
CSPP = {
    'global': {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scales Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Christopher Wingard',
        'creator_email': 'cwingard@coas.oregonstate.edu',
        'creator_url': 'http://oceanobservatories.org',
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'standard_name': 'deployment_id',
        'units': '1'
    },
    'profile_id': {
        'long_name': 'Profile ID',
        'standard_name': 'profile_id',
        'units': '1'
    },
    'site_depth': {
        'long_name': 'Deployment Site Depth',
        'standard_name': 'depth',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000'
    },
    'precise_time': {
        'long_name': 'Measurement Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01',
    },
    'z': {
        'long_name': 'Sensor Depth',
        'standard_name': 'depth_of_sensor_below_water',
        'units': 'm',
        'positive': 'down',
        'axis': 'Z',
        'valid_min': '-10000',
        'valid_max': '1000'
    }
}

CSPP_CTDPF = {
    'global': {
        'title': 'uCSPP CTD Data Records',
        'summary': (
            'Records the CTD data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'conductivity': {
        'long_name': 'Sea Water Conductivity',
        'standard_name': 'sea_water_electrical_conductivity',
        'units': 'mS cm-1'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius'
    },
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_salinity',
        'units': '1',
    },
    'in_situ_density': {
        'long_name': 'In-Situ Seawater Density',
        'standard_name': 'sea_water_density',
        'units': 'kg m-3',
        'valid_min': '1000',
        'valid_max': '1035'
    }
}

CSPP_DOSTA = {
    'global': {
        'title': 'uCSPP Dissolved Oxygen Data Records',
        'summary': (
            'Records the dissolved oxygen data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'depth': {
        'long_name': 'CSPP Depth from CTD',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'axis': 'Z',
        'valid_min': '-5',
        'valid_max': '1000',
    },
    'product_number': {
        'units': '1'
    },
    'serial_number': {
        'units': '1'
    },
    'estimated_oxygen_concentration': {
        'units': 'uM'
    },
    'estimated_oxygen_saturation': {
        'units': 'percent'
    },
    'optode_temperature': {
        'units': 'degree_Celsius'
    },
    'calibrated_phase': {
        'units': 'degree'
    },
    'temp_compensated_phase': {
        'units': 'degree'
    },
    'blue_phase': {
        'units': 'degree'
    },
    'red_phase': {
        'units': 'degree'
    },
    'blue_amplitude': {
        'units': 'mV'
    },
    'red_amplitude': {
        'units': 'mV'
    },
    'raw_temperature': {
        'units': 'mV'
    }
}

CSPP_FLORT = {
    'global': {
        'title': 'uCSPP ECO Triplet Data Records',
        'summary': (
            'Records chlorophyll, optical backscatter and CDOM data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'depth': {
        'long_name': 'CSPP Depth from CTD',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'axis': 'Z',
        'valid_min': '-5',
        'valid_max': '1000',
    },
    'measurement_wavelength_beta': {
        'units': 'nm'
    },
    'raw_signal_beta': {
        'units': 'counts'
    },
    'measurement_wavelength_chl': {
        'units': 'nm'
    },
    'raw_signal_chl': {
        'units': 'counts'
    },
    'measurement_wavelength_cdom': {
        'units': 'nm'
    },
    'raw_signal_cdom': {
        'units': 'counts'
    },
    'raw_internal_temp': {
        'units': 'counts'
    },
    'estimated_chlorophyll': {
        'units': 'mg L-1'
    },
    'fluorometric_cdom': {
        'units': 'ppm'
    },
    'beta_700': {
        'units': 'm-1 sr-1'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degree_Celsius',
        'comment': 'Interpolated into record from co-located CTD for use in calculating the total optical backscatter'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_salinity',
        'units': '1',
        'comment': 'Interpolated into record from co-located CTD for use in calculating the total optical backscatter'
    },
    'bback': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'units': 'm-1'
    }
}

CSPP_PARAD = {
    'global': {
        'title': 'uCSPP PAR Data Records',
        'summary': (
            'Records downwelling PAR data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'depth': {
        'long_name': 'CSPP Depth from CTD',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'axis': 'Z',
        'valid_min': '-5',
        'valid_max': '1000',
    },
    'raw_par': {
        'units': 'counts'
    },
    'irradiance': {
        'long_name': 'Downwelling Photosynthetic Radiation',
        'standard_name': 'downwelling_photosynthetic_photon_spherical_irradiance_in_sea_water',
        'units': 'umol m-2 s-1'
    }
}

CSPP_SPKIR = {
    'global': {
        'title': 'uCSPP Downwelling Spectral Irradiance Data Records',
        'summary': (
            'Records 7 wavelengths of downwelling irradiance data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'depth': {
        'long_name': 'CSPP Depth from CTD',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'axis': 'Z',
        'valid_min': '-5',
        'valid_max': '1000',
    },
    'serial_number': {
        'units': '1'
    },
    'timer': {
        'units': 's'
    },
    'sample_delay': {
        'units': 'ms'
    },
    'raw_channels': {
        'units': 'counts'
    },
    'input_voltage': {
        'units': 'V'
    },
    'analog_rail_voltage': {
        'units': 'V'
    },
    'frame_counter': {
        'units': '1'
    },
    'internal_temperature': {
        'units': 'degree_Celsius'
    },
    'irradiance': {
        'long_name': 'Downwelling Spectral Irradiance',
        'standard_name': 'downwelling_spectral_spherical_irradiance_in_sea_water',
        'units': 'uW cm-2 nm-1'
    },
    'wavelengths': {
        'long_name': 'Radiation Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    }
}

CSPP_VELPT = {
    'global': {
        'title': 'uCSPP ECO Triplet Data Records',
        'summary': (
            'Records chlorophyll, optical backscatter and CDOM data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'depth': {
        'long_name': 'CSPP Depth from CTD',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'axis': 'Z',
        'valid_min': '-5',
        'valid_max': '1000',
    },
    'speed_of_sound': {
        'units': 'm s-1'
    },
    'heading': {
        'units': 'degree'
    },
    'pitch': {
        'units': 'degree'
    },
    'roll': {
        'units': 'degree'
    },
    'pressure': {
        'units': 'dbar'
    },
    'temperature': {
        'units': 'degree_Celsius'
    },
    'velocity_east': {
        'units': 'cm s-1'
    },
    'velocity_north': {
        'units': 'cm s-1'
    },
    'velocity_vertical': {
        'units': 'cm s-1'
    },
    'amplitude_beam1': {
        'units': 'counts'
    },
    'amplitude_beam2': {
        'units': 'counts'
    },
    'amplitude_beam3': {
        'units': 'counts'
    }
}
