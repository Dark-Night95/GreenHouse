from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schema import CreatePlant

router = APIRouter()


@router.get("/")
def get_plants(db: Session = Depends(get_db)):
    return crud.get_plants(db)


@router.get("/{Id}")
def get_plant(Id: int, db: Session = Depends(get_db)):
    return crud.get_plant(db, Id)


@router.post("/")
def create_plant(
        plant: CreatePlant,
        db: Session = Depends(get_db)):
    return crud.create_plant(db, plant)

@router.put("/{Id}")
def update_plant(
        Id: int,
        plant: CreatePlant,
        db: Session = Depends(get_db)):
    return crud.update_plant(db,Id, plant)


@router.delete("/{Id}")
def delete_plant(
        Id: int,
        db: Session = Depends(get_db)):
    return crud.delete_plant(db, Id)
