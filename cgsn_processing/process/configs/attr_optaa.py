#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.configs.attr_optaa
@file cgsn_processing/process/configs/attr_optaa.py
@author Christopher Wingard
@brief Attributes for the OPTAA variables
"""
import numpy as np
from cgsn_processing.process.common import FILL_INT

OPTAA = {
    # global attributes and metadata variables and attributes
    'global': {
        'title': 'Optical Absorbance and Attenuation from OPTAA',
        'summary': ('Measures the absorabance and attenuation of particulate and dissolved organic matter with '
                    'the Sea-Bird Scientific Spectral Absorption and Attenuation Sensor (AC-S).')
    },
    # parsed (raw) variables and attributes
    'serial_number': {
        'long_name': 'Unit Serial Number',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'pressure_raw': {
        'long_name': 'Raw Pressure',
        'units': 'counts',
        'comment': ('Raw measurements, reported in counts, from the AC-S pressure sensor. If the unit is not '
                    'equipped with a pressure sensor, the values will all be 0.')
    },
    'external_temp_raw': {
        'long_name': 'Raw In-Situ Temperature',
        'units': 'counts',
        'data_product_identifier': 'OPTTEMP_L0',
        'comment': ('Raw measurements, reported in counts, from the AC-S external temperature sensor. This sensor '
                    'measures the in-situ seawater termperature.')
    },
    'internal_temp_raw': {
        'long_name': 'Raw Internal Instrument Temperature',
        'units': 'counts',
        'comment': ('Raw measurements, reported in counts, from the AC-S internal temperature sensor. This sensor '
                    'measures the internal instrument termperature and is used in converting the raw optical '
                    'measurements into absorbance and attenuation estimates.')
    },
    'elapsed_run_time': {
        'long_name': 'Elapsed Run Time',
        'units': 'ms',
        'comment': 'Time in milliseconds since the instrument was powered on.'
    },
    'wavelength_number': {
        'long_name': 'Wavelength Number',
        'units': 'count',
        'comment': ('An index counter between 0 and 99 used to set a common length dimension for the absorbance and '
                    'attenuation measurements. The actual number of wavelengths is variable between sensors '
                    'and may even change for a particular sensor over time if servicing requires a replacement '
                    'of the filter set. The actual number of wavelengths for this sensor is represented here '
                    'by the attribute actual_wavelengths.')
        # 'actual_wavelengths': ''  # deliberately left blank, created during the processing
    },
    'a_wavelengths': {
        'long_name': 'A Channel Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
        'comment': ('Absorbance channel measurement wavelengths, specific to the filter wheel set installed in '
                    'the AC-S.'),
        '_FillValue': np.nan
    },
    'a_reference_dark': {
        'long_name': 'A Channel Dark Reference',
        'units': 'counts',
        'comment': ('A channel reference detector dark counts (before the lamp is turned on). Used in conversion '
                    'of the raw a channel measurements to absorbance estimates.')
    },
    'a_reference_raw': {
        'long_name': 'A Channel Raw Reference',
        'units': 'counts',
        'comment': ('A channel reference detector raw counts (while the lamp is turned on). Used in conversion '
                    'of the raw a channel measurements to absorbance estimates.'),
        'data_product_identifier': 'OPTAREF_L0',
        '_FillValue': FILL_INT
    },
    'a_signal_dark': {
        'long_name': 'A Channel Dark Signal',
        'units': 'counts',
        'comment': ('A channel signal detector dark counts (before the lamp is turned on). Used in conversion '
                    'of the raw a channel measurements to absorbance estimates.')
    },
    'a_signal_raw': {
        'long_name': 'A Channel Raw Signal',
        'units': 'counts',
        'comment': ('A channel signal detector raw counts (while the lamp is turned on). Used in conversion '
                    'of the raw a channel measurements to absorbance estimates.'),
        'data_product_identifier': 'OPTASIG_L0',
        '_FillValue': FILL_INT
    },
    'c_wavelengths': {
        'long_name': 'C Channel Wavelengths',
        'standard_name': 'radiation_wavelength',
        'units': 'nm',
        'comment': ('Attenuation channel measurement wavelengths, specific to the filter wheel set installed in '
                    'the AC-S.'),
        '_FillValue': np.nan
    },
    'c_reference_dark': {
        'long_name': 'C Channel Dark Reference',
        'units': 'counts',
        'comment': ('C channel reference detector dark counts (before the lamp is turned on). Used in conversion '
                    'of the raw c channel measurements to attenuation estimates.')
    },
    'c_reference_raw': {
        'long_name': 'C Channel Raw Reference',
        'units': 'counts',
        'comment': ('C channel reference detector raw counts (while the lamp is turned on). Used in conversion '
                    'of the raw c channel measurements to attenuation estimates.'),
        'data_product_identifier': 'OPTCREF_L0',
        '_FillValue': FILL_INT
    },
    'c_signal_dark': {
        'long_name': 'C Channel Dark Signal',
        'units': 'counts',
        'comment': ('C channel signal detector dark counts (before the lamp is turned on). Used in conversion '
                    'of the raw c channel measurements to attenuation estimates.')
    },
    'c_signal_raw': {
        'long_name': 'C Channel Raw Signal',
        'units': 'counts',
        'comment': ('C channel signal detector raw counts (while the lamp is turned on). Used in conversion '
                    'of the raw c channel measurements to attenuation estimates.'),
        'data_product_identifier': 'OPTCSIG_L0',
        '_FillValue': FILL_INT
    },

    # Data from a co-located CTD, if available, interpolated into the data set
    'ctd_pressure': {
        'long_name': 'Sea Water Pressure',
        'standard_name': 'sea_water_pressure_due_to_sea_water',
        'units': 'dbar',
        'comment': ('Sea Water Pressure refers to the pressure exerted on a sensor in situ by the weight of the ' 
                    'column of seawater above it. It is calculated by subtracting one standard atmosphere from the ' 
                    'absolute pressure at the sensor to remove the weight of the atmosphere on top of the water ' 
                    'column. The pressure at a sensor in situ provides a metric of the depth of that sensor. '
                    'Measurements are from a co-located CTD.'),
        'data_product_identifier': 'PRESWAT_L1',
        '_FillValue': np.nan
    },
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

    # Derived values in the processed data set
    'pressure': {
        'long_name': 'Pressure',
        'units': 'dbar',
        'comment': ('Seawater pressure, measured at the top of the pressure housing. If the unit is not equipped '
                    'with a pressure sensor, the values will be filled with a NaN.'),
        'ancillary_variables': 'pressure_raw',
        '_FillValue': np.nan
    },
    'external_temp': {
        'long_name': 'External Instrument Temperature',
        'standard_name': 'sea_water_temperature',
        'units': 'degrees_Celsius',
        'comment': ('In-situ sea water temperature measurements from the sensor mounted at the top of the '
                    'AC-S pressure housing.'),
        'ancillary_variables': 'external_temp_raw'
    },
    'internal_temp': {
        'long_name': 'Internal Instrument Temperature',
        'units': 'degrees_Celsius',
        'comment': 'Internal instrument temperature, used to convert raw absorbance and attenuation measurements.',
        'ancillary_variables': 'internal_temp_raw'
    },
    'apd': {
        'long_name': 'Particulate and Dissolved Absorbance',
        'units': 'm-1',
        'comment': ('The optical absorption coefficient is the rate that the intensity of a beam of light will '
                    'decrease in response to the absorption (removal) of light energy as a function of propagation '
                    'distance. The optical absorption coefficient reflects the absorption coefficient for the '
                    'combination of all seawater impurities including all particulate and dissolved matter of '
                    'optical importance.'),
        'ancillary_variables': ('a_wavelengths internal_temp a_signal_raw a_reference_raw '
                                'a_signal_dark a_reference_dark'),
        '_FillValue': np.nan
    },
    'apd_ts': {
        'long_name': 'Particulate and Dissolved Absorbance with TS Correction',
        'units': 'm-1',
        'comment': ('The optical absorption coefficient corrected for the effects of temperature and salinity. '
                    'This dataset assumes a constant salinity of 33 psu, given the overall negligible effects of '
                    'salinity (as opposed to temperature) on the absorption coefficient.'),
        'ancillary_variables': 'a_wavelengths external_temp apd',
        '_FillValue': np.nan
    },
    'apd_ts_s': {
        'long_name': 'Particulate and Dissolved Absorbance with TS and Scatter Correction',
        'units': 'm-1',
        'comment': ('The optical absorption coefficient corrected for the effects of temperature and salinity, '
                    'with the baseline effects due to scattering at 715 nm removed.'),
        'data_product_identifier': 'OPTABSN_L2',
        'ancillary_variables': 'a_wavelengths apd_ts',
        '_FillValue': np.nan
    },
    'cpd': {
        'long_name': 'Particulate and Dissolved Attenuation',
        'units': 'm-1',
        'comment': ('The optical beam attenuation coefficient is the rate that the intensity of a beam of light will '
                    'decrease in response to the combined effects of absorption and scatter as a function of '
                    'propagation distance. The attenuation coefficient results from the spectral beam attenuation of '
                    'the combination of all seawater impurities including all particulate and dissolved matter of '
                    'optical importance.'),
        'ancillary_variables': ('c_wavelengths internal_temp c_signal_raw c_reference_raw '
                                'c_signal_dark c_reference_dark'),
        '_FillValue': np.nan
    },
    'cpd_ts': {
        'long_name': 'Particulate and Dissolved Attenuation with TS Correction',
        'units': 'm-1',
        'comment': ('The optical beam attenuation coefficient corrected for the effects of temperature and salinity. '
                    'This dataset assumes a constant salinity of 33 psu, given the overall negligible effects of '
                    'salinity (as opposed to temperature) on the attenuation coefficient.'),
        'data_product_identifier': 'OPTATTN_L2',
        'ancillary_variables': 'c_wavelengths external_temp cpd',
        '_FillValue': np.nan
    },
    'estimated_chlorophyll': {
        'long_name': 'Estimated Chlorophyll Concentration',
        'standard_name': 'mass_concentration_of_chlorophyll_in_sea_water',
        'units': 'ug L-1',
        'comment': ('Uses the absorption line height at 676 nm, above a linear background between 650 and 715 nm with '
                    'a chlorophyll specific absorption of 0.020 L/ug/m, to estimate the concentration of chlorophyll. '
                    'This method has been shown to be significantly related to extracted chlorophyll concentrations '
                    'and is robust in response to mild to moderate biofouling.'),
        'ancillary_variables': 'apd_ts_s',
        '_FillValue': np.nan
    },
    'estimated_poc': {
        'long_name': 'Estimated POC Concentration',
        'standard_name': 'mass_concentration_of_organic_detritus_expressed_as_carbon_in_sea_water',
        'units': 'ug L-1',
        'comment': ('Uses the particulate beam attenuation coefficient at 660 nm and a coefficient of 380 ug/L/m. This '
                    'calculation is not robust in response to biofouling and is expected to breakdown as biofouling '
                    'begins to dominate the signal.'),
        'ancillary_variables': 'cpd_ts',
        '_FillValue': np.nan
    },
    'ratio_cdom': {
        'long_name': 'CDOM to Chlorophyll Absorbance Ratio',
        'units': '1',
        'comment': ('Ratio of CDOM absorption in the violet portion of the spectrum at 412 nm relative to '
                    'chlorophyll absorption at 440 nm. Ratios greater than 1 indicate a preponderance of CDOM '
                    'absorption relative to chlorophyll.'),
        'ancillary_variables': 'apd_ts_s',
        '_FillValue': np.nan
    },
    'ratio_carotenoids': {
        'long_name': 'Carotenoid to Chlorophyll Absorbance Ratio',
        'units': '1',
        'comment': ('Ratio of carotenoid absorption in the blue-green portion of the spectrum at 490 nm relative to '
                    'chlorophyll absorption at 440 nm. A changing carotenoid to chlorophyll ratio may indicate a shift '
                    'in phytoplankton community composition in addition to changes in light history or bloom health '
                    'and age.'),
        'ancillary_variables': 'apd_ts_s',
        '_FillValue': np.nan
    },
    'ratio_phycobilins': {
        'long_name': 'Phycobilins to Chlorophyll Absorbance Ratio',
        'units': '1',
        'comment': ('Ratio of phycobilin absorption in the green portion of the spectrum at 530 nm relative to '
                    'chlorophyll absorption at 440 nm. Different phytoplankton, notably cyanobacteria, utilize '
                    'phycobilins as accessory light harvesting pigments. An increasing phycobilin to chlorophyll ratio '
                    'may indicate a shift in phytoplankton community composition.'),
        'ancillary_variables': 'apd_ts_s',
        '_FillValue': np.nan
    },
    'ratio_qband': {
        'long_name': 'Chlorophyll Q Band to Soret Band Absorbance Ratio',
        'units': '1',
        'comment': ('The Soret and the Q bands represent the two main absorption bands of chlorophyll. The former '
                    'covers absorption in the blue region of the spectrum, while the latter covers absorption in the '
                    'red region. A decrease in the ratio of the intensity of the Soret band at 440 nm to that of the Q '
                    'band at 676 nm may indicate a change in phytoplankton community structure. All phytoplankton '
                    'contain chlorophyll a as the primary light harvesting pigment, but green algae and '
                    'dinoflagellates contain chlorophyll b and c, respectively, which are spectrally redshifted '
                    'compared to chlorophyll a.'),
        'ancillary_variables': 'apd_ts_s',
        '_FillValue': np.nan
    }
}
