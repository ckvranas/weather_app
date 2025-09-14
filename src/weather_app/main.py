"""Main weather app"""
import os
from packet_api_client import Client
from dotenv import load_dotenv
from weather_app.utils import inspect_correct_packets
import argparse
from datetime import datetime

load_dotenv()
API_URL, TOKEN = os.getenv("API_URL"), os.getenv("TOKEN")

def main() -> None:
    """Main weather app"""
    parser = argparse.ArgumentParser(description='Packet API Client') 
    parser.add_argument('--datetime', dest='datetime_str', type=str, help='Packet datetime')
    parser.add_argument('--station-id', dest='station_id', type=int, default=-1, help='Station ID')
    client = Client(base_url=API_URL, headers={"Authorization": f"Bearer {TOKEN}"})
    #parser.parse_args().datetime
    a = datetime.fromisoformat(parser.parse_args().datetime_str) if datetime is not None else None
    print(a)
    # inspect_correct_packets(client, station_id=parser.parse_args().station_id, datetime=a)

if __name__ == "__main__":
    main()