
"""
Author: Julius Schaaf
Date: 2024-11-08
Version: 0.1.0
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def saturation_pressure_water(T_K,P,use_effective=True):
    """
    Calculate the saturation vapor pressure over water.
    
    Parameters:
    T_K (float): Temperature in Kelvin (0 °C to 100 °C)
    
    Returns:
    float: Saturation vapor pressure over water in Pa
    """
    # Coefficients for over water
    a = [-6.0969385e+3, 2.214409642e+1, -2.711193e-2, 1.673952e-5, 2.433502, 1]

    e_ws = math.exp(
        a[0] / T_K +
        a[1] +
        a[2] * T_K +
        a[3] * T_K**2 +
        a[4] * math.log(T_K*a[5])
      
    )
    # Apply enhancement factor if use_effective is True
    if use_effective:
        f_water = enhancement_factor_water(T_K, P, e_ws)  # Temperature in Celsius for enhancement factor
        e_ws *= f_water  # Effective saturation vapor pressure

    return e_ws

def saturation_pressure_ice(T_K,P, use_effective=True):
    """
    Calculate the saturation vapor pressure over ice.
    
    Parameters:
    T_K (float): Temperature in Kelvin (-100 °C to 0 °C)
    
    Returns:
    float: Saturation vapor pressure over ice in Pa
    """
    # Coefficients for over ice
    a = [-6.0245282e+3, 2.932707e+1, 1.0613868e-2, -1.3198825e-5, -4.9382577e-1, 1]

    e_is = math.exp(
        a[0] / T_K +
        a[1] +
        a[2] * T_K +
        a[3] * T_K**2 +
        a[4] * math.log(T_K) +
        a[5]
    )
    # Apply enhancement factor if use_effective is True
    if use_effective:
        f_water = enhancement_factor_water(T_K, P, e_is)  # Temperature in Celsius for enhancement factor
        e_is *= f_water  # Effective saturation vapor pressure

    return e_is

def saturation_vapor_pressure_water(t, P, use_effective=True):
    """
    Calculates the saturation vapor pressure over liquid water using the Hardy formula 
    valid -100...+100 °C using the ITS-90 standard. Returns effective saturation vapor pressure
    by default (with enchancement factor), but can return ideal pressure if use_effective is set to False.
    
    Parameters:
        t (float): Temperature in Kelvin.
        P (float): Total pressure in Pascals.
        use_effective (bool): Whether to use the effective saturation vapor pressure with the enhancement factor.

    Returns:
        float: Saturation vapor pressure in Pascals.
    """
    # Coefficients from the provided formula
    g = [
        -2.8365744e3,      # g0
        -6.028076559e3,    # g1
        1.954263612e1,     # g2
        -2.737830188e-2,   # g3
        1.6261698e-5,      # g4
        7.0229056e-10,     # g5
        -1.8680009e-13,    # g6
        2.7150305          # g7
    ]

    # Compute the sum from i=0 to 6 of g_i * t^(i-2)
    ln_E_sw = sum(g[i] * t**(i - 2) for i in range(7)) + g[7] * np.log(t)
    E_sw = np.exp(ln_E_sw)  # Ideal saturation vapor pressure over water

    # Apply enhancement factor if use_effective is True
    if use_effective:
        f_water = enhancement_factor_water(t, P, E_sw)  # Temperature in Celsius for enhancement factor
        E_sw *= f_water  # Effective saturation vapor pressure

    return E_sw

def saturation_vapor_pressure_ice(t, P, use_effective=True):
    """
    Calculates the saturation vapor pressure over ice using the Hardy formula 
    according to the ITS-90 standard. Valid in the range -100...0 °C. Returns effective
    saturation vapor pressure by default, but can return ideal pressure if use_effective is False.

    Parameters:
        t (float): Temperature in Kelvin.
        P (float): Total pressure in Pascals.
        use_effective (bool): Whether to use the effective saturation vapor pressure with the enhancement factor.

    Returns:
        float: Saturation vapor pressure over ice in Pascals.
    """
    # Coefficients for Hardy ITS-90 formula for ice
    g = [
        -5.8666426e3,      # k0
        2.232870244e1,     # k1
        1.39387003e-2,     # k2
        -3.4262402e-5,     # k3
        2.7040955e-8,      # k4
        6.7063522e-1       # k5 (for ln(T))
    ]

    # Compute the logarithm of saturation vapor pressure over ice
    ln_E_si = (g[0] / t) + g[1] + g[2] * t + g[3] * t**2 + g[4] * t**3 + g[5] * np.log(t)
    E_si = np.exp(ln_E_si)  # Ideal saturation vapor pressure over ice

    # Apply enhancement factor if use_effective is True
    if use_effective:
        f_ice = enhancement_factor_ice(t, P, E_si)
        E_si *= f_ice  # Effective saturation vapor pressure

    return E_si

def enhancement_factor_water(t, P, e_s, temperature_range="ITS-90 K"):
    """
    Calculates the enhancement factor for water over the temperature ranges
    -50 to 0°C or 0 to 100°C, based on the ITS-90 [K] coefficients.

    Parameters:
        t (float): Temperature in Kelvin.
        P (float): Pressure in the same units as e_s.
        e_s (float): Ideal saturation vapor pressure in the same units as P.
        temperature_range (str): The scale and range to use for coefficients.
                                 Options are "IPTS-68 C", "ITS-90 C", and "ITS-90 K".

    Returns:
        float: The enhancement factor for water.
    """

    # Corrected ITS-90 [K] coefficients for the specified temperature ranges
    coefficients = {
        "-50 to 0°C": {
            "ITS-90 K": {
                "A": [-5.5898101e-2, 6.7140389e-4, -2.7492721e-6, 3.8268958e-9],
                "B": [-8.1985393e1, 5.8230823e-1, -1.6340527e-3, 1.6725084e-6]
            }
        },
        "0 to 100°C": {
            "ITS-90 K": {
                "A": [-1.6302041e-1, 1.8071570e-3, -6.7703064e-6, 8.5813609e-9],
                "B": [-5.9890467e1, 3.4378043e-1, -7.7326396e-4, 6.3405286e-7]
            }
        }
    }

    # Select appropriate coefficients based on temperature range and scale
    if -50+273.15 <= t <= 273.15:
        A = coefficients["-50 to 0°C"][temperature_range]["A"]
        B = coefficients["-50 to 0°C"][temperature_range]["B"]
    elif 273.15 <= t <= 373.15:
        A = coefficients["0 to 100°C"][temperature_range]["A"]
        B = coefficients["0 to 100°C"][temperature_range]["B"]
    else:
        raise ValueError("Temperature out of range. Must be between -50 and 100°C.")

    # Calculate alpha and ln(beta)
    alpha = sum(A[i] * t**i for i in range(4))
    ln_beta = sum(B[i] * t**i for i in range(4))
    beta = np.exp(ln_beta)

    # Calculate the enhancement factor f
    f = np.exp(alpha * (1 - e_s / P) + beta * (P / e_s - 1))
    
    return f


def enhancement_factor_ice(t, P, e_s, temperature_range="ITS-90 K", coef="wide"):
    """
    Calculates the enhancement factor for ice over the temperature ranges
    -100 to -50°C, or -50 to 0°C, based on the ITS-90 [K] "narrow" coefficients.
    
    If coef. variable is set to wide uses the coefficients between -100 to 0°C 
    with more error. 

    Parameters:
        t (float): Temperature in Kelvin.
        P (float): Pressure in the same units as e_s.
        e_s (float): Ideal saturation vapor pressure in the same units as P.
        temperature_range (str): The scale and range to use for coefficients.
                                 Options are "IPTS-68 C", "ITS-90 C", and "ITS-90 K".

    Returns:
        float: The enhancement factor for ice.
    """

    # ITS-90 [K] coefficients for the specified temperature ranges
    coefficients = {
        "-100 to 0°C": {
            "ITS-90 K": {
                "A": [-6.0190570e-2, 7.3984060e-4, -3.0897838e-6, 4.3669918e-9],
                "B": [-9.4868712e1, 7.2392075e-1, -2.1963437e-3, 2.4668279e-6]
            }
        },
        "-100 to -50°C": {
            "ITS-90 K": {
                "A": [-7.4712663e-2, 9.5972907e-4, -4.1935419e-6, 6.2038841e-9],
                "B": [-1.0385289e2, 8.5783626e-1, -2.8578612e-3, 3.5499292e-6]
            }
        },
        "-50 to 0°C": {
            "ITS-90 K": {
                "A": [-7.1044201e-2, 8.6786223e-4, -3.5912529e-6, 5.0194210e-9],
                "B": [-8.2308868e1, 5.6519110e-1, -1.5304505e-3, 1.5395086e-6]
            }
        }
    }
    if coef =="narrow":
        # Select appropriate coefficients based on temperature range
        if 173.15 <= t < 273.15-50:
            A = coefficients["-100 to -50°C"][temperature_range]["A"]
            B = coefficients["-100 to -50°C"][temperature_range]["B"]
        elif 273.15-50 <= t <= 273.15:
            A = coefficients["-50 to 0°C"][temperature_range]["A"]
            B = coefficients["-50 to 0°C"][temperature_range]["B"]
        else:
            raise ValueError("Temperature out of range. Must be between -100 and 0°C.")
    elif 173.15 <= t <= 273.15:
        A = coefficients["-100 to 0°C"][temperature_range]["A"]
        B = coefficients["-100 to 0°C"][temperature_range]["B"]
    else:
        raise ValueError("Temperature out of range. Must be between -100 and 0°C.")

    # Calculate alpha and ln(beta)
    alpha = sum(A[i] * t**i for i in range(4))
    ln_beta = sum(B[i] * t**i for i in range(4))
    beta = np.exp(ln_beta)

    # Calculate the enhancement factor f
    f = np.exp(alpha * (1 - e_s / P) + beta * (P / e_s - 1))
    
    return f



def dew_point_temperature(P_vapor, P):
    """
    Calculates the dew point temperature for a given water vapor partial pressure 
    using a root-finding algorithm. 

    Parameters:
        P_vapor (float): Partial pressure of water vapor in Pascals.

    Returns:
        float: Dew point temperature in Kelvin.
    """
    def func(t):
        return saturation_vapor_pressure_water(t, P) - P_vapor
    # Temperature bounds (in Kelvin)
    t_lower = 273.15+50  # -100°C
    t_upper = 273.15  # 100°C
    try:
        t_dp = brentq(func, t_lower, t_upper)
        return t_dp
    except ValueError:
        return np.nan  # Return NaN if no solution is found within bounds
    
def frost_point_temperature(P_vapor, P_total):
    """
    Calculates the frost point temperature for a given water vapor partial pressure 
    using a root-finding algorithm.
    
    Parameters:
        P_vapor (float): Partial pressure of water vapor in Pascals.

    Returns:
        float: Frost point temperature in Kelvin.
    """
    def func(t):
        return saturation_vapor_pressure_ice(t, P_total) - P_vapor  # Use effective saturation vapor pressure over ice

    # Temperature bounds (in Kelvin)
    t_lower = 173.15  # -100°C
    t_upper = 273.15  # 0°C
    try:
        t_fp = brentq(func, t_lower, t_upper)
        return t_fp
    except ValueError:
        return np.nan  # Return NaN if no solution is found within bounds
    
def relative_humidity(p_w, t_k, over_ice=False):
    """
    Calculate the relative humidity (RH) over water or ice.

    Parameters:
    p_w (float): Partial pressure of water vapor in Pa.
    t_k (float): Temperature in Kelvin.
    over_ice (bool): If True, calculate RH over ice; otherwise, over water.

    Returns:
    float: Relative humidity (RH) as a percentage.
    """
    if over_ice:
        # Calculate saturation vapor pressure over ice
        p_is = saturation_pressure_ice(t_k)
        rh_i = (p_w / p_is) * 100  # Relative humidity over ice
        return rh_i
    else:
        # Calculate saturation vapor pressure over water
        p_ws = saturation_pressure_water(t_k)
        rh = (p_w / p_ws) * 100  # Relative humidity over water
        return rh

def calculate_absolute_humidity(p_w, t_k):
    """
    Calculate absolute humidity (A) in g/m³.

    Parameters:
    p_w (float): Vapor pressure of water in Pa.
    t_k (float): Temperature in Kelvin.

    Returns:
    float: Absolute humidity in g/m³.
    """
    # Constants
    M_H2O = 18.01528  # Molar mass of water in g/mol
    R = 8.3145  # Universal gas constant in J/(K·mol)

    # Calculate absolute humidity
    absolute_humidity = (M_H2O * p_w) / (R * t_k)
    return absolute_humidity

def calculate_mixing_ratio(p_w, p_total):
    """
    Calculate the mixing ratio (x) in g_H2O/kg_dry_gas.

    Parameters:
    p_w (float): Vapor pressure of water in Pa.
    p_total (float): Total pressure (dry gas + water vapor) in Pa.

    Returns:
    float: Mixing ratio in g_H2O/kg_dry_gas.
    """
    # Constants
    M_H2O = 18.0154  # Molecular weight of water in g/mol
    M_gas = 28.965  # Molecular weight of dry air in g/mol

    # Calculate B
    B = (M_H2O / M_gas) * 1000  # Convert to g/kg

    # Calculate mixing ratio
    if p_total > p_w:
        mixing_ratio = B * (p_w / (p_total - p_w))
    else:
        raise ValueError("Total pressure must be greater than vapor pressure.")

    return mixing_ratio

def calculate_enthalpy(mixing_ratio, temperature_c):
    """
    Calculate the specific enthalpy (h) of water vapor in kJ/kg.

    Parameters:
    mixing_ratio (float): Mixing ratio (x) in g_H2O/kg_dry_gas.
    temperature_c (float): Temperature in Celsius (T).

    Returns:
    float: Specific enthalpy (h) in kJ/kg.
    """
    # Constants
    C_pg = 1.006  # Specific heat capacity of dry air at constant pressure (kJ/(kg·°C))
    C_pw = 1.84   # Specific heat capacity of water vapor at constant pressure (kJ/(kg·°C))
    h_we = 2501   # Evaporation heat of water at 0°C (kJ/kg)

    # Calculate enthalpy
    h = C_pg * temperature_c + (mixing_ratio / 1000) * (C_pw * temperature_c + h_we)
    return h

def calculate_ppm_vdry(p_w, p_total):
    """
    Calculate ppm (volume H2O/volume dry) using vapor pressure.
    
    Parameters:
    p_w (float): Vapor pressure of water in Pa.
    p_total (float): Total pressure in Pa.
    
    Returns:
    float: ppm_vdry.
    """
    return (p_w / (p_total - p_w)) * 1e6


def calculate_ppm_mdry(p_w, p_total):
    """
    Calculate ppm (mass H2O/mass dry) using vapor pressure.
    
    Parameters:
    p_w (float): Vapor pressure of water in Pa.
    p_total (float): Total pressure in Pa.
    
    Returns:
    float: ppm_mdry.
    """
    M_H2O = 18.0146  # Molecular weight of water in g/mol
    M_gas = 28.965  # Molecular weight of dry gas (air) in g/mol
    return (M_H2O * p_w) / (M_gas * (p_total - p_w)) * 1e6


def calculate_ppm_vwet(p_w, p_total):
    """
    Calculate ppm (volume H2O/volume wet) using vapor pressure.
    
    Parameters:
    p_w (float): Vapor pressure of water in Pa.
    p_total (float): Total pressure in Pa.
    
    Returns:
    float: ppm_vwet.
    """
    return (p_w / p_total) * 1e6


def calculate_ppm_mwet(p_w, p_total):
    """
    Calculate ppm (mass H2O/mass wet) using vapor pressure.
    
    Parameters:
    p_w (float): Vapor pressure of water in Pa.
    p_total (float): Total pressure in Pa.
    
    Returns:
    float: ppm_mwet.
    """
    M_H2O = 18.0146  # Molecular weight of water in g/mol
    M_gas = 28.965  # Molecular weight of dry gas (air) in g/mol
    return (M_H2O * p_w) / (M_gas * p_total) * 1e6


#conversion formulas to imperial units
def celsius_to_fahrenheit(t_c):
    """
    Convert Celsius to Fahrenheit.
    
    Parameters:
    t_c (float): Temperature in Celsius.
    
    Returns:
    float: Temperature in Fahrenheit.
    """
    return (t_c * 9/5) + 32


def pa_to_psi(p_pa):
    """
    Convert pressure from Pascals to pounds per square inch (psi).
    
    Parameters:
    p_pa (float): Pressure in Pascals (Pa).
    
    Returns:
    float: Pressure in psi.
    """
    return p_pa / 6894.76


def absolute_humidity_to_grains_per_cubic_foot(a_g_kg):
    """
    Convert absolute humidity from g/m³ to grains per cubic foot.
    
    Parameters:
    a_g_kg (float): Absolute humidity in g/m³.
    
    Returns:
    float: Absolute humidity in grains per cubic foot.
    """
    return 2.2883 * a_g_kg


def mixing_ratio_to_grains_per_pound(x_g_kg):
    """
    Convert mixing ratio from g/kg to grains per pound.
    
    Parameters:
    x_g_kg (float): Mixing ratio in g/kg.
    
    Returns:
    float: Mixing ratio in grains per pound.
    """
    return 0.14286 * x_g_kg


def enthalpy_to_btu_per_pound(h_kj_kg):
    """
    Convert enthalpy from kJ/kg to BTU per pound.
    
    Parameters:
    h_kj_kg (float): Enthalpy in kJ/kg.
    
    Returns:
    float: Enthalpy in BTU per pound.
    """
    return 2.324 * h_kj_kg

