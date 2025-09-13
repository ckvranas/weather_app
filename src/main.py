"""Main weather app"""
import os
import datetime
from packet_api_client import Client
from packet_api_client.api.default import get_packets
from dotenv import load_dotenv

from utils import inspect_response
import argparse

load_dotenv()
API_URL, TOKEN = os.getenv("API_URL"), os.getenv("TOKEN")

def main() -> None:
    """Main weather app"""
    parser = argparse.ArgumentParser(description='Packet API Client') 
    parser.add_argument('--datetime', dest='datetime', type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f'), help='Packet datetime')
    parser.add_argument('--station-id', dest='station_id', type=int, default=-1, help='Station ID')
    try:
        client = Client(base_url=API_URL, headers={"Authorization": f"Bearer {TOKEN}"})
        response = get_packets.sync(client=client, station_id=2)
        inspect_response(response)
    except Exception as e:
        print(f"Error while calling API: {e}")

if __name__ == "__main__":
    main()