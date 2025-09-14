"""Main weather app"""
import os
from packet_api_client import Client
from dotenv import load_dotenv
from weather_app.utils import inspect_correct_packets
import argparse
from datetime import datetime

env_file = os.getenv("ENV_FILE", ".env.local")
load_dotenv(dotenv_path=env_file)
API_URL, TOKEN, DUMMY_DATETIME = os.getenv("API_URL"), os.getenv("TOKEN"), os.getenv("DUMMY_DATETIME")
print(API_URL, TOKEN, DUMMY_DATETIME)   
def main() -> None:
    """Interactive CLI for weather client"""
    client = Client(base_url=API_URL, headers={"Authorization": f"Bearer {TOKEN}"})

    while True:
        print("\n--- Weather Client ---")
        print("1. Inspect and correct packets")
        print("2. Exit")
        choice = input("Enter choice [1-2]: ").strip()

        if choice == "1":
            dt_input = input(f"Enter datetime (default={DUMMY_DATETIME}): ").strip() or DUMMY_DATETIME
            station_input = input("Enter station ID (default=-1): ").strip() or -1
            try:
                inspect_correct_packets(client, station_id=int(station_input), datetime_=datetime.strptime(dt_input, "%Y-%m-%d %H:%M:%S.%f"))
            except Exception as e:
                print(f"[ERROR] {e}")
        elif choice == "2":
            print("Exiting!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()