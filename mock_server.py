import os
from fastapi import FastAPI, HTTPException, Query, status, Security, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List, Literal, TYPE_CHECKING
import sqlite3

from datetime import datetime

load_dotenv()
DB_PATH, TOKEN = os.getenv("DB_PATH"), os.getenv("TOKEN")

app = FastAPI()
security = HTTPBearer()

# Pydantic model
class Packet(BaseModel):
    id: int
    datetime: str
    station_id: int
    temperature_celsium: float
    moisture_perc: float
    wind_speed_kmh: float
    wind_direction: Literal["south", "north", "west", "east"]
    rain_meas_mm: float

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token"
        )

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
@app.get("/packets", response_model=List[Packet], dependencies=[Depends(verify_token)])
def get_packets(
    datetime: None | datetime = Query(None),
    station_id: int = Query(-1)) -> None:  
    conn = get_db_connection() 
    cursor = conn.cursor()
    if datetime is None and station_id == -1:
        cursor.execute('SELECT * FROM packets')
    elif datetime is not None and station_id != -1:
        cursor.execute('SELECT * FROM packets WHERE datetime = ? AND station_id = ?', (datetime, station_id))
    elif datetime is not None:
        cursor.execute('SELECT * FROM packets WHERE datetime = ?', (datetime,))
    elif station_id != -1:
        cursor.execute('SELECT * FROM packets WHERE station_id = ?', (station_id,))
    else:
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    rows = cursor.fetchall()
    conn.close()
    return [Packet(**dict(row)) for row in rows]

# PUT /packets/{packet_id}
@app.put("/packets/{packet_id}", response_model=Packet)
def update_packet(packet_id: int, updated: Packet):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if packet exists
    if not cursor.execute('SELECT id FROM packets WHERE id = ?', (packet_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Packet not found")

    # Update packet
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

    return Response(status_code=204)