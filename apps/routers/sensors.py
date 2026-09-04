from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import SensorData
from ..database import  get_db
from .. import crud
from ..schema import SensorDataCreate

router = APIRouter()

@router.post("/sensor_data")
def create_sensor_data(
        data: SensorDataCreate,
        db: Session = Depends(get_db)
):
    new_data = SensorData(
        Plant_id=data.plant_id,
        Temperature=data.temperature,
        Humidity=data.humidity,
        Soil_moisture=data.soil_moisture,
        Light=data.light,
        Timestamp=data.timestamp,
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data
