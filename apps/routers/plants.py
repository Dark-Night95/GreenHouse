from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud
from ..schema import CreatePlant

router = APIRouter()


@router.get("/")
def get_plants(db: Session = Depends(get_db)):
    return crud.get_plants(db)


@router.get("/{plant_id}")
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    return crud.get_plant(db, plant_id)


@router.post("/")
def create_plant(
        plant: CreatePlant,
        db: Session = Depends(get_db)):
    return crud.create_plant(db, plant)

@router.put("/{plant_id}")
def update_plant(
        plant_id: int,
        plant: CreatePlant,
        db: Session = Depends(get_db)):
    return crud.update_plant(db, plant_id, plant)


@router.delete("/{plant_id}")
def delete_plant(
        plant_id: int,
        db: Session = Depends(get_db)):
    return crud.delete_plant(db, plant_id)