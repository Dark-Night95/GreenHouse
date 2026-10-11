from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.database import get_db
from apps import crud
from apps.models import Plant
from apps.schema import SensorDataCreate

router = APIRouter()

@router.post("/")
def create_sensor_reading(
        data: SensorDataCreate,
        db: Session = Depends(get_db),
):
    plant = db.query(Plant).filter(Plant.Id == data.Plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail=f"Plant ID {data.Plant_id} does not exist")
    return crud.create_sensor_reading(db, data)

@router.get("/{Id}")
def get_sensor_readings(Id: int, db: Session = Depends(get_db)):
    return crud.get_sensor_reading(db, Id)

