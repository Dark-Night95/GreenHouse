from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Plant, PlantRequirement, SensorData, Alert
from ..services.greenhouse_logic import check_greenhouse


router = APIRouter()


@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):

    # Total plants
    total_plants = db.query(Plant).count()

    # Active alerts
    active_alerts = db.query(Alert).filter(
        Alert.Status == "ACTIVE"
    ).count()

    # Latest sensor reading
    latest_sensor = db.query(SensorData).order_by(
        SensorData.Timestamp.desc()
    ).first()

    temperature = None
    humidity = None
    soil_moisture = None
    light = None

    if latest_sensor:
        temperature = latest_sensor.Temperature
        humidity = latest_sensor.Humidity
        soil_moisture = latest_sensor.Soil_moisture
        light = latest_sensor.Light

    # Healthy and warning plants
    healthy_plants = 0
    warning_plants = 0

    plants = db.query(Plant).all()

    for plant in plants:

        requirement = db.query(PlantRequirement).filter(
            PlantRequirement.Plant_id == plant.Id
        ).first()

        sensor = db.query(SensorData).filter(
            SensorData.Plant_id == plant.Id
        ).order_by(
            SensorData.Timestamp.desc()
        ).first()

        if requirement and sensor:

            problems = check_greenhouse(
                sensor,
                requirement
            )

            if len(problems) == 0:
                healthy_plants += 1
            else:
                warning_plants += 1

    return {
        "total_plants": total_plants,
        "healthy_plants": healthy_plants,
        "warning_plants": warning_plants,
        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil_moisture,
        "light": light,
        "active_alerts": active_alerts
    }