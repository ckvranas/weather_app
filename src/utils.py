"""Helper methods to inspect the GET response"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from packet_api_client.models import Packet 

def inspect_response(response: Optional[list[Packet]]) -> None:
    if response.status == 200:
        packet = response.parsed
        