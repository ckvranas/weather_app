# Weather Data Client and Mock Server

## Overview

Python application designed for adding and correcting weather measurement data collected from base stations. It uses an OpenAPI-generated client to interact with a mock server implemented with FastAPI. The backend persists data in a SQLite database.

The application supports inspecting and correcting erroneous measurement values and includes some initial test data generated during development.

---

## Features

- Add and correct weather measurements from base stations.
- Client-server interaction using OpenAPI-generated Python client.
- Mock server implemented with FastAPI and SQLite backend.
- Data inspection and automatic correction of invalid measurement values.
- Ability to post new data to the server using RESTful API.
- Automated testing with `pytest` using mocks for client API calls.
- Dockerized setup for easy local development and testing.

---

## Local Development Setup

1. Run the setup script:

    ```bash
    source setup.sh
    ```

2. Open a new terminal and start the mock server:

    ```bash
    source .venv/bin/activate
    cd src/mock_server
    uvicorn mock_server:app --reload --port 8000
    ```

3. Back in the original terminal (project root directory), run the client:

    ```bash
    python src/weather_app/main.py
    ```

4. Interacting with the client:

    - Press `1` to inspect and correct data based on datetime and station ID.
    - Press `2` to exit.

    By providing filter inputs, the application displays filtered packets, applies corrections on erroneous fields, and updates the database. Reapplying the same filter after correction will show the updated data. Input examples with the client application are:

I. Datetime: 2026-08-15 20:27:13.882773
II. station-id: 8

---

## Posting Data via API

With the mock server running, you can post data directly using `curl`:

```bash
curl -X POST http://localhost:8000/packets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer my_secret" \
  -d '{
    "id": 8,
    "datetime_": "2026-08-15 20:27:13.882773",
    "station_id": 8,
    "temperature_celsius": 25.4,
    "moisture_perc": 100.2,
    "wind_speed_kmh": 130.4,
    "wind_direction": "north",
    "rain_meas_mm": -102.0
  }'
```

## Testing

This project uses `pytest` with mocking to test the OpenAPI client.

To run the tests, execute the following command from the project root directory:

```bash
pytest
```

## Docker Usage
# Build Docker Images

Run the following command from the root directory of the project to build the Docker images:

```bash
docker-compose build
```

# Start the Mock Server
To start the mock server service in detached mode, run:

```bash
docker-compose up -d mock-server
```

You can follow the mock server logs with:
```bash
docker-compose logs -f mock-server
```

# Run the Weather Client Interactively
Open a new terminal and run the weather client container interactively with:
```bash
docker-compose run --rm weather-client
```
This lets you interact with the weather app client while viewing the mock server logs simultaneously.

# Posting Data Using curl Inside the Client Container
1. Find the running weather client container ID:

```bash
docker ps
```

2. Access the container’s shell:
```bash
docker exec -it <container_id> /bin/sh
```

3. If curl is not installed, install it inside the container:
```bash
apt-get update && apt-get install -y curl
```

4. Use curl to POST data to the mock server:
```bash
curl -X POST http://mock-server:8000/packets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer my_secret" \
  -d '{
    "id": 9,
    "datetime_": "2026-08-15 20:28:13.882773",
    "station_id": 8,
    "temperature_celsius": 25.4,
    "moisture_perc": 10.2,
    "wind_speed_kmh": 130.4,
    "wind_direction": "north",
    "rain_meas_mm": 10.0
  }'
```

## Future Work

- Prepare a YAML configuration file for Continuous Integration (CI) to automate:
  - Running `pytest` for automated testing.
  - Building the Docker images after successful tests.
  - Pushing the built images to Docker Hub (or another container registry).

This will help automate the testing and deployment process, ensuring the project is always up-to-date and verified on each commit.

