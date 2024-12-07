# utilities.py

from .constants import API_TO_SG_CONVERSION, API_TO_SG_OFFSET, TEMPERATURE_OFFSET_RANKINE

def api_to_specific_gravity(API):
    """
    Convert API gravity to specific gravity.

    Parameters:
        API (float): Oil gravity, °API

    Returns:
        float: Specific gravity of the oil
    """
    return API_TO_SG_CONVERSION / (API_TO_SG_OFFSET + API)

def fahrenheit_to_rankine(temperature_f):
    """
    Convert temperature from Fahrenheit to Rankine.

    Parameters:
        temperature_f (float): Temperature in °F

    Returns:
        float: Temperature in °R
    """
    return temperature_f + TEMPERATURE_OFFSET_RANKINE
