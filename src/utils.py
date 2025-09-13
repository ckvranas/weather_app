"""Helper methods to inspect the GET response"""
from __future__ import annotations
from typing import TYPE_CHECKING
from packet_api_client.api.default import update_packet, get_packets
from datetime import datetime

if TYPE_CHECKING:
    from packet_api_client.models import Packet 
    from packet_api_client import Client

def inspect_correct_packets(
    client: Client, 
    station_id: int = -1, 
    datetime: datetime | None = None
) -> None:
    """
    Inspects the response from a GET /packets request to ensure that all Packet objects have the correct type for each field.
    
    If the response is not None, it will iterate over each Packet in the response and call inspect_packet_type_fields and correct_packet_invalid_values on each one.
    This function will also attempt to update the packets through the API if they have invalid values.
    """
    try:
        response = get_packets.sync(client=client, station_id=station_id)
    except Exception as e:
        print(f"Error for API call getting packets: {e}")
        return
    # If we have one packet at least from the query then we can inspect it
    if response is not None:
        for packet in response:
            # Check the types of the fields in the packet
            inspect_packet_type_fields(packet)
            # Check if the packet has invalid values
            is_corrected = correct_packet_invalid_values(packet)
            # If the packet has invalid values, update it through the API
            if is_corrected:
                try:
                    update_packet.sync(
                        client=client,
                        packet_id=packet.id,
                        body=packet
                    )
                except Exception as e:
                    print(f"Error for API call updating packet: {e}")
                    return
        

def inspect_packet_type_fields(packet: Packet) -> None:
    """
    Checks that all fields of a Packet object have the correct type.
    
    It asserts that the datetime field is a datetime object, station_id is an integer, temperature_celsium and moisture percentage are floats, wind_speed_kmh is a float, wind_direction is one of 'south', 'north', 'west', 'east', and rain_meas_mm is a float.
    """
    assert isinstance(packet.datetime_, datetime), "Packet datetime should be a datetime object"
    assert isinstance(packet.station_id, int),   "Packet station_id should be an integer"
    assert isinstance(packet.temperature_celsium, float), "Packet temperature_celsium should be a float"
    assert isinstance(packet.moisture_perc, float), "Packet moisture percentage should be a float"
    assert isinstance(packet.wind_speed_kmh, float), "Packet wind_speed_kmh should be a float"
    assert packet.wind_direction in ("south", "north", "west", "east"), "Packet wind_direction should be one of 'south', 'north', 'west', 'east'"
    assert isinstance(packet.rain_meas_mm, float), "Packet rain_meas_mm should be a float"

def correct_packet_invalid_values(packet: Packet) -> bool:
    """
    Corrects invalid values in a Packet object.

    Checks if the moisture percentage, wind speed and rain measurement values are valid.
    If they are not, it sets them to the closest valid value.

    Packet is going to be updated without returning it. Only is_corrected is returned

    Assumed that only moisture percentage, wind speed and rain measurement values can take invalid values
    """
    is_corrected = False
    if packet.moisture_perc <= 0.0:
        packet.moisture_perc = 0.0
        is_corrected = True
    elif packet.moisture_perc >= 100.0:
        packet.moisture_perc = 100.0
        is_corrected = True
    if packet.wind_speed_kmh < 0.0:
        packet.wind_speed_kmh = 0.0
        is_corrected = True
    if packet.rain_meas_mm < 0.0:
        packet.rain_meas_mm =  0.0
        is_corrected = True
    return is_corrected