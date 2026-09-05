from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.database import get_db
from apps import crud
from apps.schema import SensorDataCreate

router = APIRouter()

@router.post("/")
def create_sensor_reading(
        data: SensorDataCreate,
        db: Session = Depends(get_db),
):
    return crud.create_sensor_reading(db, data)

@router.get("/{Id}")
def get_sensor_readings(id: int, db: Session = Depends(get_db)):
    return crud.get_sensor_reading(db, Id)

