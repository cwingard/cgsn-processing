#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_cspp
@file cgsn_processing/process/configs/attr_cspp.py
@author Christopher Wingard
@brief Attributes for the CSPP dataset variables
"""
import numpy as np
from cgsn_processing.process.common import FILL_INT, FILL_NAN

CSPP = {
    'global': {
        'project': 'Ocean Observatories Initiative',
        'institution': 'Coastal and Global Scale Nodes (CGSN)',
        'acknowledgement': 'National Science Foundation',
        'references': 'http://oceanobservatories.org',
        'creator_name': 'Ocean Observatories Initiative',
        'creator_email': 'helpdesk@oceanobservatories.org',
        'creator_url': 'http://oceanobservatories.org',
        'featureType': 'timeSeriesProfile',
        'cdm_data_type': 'Station',
        'Conventions': 'CF-1.7'
    },
    'deploy_id': {
        'long_name': 'Deployment ID',
        'comment': ('Mooring deployment ID. Useful for differentiating data by deployment, '
                    'allowing for overlapping deployments in the data sets.')
    },
    'profile_id': {
        'cf_role': 'profile_id',
        'long_name': 'Profile ID',
        'comment': ('Profiler ID. Includes the profiler number and a date and time string to help distinguish '
                    'individual profiles. ')
    },
    'station': {
        'cf_role': 'timeseries_id',
        'long_name': 'Station Name',
    },
    'time': {
        'long_name': 'Time',
        'standard_name': 'time',
        'units': 'seconds since 1970-01-01T00:00:00.000Z',
        'axis': 'T',
        'calendar': 'gregorian',
        'comment': ('Derived from either the DCL data logger GPS referenced clock, or the internal instrument clock. '
                    'For instruments attached to a DCL, the instrument''s internal clock can be cross-compared to '
                    'the GPS clock to determine the internal clock''s offset and drift.')
    },
    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'longitude',
        'units': 'degrees_east',
        'axis': 'X',
        'comment': ('CSPP mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'latitude',
        'units': 'degrees_north',
        'axis': 'Y',
        'comment': ('CSPP mooring deployment location, surveyed after deployment to determine the anchor location and '
                    'the center of the watch circle.')
    },
    'z': {
        'long_name': 'Site Depth',
        'standard_name': 'sea_floor_depth_below_sea_surface',
        'units': 'm',
        'comment': ('Sea floor depth of the CSPP mooring deployment.'),
        'positive': 'down',
        'axis': 'Z'
    },
    'ctd_pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Sea Water Pressure refers to the pressure exerted on a sensor in situ by the weight of the '
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the '
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water '
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRESWAT_L1'
    },
    'ctd_depth': {
        'long_name': 'Profiler Depth',
        'standard_name': 'depth',
        'units': 'm',
        'comment': 'The CTD pressure record from the co-located CTD, converted to depth in meters.',
        'ancillary_variables': 'ctd_pressure lat'
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
        'title': 'Dissolved Oxygen Data from the CSPP',
        'summary': 'Dissolved oxygen concentrations from the Aanderaa Optode dissolved oxygen sensor.'
    },
    # dataset attributes --> parsed data
    'product_number': {
        'long_name': 'Product Number',
        'comment': 'Optode product number, usually model 4831 for OOI systems.',
        # 'units': '',    deliberately left blank, no units for this value,
    },
    'serial_number': {
        'long_name': 'Serial Number',
        'comment': 'Instrument serial number.',
        # 'units': '',    deliberately left blank, no units for this value
    },
    'oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'an optode oxygen sensor. Computed on-board the sensor using internal calibration coefficients.'),
        'data_product_identifier': 'DOCONCS_L1'
    },
    'oxygen_saturation': {
        'long_name': 'Dissolved Oxygen Saturation',
        'units': 'percent',
        'comment': ('Oxygen saturation is the percentage of dissolved oxygen relative to the absolute solubility of '
                    'oxygen at a particular water temperature. Computed on-board the sensor using internal calibration '
                    'coefficients.')
    },
    'oxygen_thermistor_temperature': {
        'long_name': 'Optode Thermistor Temperature',
        'standard_name': 'temperature_of_sensor_for_oxygen_in_sea_water',
        'units': 'degrees_Celsius',
        'comment': ('Optode internal thermistor temperature used in calculation of the absolute oxygen '
                    'concentration. This is not the in-situ sea water temperature, though it will be very close.'),
        'ancillary_variables': 'raw_oxygen_thermistor'
    },
    'calibrated_phase': {
        'long_name': 'Calibrated Phase Difference',
        'units': 'degrees',
        'comment': ('The optode measures oxygen by exciting a special platinum porphyrin complex embedded in a '
                    'gas permeable foil with modulated blue light. The optode measures the phase shift of the '
                    'returned red light. By linearizing and temperature compensating, with an incorporated '
                    'temperature sensor, the absolute O2 concentration can be determined.'),
        'data_product_identifier': 'DOCONCS-VLT_L0'
    },
    'compensated_phase': {
        'long_name': 'Temperature Compensated Calibrated Phase Difference',
        'units': 'degrees',
        'comment': 'Temperature compensated (using the temperature data from an onboard thermistor) calibrated phase '
                   'difference.',
        'ancillary_variables': 'oxygen_thermistor_temperature, calibrated_phase'
    },
    'blue_phase': {
        'long_name': 'Blue Phase Measurement',
        'units': 'degree',
        'comment': ('Phase measurement with blue excitation light of the returned signal after the luminophore '
                    'quenching')
    },
    'red_phase': {
        'long_name': 'Red Phase Measurement',
        'units': 'degree',
        'comment': ('Phase measurement, with red excitation light, of the returned signal after the luminophore '
                    'quenching')
    },
    'blue_amplitude': {
        'long_name': 'Blue Amplitude Measurement',
        'units': 'mV',
        'comment': ('Amplitude measurement, with blue excitation light, of the returned signal after the luminophore '
                    'quenching')
    },
    'red_amplitude': {
        'long_name': 'Red Amplitude Measurement',
        'units': 'mV',
        'comment': ('Amplitude measurement, with red excitation light, of the returned signal after the luminophore '
                    'quenching')
    },
    'raw_oxygen_thermistor': {
        'long_name': 'Raw Optode Thermistor Temperature',
        'units': 'mV',
        'comment': ('The optode includes an integrated internal thermistor to measure the temperature at '
                    'the sensing foil.')
    },
    # dataset attributes --> interpolated in from a co-located CTD data
    'ctd_temperature': {
        'long_name': 'Sea Water Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('Sea water temperature is the in situ temperature of the sea water. Measurements are from a '
                    'co-located CTD'),
        'data_product_identifier': 'TEMPWAT_L1',
        '_FillValue': FILL_NAN
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
        '_FillValue': FILL_NAN
    },
    # dataset attributes --> derived values
    'svu_oxygen_concentration': {
        'long_name': 'Dissolved Oxygen Concentration',
        'standard_name': 'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
        'units': 'umol L-1',
        'comment': ('Mole concentration of dissolved oxygen per unit volume, also known as Molarity, as measured by '
                    'an optode oxygen sensor. Compares to the oxygen_concentration computed on-board the sensor, '
                    'but is recomputed using factory calibration coefficients, the calibrated phase values and '
                    'the optode thermistor temperature via the Stern-Volmer-Uchida equation.'),
        'data_product_identifier': 'DOCONCS_L1',
        'ancillary_variables': 'oxygen_thermistor_temperature, calibrated_phase',
        '_FillValue': FILL_NAN
    },
    'oxygen_concentration_corrected': {
        'long_name': 'Corrected Dissolved Oxygen Concentration',
        'standard_name': 'moles_of_oxygen_per_unit_mass_in_sea_water',
        'units': 'umol kg-1',
        'comments': ('The dissolved oxygen concentration from the Stable Response Dissolved Oxygen Instrument is a '
                     'measure of the concentration of gaseous oxygen mixed in seawater. This data product corrects '
                     'the dissolved oxygen concentration for the effects of salinity, temperature, and pressure with '
                     'data from a co-located CTD.'),
        'data_product_identifier': 'DOXYGEN_L2',
        'ancillary_variables': 'svu_oxygen_concentration, ctd_temperature, ctd_pressure, ctd_salinity, lat, lon',
        '_FillValue': FILL_NAN
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
        'units': 'count'
    },
    'measurement_wavelength_chl': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_chl': {
        'units': 'count'
    },
    'measurement_wavelength_cdom': {
        'long_name': 'Wavelength',
        'standard_name': 'radiation_wavelength',
        'units': 'nm'
    },
    'raw_signal_cdom': {
        'units': 'count'
    },
    'raw_internal_temp': {
        'units': 'count'
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
        'units': 'count'
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

CSPP_PARAD = {
    'global': {
        'title': 'uCSPP PAR Data Records',
        'summary': (
            'Records downwelling PAR data for the uncabled Coastal Surface Piercing Profilers'
        )
    },
    'raw_par': {
        'units': 'count'
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
        'units': 'count'
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
        'units': 'count'
    },
    'amplitude_beam2': {
        'units': 'count'
    },
    'amplitude_beam3': {
        'units': 'count'
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
        'units': 'count'
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
