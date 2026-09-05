from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schema import PlantRequirementCreate

router = APIRouter()

@router.get("/{Id}")
def get_requirements(Id:int,db: Session = Depends(get_db)):
    return crud.get_requirements(db,Id)

@router.post("/")
def create_requirements(
        requirement:PlantRequirementCreate,
        db: Session = Depends(get_db)):
    return crud.create_requirements(db,requirement)

@router.put("/{Id}")
def update_requirements(
        Id:int,
        requirement:PlantRequirementCreate,
        db: Session = Depends(get_db)):
    return crud.update_requirements(db,Id,requirement)
