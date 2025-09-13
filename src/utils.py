"""Helper methods to inspect the GET response"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import datetime
if TYPE_CHECKING:
    from packet_api_client.models import Packet 

def inspect_response(response: Optional[list[Packet]], datetime: datetime | None, station_id: int) -> None:
    if response is not None:
        # if no filter applied, fetch all the packets
        if datetime is None and station_id == -1:
            packet = response.parsed
            k = 1