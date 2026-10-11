# Smart Greenhouse

Smart Greenhouse is a greenhouse monitoring app with a web dashboard and a FastAPI backend. It lets you manage plants, record sensor readings, compare readings with plant-specific growing ranges, and view alerts. A bundled machine learning model predicts whether watering is required based on the latest sensor reading.

## Features

- Dashboard showing plant counts, recent sensor readings, alerts, and a sensor trend.
- Create, view, update, and delete plant records.
- Configure temperature, humidity, and light ranges for each plant.
- Record sensor readings and generate condition alerts when readings fall outside configured ranges.
- Predict watering needs from the latest sensor reading.
- Optional sensor simulator that sends sample readings every 10 seconds.

## Requirements

- Python 3.10 or newer
- MySQL server

Python dependencies are listed in requirements.txt.

## Setup

1. Clone the repository and enter its directory:

   git clone <repository-url>
cd <repository-directory>
2. Create and activate a virtual environment:

   python -m venv .venv

   Windows PowerShell

   .venv\Scripts\Activate.ps1

   macOS or Linux

   source .venv/bin/activate
3. Install dependencies:

   pip install -r requirements.txt
4. Create the MySQL database and configure its connection.

   The app expects a database named greenhouse. Update SQLALCHEMY_DATABASE_URL in apps/database.py with your MySQL username, password, host, and port. The current source uses root:1234 on localhost.
5. Create the tables. The app does not create database tables automatically. The following schema matches the SQLAlchemy models and requires MySQL 5.7 or newer:

   CREATE DATABASE IF NOT EXISTS greenhouse;
USE greenhouse;

CREATE TABLE plants (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(30),
    Plant_type VARCHAR(30),
    Location VARCHAR(20),
    Date_added DATE,
    Status VARCHAR(15)
);

CREATE TABLE plant_requirements (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Plant_id INT,
    Min_temp FLOAT,
    Max_temp FLOAT,
    Min_humid FLOAT,
    Max_humid FLOAT,
    Min_light FLOAT,
    Max_light FLOAT
);

CREATE TABLE sensor_data (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Plant_id INT,
    Temperature FLOAT,
    Humidity FLOAT,
    water_required INT GENERATED ALWAYS AS
        (CASE WHEN Humidity < 40 THEN 1 ELSE 0 END) STORED,
    Light FLOAT,
    Timestamp DATETIME
);

CREATE TABLE alerts (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Plant_id INT,
    Alert_type VARCHAR(50),
    Message VARCHAR(80),
    Severity VARCHAR(20),
    Time_stamp DATETIME,
    Status VARCHAR(20)
);

## Run the application

From the project root, with your virtual environment activated, run:

uvicorn apps.main:app --reload

When the server starts, open:

- Dashboard: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## Send sample sensor readings

In a second terminal, activate the virtual environment and run:

python sensor_simulator.py

The simulator sends readings for plant ID 1 every 10 seconds. Create plant 1 before starting the simulator. Configure growing requirements for that plant in the dashboard or API to enable automatic condition checks and alerts.

## API reference

The API accepts and returns JSON. Visit /docs while the server is running to see request fields and try endpoints interactively.

| Endpoint | Methods | Description |
|---|---|---|
| /plants/ | GET, POST | List plants or create a plant |
| /plants/{id} | GET, PUT, DELETE | Read, update, or delete a plant |
| /requirements/ | POST | Create a plant's growing ranges |
| /requirements/{plant_id} | GET, PUT | Read or update a plant's growing ranges |
| /sensors/ | POST | Record a sensor reading |
| /sensors/{plant_id} | GET | Get a plant's sensor reading |
| /alerts/ | GET, POST | List or create alerts |
| /alerts/{id} | GET, PUT | Read or update an alert |
| /dashboard/ | GET | Get summary data for the dashboard |
| /prediction/latest | GET | Predict watering needs from the latest reading |

Example request to record a sensor reading:

curl -X POST "http://127.0.0.1:8000/sensors/" \
  -H "Content-Type: application/json" \
  -d '{"Plant_id":1,"Temperature":28.5,"Humidity":55,"Light":2.4}'

## Water prediction model

The prediction endpoint uses the latest recorded temperature, humidity, and light values. It returns whether watering is predicted to be required and the model's confidence.

The trained model is included at ml_prediction/model.pkl. The ml_prediction folder also contains scripts to prepare sensor data and train a Random Forest model. Some script input and output paths depend on the current working directory. The API loads the model from ml_prediction/model.pkl.

The database derives the water_required label from humidity: values below 40 produce a label of 1; other values produce 0.

## Project structure

apps/                 FastAPI app, database models, API routes, and greenhouse logic
frontend/              Dashboard HTML, CSS, and JavaScript
ml_prediction/         Prediction code, trained model, and training scripts
sensor_simulator.py    Example sensor data sender
requirements.txt       Python dependencies

## Configuration note

Database credentials are currently configured directly in apps/database.py. Update the connection string there to match your MySQL setup.
