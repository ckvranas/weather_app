import os
from fastapi import FastAPI, HTTPException, Query, status, Security, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List, Literal
import sqlite3

from datetime import datetime

load_dotenv()
DB_PATH, TOKEN, DUMMY_DATETIME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packets.db"), os.getenv("TOKEN"), os.getenv("DUMMY_DATETIME")

app = FastAPI()
security = HTTPBearer()

# Pydantic model
class Packet(BaseModel):
    id: int
    datetime_: datetime
    station_id: int
    temperature_celsius: float
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
            datetime_ TEXT,
            station_id INTEGER,
            temperature_celsius REAL,
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
        INSERT INTO packets (datetime_, station_id, temperature_celsius, moisture_perc,
                             wind_speed_kmh, wind_direction, rain_meas_mm)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        packet.datetime_,
        packet.station_id,
        packet.temperature_celsius,
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
    datetime_: datetime = Query(datetime.strptime(DUMMY_DATETIME, '%Y-%m-%d %H:%M:%S.%f')),
    station_id: int = Query(-1)) -> None:  
    conn = get_db_connection() 
    cursor = conn.cursor()
    isoformat_dummy_datetime = datetime.strptime(DUMMY_DATETIME, '%Y-%m-%d %H:%M:%S.%f')
    # if no input for datetime, it will be equal to the dummy and gets all the rows
    if datetime_ == isoformat_dummy_datetime and station_id == -1:
        cursor.execute('SELECT * FROM packets')
    elif datetime_ != isoformat_dummy_datetime and station_id != -1:
        cursor.execute('SELECT * FROM packets WHERE datetime_ = ? AND station_id = ?', (datetime_.strftime('%Y-%m-%d %H:%M:%S.%f'), station_id))
    elif datetime_ != isoformat_dummy_datetime:
        cursor.execute('SELECT * FROM packets WHERE datetime_ = ?', (datetime_.strftime('%Y-%m-%d %H:%M:%S.%f'),))
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
            datetime_ = ?,
            station_id = ?,
            temperature_celsius = ?,
            moisture_perc = ?,
            wind_speed_kmh = ?,
            wind_direction = ?,
            rain_meas_mm = ?
        WHERE id = ?
    ''', (
        updated.datetime_,
        updated.station_id,
        updated.temperature_celsius,
        updated.moisture_perc,
        updated.wind_speed_kmh,
        updated.wind_direction,
        updated.rain_meas_mm,
        packet_id
    ))

    conn.commit()
    conn.close()

    return Response(status_code=204)