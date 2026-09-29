from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.database import get_db
from apps.models import SensorData
from ml_prediction.predict import predict_water_requirement

router = APIRouter()


@router.get("/latest")
def latest_prediction(db: Session = Depends(get_db)):

    latest_sensor = (
        db.query(SensorData)
        .order_by(SensorData.Timestamp.desc())
        .first()
    )

    if latest_sensor is None:
        return {
            "message": "No sensor data available"
        }

    prediction = predict_water_requirement(
        latest_sensor.Temperature,
        latest_sensor.Humidity,
        latest_sensor.Light
    )

    return {
        "temperature": latest_sensor.Temperature,
        "humidity": latest_sensor.Humidity,
        "light": latest_sensor.Light,
        "Prediction and its chances": prediction
    }