from .utilities import api_to_specific_gravity, fahrenheit_to_rankine

def calculate_bubble_point_pressure(Rs, SGg, T, API):
    Pb = 18.2 * ((Rs / SGg) ** 0.83) * 10 ** (0.00091 * T - 0.0125 * API)
    return Pb

def calculate_solution_gas_oil_ratio(Pb, SGg, T, API):
    Rs = SGg * ((Pb / (18.2 * 10 ** (0.00091 * T - 0.0125 * API))) ** (1 / 0.83))
    return Rs

def calculate_oil_formation_volume_factor(Rs, SGg, API, T):
    SGo = api_to_specific_gravity(API)
    Bo = 0.9759 + 0.00012 * ((Rs * (SGg / SGo) ** 0.5 + 1.25 * T) ** 1.2)
    return Bo

def calculate_oil_viscosity(API, T, Rs):
    SGo = api_to_specific_gravity(API)
    dead_oil_viscosity = 10 ** (10 ** (3.0324 - 0.02023 * API) - 1.163)
    live_oil_viscosity = dead_oil_viscosity * (10 ** (-3.9 * (Rs / (2.6 * SGo ** 0.5 + T)) ** 0.2))
    return live_oil_viscosity

def calculate_gas_formation_volume_factor(P, T, Z):
    T_rankine = fahrenheit_to_rankine(T)
    Bg = 0.02827 * Z * T_rankine / P
    return Bg

def calculate_gas_viscosity(T, P, SGg):
    T_rankine = fahrenheit_to_rankine(T)
    T_k = (T_rankine - 460) * 5 / 9  # Convert to Kelvin
    x = (9.379 + 0.01607 * SGg * T_k) * (1 + 0.001083 * P)
    y = 3.448 + 986.4 / T_k + 0.01009 * SGg
    z = 2.447 - 0.2224 * y
    gas_viscosity = (10 ** (-x)) * (10 ** z)
    return gas_viscosity

def calculate_oil_compressibility(Pb, P):
    if P < Pb:
        Co = 0.00001 * (Pb - P) ** 0.5
    else:
        Co = 0.0
    return Co

def calculate_gas_compressibility(P, T, Z):
    T_rankine = fahrenheit_to_rankine(T)
    Cg = 1 / P - (1 / Z) * (Z - 1) / T_rankine
    return Cg
