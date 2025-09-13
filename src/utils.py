"""Helper methods to inspect the GET response"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import datetime
if TYPE_CHECKING:
    from packet_api_client.models import Packet 

def inspect_response(response: Optional[list[Packet]]) -> None:
    """
    Inspects the response from a GET /packets request to ensure that all Packet objects have the correct type for each field.
    If the response is not None, it will iterate over each Packet in the response and call inspect_packet_type_fields and correct_packet_invalid_values on each one.
    """
    if response is not None:
       for packet in response:
           inspect_packet_type_fields(packet)
           packet = correct_packet_invalid_values(packet)


def inspect_packet_type_fields(packet: Packet) -> None:
    """
    Checks that all fields of a Packet object have the correct type.
    
    It asserts that the datetime field is a datetime object, station_id is an integer, temperature_celsium and moisture percentage are floats, wind_speed_kmh is a float, wind_direction is one of 'south', 'north', 'west', 'east', and rain_meas_mm is a float.
    """
    assert isinstance(packet.datetime, datetime.datetime), "Packet datetime should be a datetime object"
    assert isinstance(packet.station_id, int),   "Packet station_id should be an integer"
    assert isinstance(packet.temperature_celsium, float), "Packet temperature_celsium should be a float"
    assert isinstance(packet.moisture_perc, float), "Packet moisture percentage should be a float"
    assert isinstance(packet.wind_speed_kmh, float), "Packet wind_speed_kmh should be a float"
    assert isinstance(packet.wind_direction, ("south", "north", "west", "east")), "Packet wind_direction should be one of 'south', 'north', 'west', 'east'"
    assert isinstance(packet.rain_meas_mm, float), "Packet rain_meas_mm should be a float"

def correct_packet_invalid_values(packet: Packet) -> Packet:
    """
    Corrects invalid values in a Packet object.

    Checks if the moisture percentage, wind speed and rain measurement values are valid.
    If they are not, it sets them to the closest valid value.

    Assumed that only moisture percentage, wind speed and rain measurement values can take invalid values
    """
    if packet.moisture_perc <= 0.0:
        packet.moisture_perc = 0.0
    elif packet.moisture_perc >= 100.0:
        packet.moisture_perc = 100.0
    packet.wind_speed_kmh = packet.wind_speed_kmh if packet.wind_speed_kmh > 0.0 else 0.0
    packet.rain_meas_mm = packet.rain_meas_mm if packet.rain_meas_mm > 0.0 else 0.0
    return packet