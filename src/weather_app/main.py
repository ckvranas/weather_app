"""Main weather app"""
import os
from packet_api_client import Client
from dotenv import load_dotenv
from weather_app.utils import inspect_correct_packets
import argparse
from datetime import datetime

load_dotenv()
API_URL, TOKEN, DUMMY_DATETIME = os.getenv("API_URL"), os.getenv("TOKEN"), os.getenv("DUMMY_DATETIME")

def main() -> None:
    """Main weather app"""
    parser = argparse.ArgumentParser(description='Packet API Client') 
    parser.add_argument('--datetime', dest='datetime_', type=str, default=DUMMY_DATETIME, help='Packet datetime')
    parser.add_argument('--station-id', dest='station_id', type=int, default=-1, help='Station ID')
    client = Client(base_url=API_URL, headers={"Authorization": f"Bearer {TOKEN}"})
    inspect_correct_packets(client, station_id=parser.parse_args().station_id, datetime_=datetime.strptime(parser.parse_args().datetime_, '%Y-%m-%d %H:%M:%S.%f'))

if __name__ == "__main__":
    main()