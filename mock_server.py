from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Literal
import sqlite3

DB_PATH = "./packets.db"

app = FastAPI()

# Pydantic model
class Packet(BaseModel):
    datetime: str
    station_id: int
    temperature_celsium: float
    moisture_perc: float
    wind_speed_kmh: float
    wind_direction: Literal["south", "north", "west", "east"]
    rain_meas_mm: float

# Helper function to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            station_id INTEGER,
            temperature_celsium REAL,
            moisture_perc REAL,
            wind_speed_kmh REAL,
            wind_direction TEXT,
            rain_meas_mm REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# POST /packets
@app.post("/packets", response_model=Packet)
def create_packet(packet: Packet):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO packets (datetime, station_id, temperature_celsium, moisture_perc,
                             wind_speed_kmh, wind_direction, rain_meas_mm)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        packet.datetime,
        packet.station_id,
        packet.temperature_celsium,
        packet.moisture_perc,
        packet.wind_speed_kmh,
        packet.wind_direction,
        packet.rain_meas_mm,
    ))
    conn.commit()
    conn.close()
    return packet

# GET /packets
@app.get("/packets", response_model=List[Packet])
def get_packets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT datetime, station_id, temperature_celsium, moisture_perc, wind_speed_kmh, wind_direction, rain_meas_mm FROM packets')
    rows = cursor.fetchall()
    conn.close()
    return [Packet(**dict(row)) for row in rows]

# PUT /packets/{packet_id}
@app.put("/packets/{packet_id}", response_model=Packet)
def update_packet(packet_id: int, updated: Packet):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM packets WHERE id = ?', (packet_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Packet not found")

    cursor.execute('''
        UPDATE packets SET
            datetime = ?,
            station_id = ?,
            temperature_celsium = ?,
            moisture_perc = ?,
            wind_speed_kmh = ?,
            wind_direction = ?,
            rain_meas_mm = ?
        WHERE id = ?
    ''', (
        updated.datetime,
        updated.station_id,
        updated.temperature_celsium,
        updated.moisture_perc,
        updated.wind_speed_kmh,
        updated.wind_direction,
        updated.rain_meas_mm,
        packet_id
    ))
    conn.commit()
    conn.close()
    return updated
