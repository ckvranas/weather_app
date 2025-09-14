import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from packet_api_client.models import Packet
from weather_app.utils import inspect_correct_packets
from packet_api_client import Client

@pytest.fixture
def client() -> Client:
    """
    Returns a Client object, which can be used to call the API methods.
    """
    return Client()

@pytest.fixture
def mock_get_packets():
    """
    Returns a mock object for the get_packets function.
    """
    return Mock()

@pytest.fixture
def mock_update_packet():
    """
    Returns a mock object for the update_packet function.
    """
    return Mock()

# Any call of the get and update sync methods will be redirected to the mock functions
@patch('packet_api_client.api.default.update_packet.sync')
@patch('packet_api_client.api.default.get_packets.sync')
def test_none_packets(mock_get_packets: Mock, mock_update_packet: Mock) -> None:
    """
    Tests that inspect_correct_packets does not call update_packet when there are no packets in the response.

    Args:
        mock_update_packet (Mock): A mock object for the update_packet method.
        mock_get_packets (Mock): A mock object for the get_packets method.
    """
    # Note that inspect_correct_packets may update the packet due to the correction functionality if invalid values
    mock_get_packets.return_value = None
    inspect_correct_packets(client)
    # Check if get_packets was called with the correct parameters
    mock_get_packets.assert_called_once_with(client=client, station_id=-1)
    assert mock_update_packet.call_count == 0, "update_packet should not be called"
    assert mock_get_packets.return_value == None, "get_packets should return None"

@patch('packet_api_client.api.default.update_packet.sync')
@patch('packet_api_client.api.default.get_packets.sync')
def test_valid_packets(mock_get_packets: Mock, mock_update_packet: Mock):
    """
    Tests that inspect_correct_packets does not call update_packet when there are valid packets in the response.

    Args:
        mock_update_packet (Mock): A mock object for the update_packet method.
        mock_get_packets (Mock): A mock object for the get_packets method.
    """
    init_packet = Packet(id=1, 
                     datetime_=datetime.now(), 
                     station_id=1, 
                     temperature_celsius=25.5, 
                     moisture_perc=50.0, 
                     wind_speed_kmh=10.3, 
                     wind_direction="north",
                     rain_meas_mm=10.0)
                     
    mock_get_packets.return_value = [init_packet]
    # Note that inspect_correct_packets may update the packet due to the correction functionality if invalid values
    inspect_correct_packets(client, station_id=1)
    # Check if get_packets was called with the correct parameters
    mock_get_packets.assert_called_once_with(client=client, station_id=1)
    assert mock_update_packet.call_count == 0, "update_packet should not be called"
    assert mock_get_packets.return_value == [init_packet], "get_packets should return the initial packet"

@patch('packet_api_client.api.default.update_packet.sync')
@patch('packet_api_client.api.default.get_packets.sync')
def test_invalid_and_correct_packets(mock_get_packets: Mock, mock_update_packet: Mock):
    """
    Tests that inspect_correct_packets updates the packet with invalid values.

    This function creates a packet with invalid rain meas (negative), and then calls inspect_correct_packets.
    It asserts that get_packets is called with the correct parameters. Then update_packet is called with the correct parameters,
    and that the return value of get_packets is the updated packet.

    mock_update_packet: A mock object for the update_packet method.
    mock_get_packets: A mock object for the get_packets method.
    """
    ref_detatime = datetime.now()
    init_packet = Packet(id=1, 
                     datetime_=ref_detatime, 
                     station_id=1, 
                     temperature_celsius=25.5, 
                     moisture_perc=50.0, 
                     wind_speed_kmh=10.3, 
                     wind_direction="north",
                     rain_meas_mm=-10.0)
    mock_get_packets.return_value = [init_packet] 
    # Note that inspect_correct_packets may update the packet due to the correction functionality if invalid values
    # Function updates mock_get_packets.return_value (rain_meas_mm -10.0 -> 0.0)
    inspect_correct_packets(client, station_id=1)
    # Create the expected updated packet
    updated_packet = Packet(id=1, 
                     datetime_=ref_detatime, 
                     station_id=1, 
                     temperature_celsius=25.5, 
                     moisture_perc=50.0, 
                     wind_speed_kmh=10.3, 
                     wind_direction="north",
                     rain_meas_mm=0.0)
    # Check if get_packets was called with the correct parameters
    mock_get_packets.assert_called_once_with(client=client, station_id=1)
    # Check if updated_packets was called with the correct parameters
    mock_update_packet.assert_called_once_with(
        client=client, packet_id=updated_packet.id, body=updated_packet)
    # Check if return value has the updated packet
    assert mock_get_packets.return_value == [updated_packet], "get_packets should return updated packet"


    