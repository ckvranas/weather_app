"""Main weather app"""
import os
from packet_api_client import Client
from packet_api_client.api.default import get_packets

from utils import inspect_response

API_URL = "http://localhost:8000" 

def main() -> None:
    client = Client(base_url=API_URL)
    response = get_packets.sync(client=client)
    try:
        response = get_packets.sync(client=client)
    except Exception as e:
        print(f"Error while making API call: {e}")
        return

    inspect_response(response)


if __name__ == "__main__":
    main()