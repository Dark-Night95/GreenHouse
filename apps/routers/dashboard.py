from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Plant, SensorData, Alert


router = APIRouter()


@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):

    plants = db.query(Plant).all()
    total_plants = len(plants)
    latest_alerts = db.query(Alert).order_by(
        Alert.Time_stamp.desc(),
        Alert.Id.desc(),
    ).limit(5).all()
    alert_plant_ids = {alert.Plant_id for alert in latest_alerts}
    warning_plants = sum(plant.Id in alert_plant_ids for plant in plants)
    healthy_plants = total_plants - warning_plants
    active_alerts = sum(alert.Status == "ACTIVE" for alert in latest_alerts)

    # Latest sensor reading
    latest_sensor = db.query(SensorData).order_by(
        SensorData.Timestamp.desc()
    ).first()

    temperature = None
    humidity = None
    light = None

    if latest_sensor:
        temperature = latest_sensor.Temperature
        humidity = latest_sensor.Humidity
        light = latest_sensor.Light

    return {
        "total_plants": total_plants,
        "healthy_plants": healthy_plants,
        "warning_plants": warning_plants,
        "temperature": temperature,
        "humidity": humidity,
        "light": light,
        "active_alerts": active_alerts
    }
