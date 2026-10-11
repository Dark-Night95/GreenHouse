from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schema import AlertCreate, AlertUpdate
from ..services.greenhouse_logic import sync_latest_sensor_conditions

router = APIRouter()
@router.get("/")
def get_alerts(db:Session = Depends(get_db)):
    sync_latest_sensor_conditions(db)
    return crud.get_alerts(db)

@router.get("/{Id}")
def get_alert(Id:int,db:Session = Depends(get_db)):
    return crud.get_alert(db,Id)

@router.post("/")
def create_alert(
        alert:AlertCreate,
        db:Session = Depends(get_db)):
    return crud.create_alert(db,alert)

@router.put("/{Id}")
def update_alert(
        Id:int,
        alert:AlertUpdate,
        db:Session = Depends(get_db)):
    return crud.update_alert(db,Id,alert)
