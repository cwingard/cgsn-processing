#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_cspp
@file cgsn_processing/process/configs/attr_cspp.py
@author Christopher Wingard
@brief Attributes for the CSPP dataset variables
"""
import numpy as np

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
        'units': '1'
    },
    'profile_id': {
        'long_name': 'Profile ID',
        'units': '1',
    },
    'z': {
        'long_name': 'Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'Deployment site depth',
        'positive': 'down',
        'axis': 'Z'
    },
    'precise_time': {
        'long_name': 'Measurement Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01',
    },
    'ctd_depth': {
        'long_name': 'Depth from CTD Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'valid_min': '-5',
        'valid_max': '1000',
        'comment': 'Pressure used as proxy for depth interpolated into record from co-located CTD'
    },
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
        'units': 'degrees_Celsius'
    },
    'pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
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
        'units': 'degrees_Celsius'
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
    'measurement_wavelength_beta': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_beta': {
        'units': 'counts'
    },
    'measurement_wavelength_chl': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_chl': {
        'units': 'counts'
    },
    'measurement_wavelength_cdom': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_cdom': {
        'units': 'counts'
    },
    'raw_internal_temp': {
        'units': 'counts'
    },
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'mg L-1'
    },
    'fluorometric_cdom': {
        'long_name': 'Fluorometric CDOM',
        'units': 'ppm'
    },
    'beta_700': {
        'long_name': 'Volume Scattering Function at 700 nm',
        'standard_name': 'volume_scattering_function_of_radiative_flux_in_sea_water',
        'units': 'm-1 sr-1'
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'bback': {
        'long_name': 'Total Optical Backscatter at 700 nm',
        'units': 'm-1'
    }
}

CSPP_NUTNR = {
    'global': {
        'title': 'uCSPP Satlantic SUNA Data Records',
        'summary': (
            'Records the nitrate concentration for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'measurement_type': {
        'units': '1'
    },
    'year': {
        'units': 'year'
    },
    'day_of_year': {
        'units': 'day'
    },
    'decimal_hours': {
        'units': 'hour'
    },
    'nitrate_concentration': {
        'units': 'umol L-1'
    },
    'nitrogen_in_nitrate': {
        'units': 'mg L-1'
    },
    'absorbance_254': {
        'units': '1'
    },
    'absorbance_250': {
        'units': '1'
    },
    'bromide_trace': {
        'units': 'mg L-1'
    },
    'spectal_average': {
        'units': '1'
    },
    'dark_value': {
        'units': '1'
    },
    'integration_factor': {
        'units': '1'
    },
    'channel_measurements': {
        'units': 'counts'
    },
    'temperature_internal': {
        'units': 'degrees_Celsius'
    },
    'temperature_spectrometer': {
        'units': 'degrees_Celsius'
    },
    'temperature_lamp': {
        'units': 'degrees_Celsius'
    },
    'lamp_on_time': {
        'units': 's'
    },
    'humidity': {
        'units': 'percent'
    },
    'voltage_main': {
        'units': 'V'
    },
    'voltage_lamp': {
        'units': 'V'
    },
    'voltage_internal': {
        'units': 'V'
    },
    'main_current': {
        'units': 'mA'
    },
    'fit_auxiliary_1': {
        'units': '1'
    },
    'fit_auxiliary_2': {
        'units': '1'
    },
    'fit_base_1': {
        'units': '1'
    },
    'fit_base_2': {
        'units': '1'
    },
    'fit_rmse': {
        'units': '1'
    },
    'temperature': {
       'long_name': 'Sea Water Temperature',
       'standard_name': 'sea_water_temperature',
       'units': 'degrees_Celsius',
       'comment': 'Interpolated into record from co-located CTD'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'wavelengths': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
    },
    'corrected_nitrate': {
        'long_name': 'Corrected Nitrate Concentration',
        'standard_name': 'mole_concentration_of_nitrate_in_sea_water',
        'units': 'umol L-1'
    }
}

CSPP_OPTAA = {
    'global': {
        'title': 'uCSPP WET Labs AC-S Data Records',
        'summary': (
            'Records the absorbance and attenuation data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'serial_number': {
        'long_name': 'Unit Serial Number',
        'units': '1'
    },
    'a_reference_dark': {
        'long_name': 'A Channel Dark Reference',
        'units': 'counts'
    },
    'pressure_raw': {
        'long_name': 'Raw Pressure',
        'units': 'counts'
    },
    'pressure': {
        'long_name': 'Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'a_signal_dark': {
        'long_name': 'A Channel Dark Signal',
        'units': 'counts'
    },
    'external_temp_raw': {
        'long_name': 'Raw External Temperature',
        'units': 'counts'
    },
    'external_temp': {
        'long_name': 'In-Situ Temperature',
        'standard_name': 'seawater_temperature',
        'units': 'degrees_Celsius'
    },
    'internal_temp_raw': {
        'long_name': 'Raw Internal Temperature',
        'units': 'counts'
    },
    'internal_temp': {
        'long_name': 'Instrument Temperature',
        'units': 'degrees_Celsius'
    },
    'c_reference_dark': {
        'long_name': 'C Channel Dark Reference',
        'units': 'counts'
    },
    'c_signal_dark': {
        'long_name': 'C Channel Dark Signal',
        'units': 'counts'
    },
    'elapsed_run_time': {
        'long_name': 'Elapsed Run Time',
        'units': 'ms'
    },
    'num_wavelengths': {
        'long_name': 'Number of Wavelengths',
        'units': '1'
    },
    'wavelengths': {'units': '1'},
    'a_wavelengths': {
        'long_name': 'A Channel Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'c_wavelengths': {
        'long_name': 'c Channel Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'c_reference_raw': {
        'long_name': 'C Channel Raw Reference',
        'units': 'counts',
        'fill_value': np.int32(-999999999)
    },
    'a_reference_raw': {
        'long_name': 'A Channel Raw Reference',
        'units': 'counts',
        'fill_value': np.int32(-999999999)
    },
    'c_signal_raw': {
        'long_name': 'C Channel Raw Signal',
        'units': 'counts',
        'fill_value': np.int32(-999999999)
    },
    'a_signal_raw': {
        'long_name': 'A Channel Raw Signal',
        'units': 'counts',
        'fill_value': np.int32(-999999999)
    },
    'apd': {
        'long_name': 'Particulate and Dissolved Absorbance',
        'units': 'm-1',
        'fill_value': np.nan
    },
    'apd_ts': {
        'long_name': 'Particulate and Dissolved Absorbance with TS Correction',
        'units': 'm-1',
        'fill_value': np.nan
    },
    'apd_ts_s': {
        'long_name': 'Particulate and Dissolved Absorbance with TS and Scatter Correction',
        'units': 'm-1',
        'fill_value': np.nan
    },
    'cpd': {
        'long_name': 'Particulate and Dissolved Attenuation',
        'units': 'm-1',
        'fill_value': np.nan
    },
    'cpd_ts': {
        'long_name': 'Particulate and Dissolved Attenuation with TS Correction',
        'units': 'm-1',
        'fill_value': np.nan
    },
    'temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': 'Interpolated into record from co-located CTD'
    },
    'salinity': {
        'long_name': 'Practical Salinity',
        'standard_name': 'sea_water_practical_salinity',
        'units': '1',
        'comment': 'Interpolated into record from co-located CTD'
    }
}

CSPP_PARAD = {
    'global': {
        'title': 'uCSPP PAR Data Records',
        'summary': (
            'Records downwelling PAR data for the uncabled Coastal Surface Piercing Profilers'
        )
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
        'units': 'degrees_Celsius'
    },
    'irradiance': {
        'long_name': 'Downwelling Spectral Irradiance',
        'standard_name': 'downwelling_spectral_spherical_irradiance_in_sea_water',
        'units': 'uW cm-2 nm-1'
    },
    'wavelengths': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    }
}

CSPP_VELPT = {
    'global': {
        'title': 'uCSPP ECO Triplet Data Records',
        'summary': (
            'Records combined profiler and seawater point velocity data for the uncabled Coastal Surface Piercing Profilers'
        )
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
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar'
    },
    'temperature': {
        'units': 'degrees_Celsius'
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

CSPP_WINCH = {
    'global': {
        'title': 'uCSPP Winch Controller Data',
        'summary': (
            'Records data from the uCSPP winch controller data files'
        )
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
        'units': 'degree'
    },
    'pitch': {
        'units': 'degree'
    },
    'roll': {
        'units': 'degree'
    }
}
