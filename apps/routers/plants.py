from collections.abc import Generator
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Plant
from ..schema import CreatePlant

router = APIRouter()


def get_db() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get("/")
def get_plants(session: Session = Depends(get_db)):
    return session.query(Plant).all()


@router.get("/{plant_id}")
def get_plant(plant_id: int, session: Session = Depends(get_db)):
    return session.query(Plant).filter(Plant.Id == plant_id).first()



@router.post("/plants")
def create_plant(plant:CreatePlant):
    return plant
