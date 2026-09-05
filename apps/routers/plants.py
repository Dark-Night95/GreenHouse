from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schema import CreatePlant

router = APIRouter()


@router.get("/")
def get_plants(db: Session = Depends(get_db)):
    return crud.get_plants(db)


@router.get("/{id}")
def get_plant(id: int, db: Session = Depends(get_db)):
    return crud.get_plant(db, id)


@router.post("/")
def create_plant(
        plant: CreatePlant,
        db: Session = Depends(get_db)):
    return crud.create_plant(db, plant)

@router.put("/{id}")
def update_plant(
        id: int,
        plant: CreatePlant,
        db: Session = Depends(get_db)):
    return crud.update_plant(db,id, plant)


@router.delete("/{id}")
def delete_plant(
        id: int,
        db: Session = Depends(get_db)):
    return crud.delete_plant(db, id)