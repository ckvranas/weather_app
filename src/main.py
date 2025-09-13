"""Main weather app"""
import os
import datetime
from packet_api_client import Client
from packet_api_client.api.default import get_packets


from utils import inspect_response
import argparse

API_URL = "http://localhost:8000" 

def main() -> None:
    """Main weather app"""
    parser = argparse.ArgumentParser(description='Packet API Client') 
    parser.add_argument('--datetime', dest='datetime', type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f'), help='Packet datetime')
    parser.add_argument('--station-id', dest='station_id', type=int, default=-1, help='Station ID')
    try:
        client = Client(base_url=API_URL)
        response = get_packets.sync(client=client, station_id=2)
        inspect_response(response)
    except Exception as e:
        print(f"Error while calling API: {e}")

if __name__ == "__main__":
    main()