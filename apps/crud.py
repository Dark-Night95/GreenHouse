from sqlalchemy.orm import Session
from .models import Plant,PlantRequirement

#these are for plants
def create_plant(db:Session,plant_data):
    new_plant=Plant(
        Name=plant_data.Name,
        Plant_type=plant_data.Plant_type,
        Location=plant_data.Location,
        Date_added=plant_data.Date_added,
        Status=plant_data.Status,
    )
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)

    return new_plant


def get_plant(db: Session, plant_id: int):
    return db.query(Plant).filter(
        Plant.Id == plant_id
    ).first()

def get_plants(db:Session):
    return db.query(Plant).all()

def update_plant(db: Session, plant_id: int, plant_data):
    plant = db.query(Plant).filter(
        Plant.Id == plant_id
    ).first()
    if plant is None:
        return None
    plant.Name = plant_data.Name
    plant.Plant_type = plant_data.Plant_type
    plant.Location = plant_data.Location
    plant.Date_added = plant_data.Date_added
    plant.Status = plant_data.Status

    db.commit()
    db.refresh(plant)
    return plant

def delete_plant(db:Session,plant_id:int):
    plant=db.query(Plant).filter(
        Plant.Id==plant_id
    ).first()
    if plant is None:
        return None

    db.delete(plant)
    db.commit()
    return plant

#tthese are for requirements

def create_requirements(db:Session,requirements_data):
    new_requirement=PlantRequirement(
        Plant_id=requirements_data.Plant_id,
        Min_temp=requirements_data.Min_temp,
        Max_temp=requirements_data.Max_temp,
        Min_humid=requirements_data.Min_humid,
        Max_humid=requirements_data.Max_humid,
        Min_light=requirements_data.Min_light,
        Max_light=requirements_data.Max_light,
    )
    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)
    return new_requirement

def get_requirements(db:Session,plant_id:int):
    return db.query(PlantRequirement).filter(
        PlantRequirement.Plant_id==plant_id
    ).first()

def update_requirements(db:Session,plant_id:int,requirements_data):
    requirement=db.query(PlantRequirement).filter(
        PlantRequirement.Plant_id==plant_id
    ).first()
    if requirement is None:
        return None
    requirement.Min_temp=requirements_data.Min_temp
    requirement.Max_temp=requirements_data.Max_temp
    requirement.Min_humid=requirements_data.Min_humid
    requirement.Max_humid=requirements_data.Max_humid
    requirement.Min_light=requirements_data.Min_light
    requirement.Max_light=requirements_data.Max_light
    db.commit()
    db.refresh(requirement)
    return requirement
