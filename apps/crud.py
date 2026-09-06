from sqlalchemy.orm import Session
from .models import Plant,PlantRequirement,SensorData,Alert
from datetime import datetime

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

# get the plant id by manually searching it
def get_plant(db: Session, plant_id: int):
    return db.query(Plant).filter(
        Plant.Id == plant_id
    ).first()

#get all plants
def get_plants(db:Session):
    return db.query(Plant).all()

#update plant
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
#delete plant
def delete_plant(db:Session,plant_id:int):
    plant=db.query(Plant).filter(
        Plant.Id==plant_id
    ).first()
    if plant is None:
        return None

    db.delete(plant)
    db.commit()
    return plant

#these are for requirements
# create new requirements for plants
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

# get requirements by searching plant id
def get_requirements(db:Session,plant_id:int):
    return db.query(PlantRequirement).filter(
        PlantRequirement.Plant_id==plant_id
    ).first()


# update requirements
def update_requirements(db:Session,plant_id:int,requirements_data):
    requirement=db.query(PlantRequirement).filter(
        PlantRequirement.Plant_id==plant_id
    ).first()
    if requirement is None:
        return None
    requirement.Plant_id=requirements_data.Plant_id
    requirement.Min_temp=requirements_data.Min_temp
    requirement.Max_temp=requirements_data.Max_temp
    requirement.Min_humid=requirements_data.Min_humid
    requirement.Max_humid=requirements_data.Max_humid
    requirement.Min_light=requirements_data.Min_light
    requirement.Max_light=requirements_data.Max_light
    db.commit()
    db.refresh(requirement)
    return requirement


# for sensor data
# create new sensor data
def create_sensor_reading(db:Session,sensor_readings_data):
    new_sensor_reading=SensorData(
        Plant_id=sensor_readings_data.Plant_id,
        Temperature=sensor_readings_data.Temperature,
        Humidity=sensor_readings_data.Humidity,
        Soil_moisture=sensor_readings_data.Soil_moisture,
        Light=sensor_readings_data.Light,
        #Timestamp=sensor_readings_data.Timestamp,
        Timestamp=datetime.now(),
    )
    db.add(new_sensor_reading)
    db.commit()
    db.refresh(new_sensor_reading)
    return new_sensor_reading

# get sensor data by searching plant id
def get_sensor_reading(db:Session,plant_id:int):
    return db.query(SensorData).filter(
        SensorData.Plant_id==plant_id
    ).first()



# for alerts
# create new alerts
def create_alert(db:Session,alerts_data):
    new_alert_data=Alert(
        Plant_id=alerts_data.Plant_id,
        Alert_type=alerts_data.Alert_type,
        Message=alerts_data.Message,
        Time_stamp=datetime.now(),
        Severity=alerts_data.Severity,
    )
    db.add(new_alert_data)
    db.commit()
    db.refresh(new_alert_data)
    return new_alert_data


# get alerts by searching plant id
def get_alert(db:Session,plant_id:int):
    return db.query(Alert).filter(
        Alert.Plant_id==plant_id
    ).first()

def get_alerts(db: Session):
    return db.query(Alert).all()

# update alerts
def update_alert(db:Session,plant_id:int,alerts_data):
    alert=db.query(Alert).filter(
        Alert.Plant_id==plant_id
    ).first()
    if alert is None:
        return None
    alert.Plant_id=alerts_data.plant_id
    alert.Alert_type=alerts_data.alert_type
    alert.Message=alerts_data.alert_message
    alert.Time_stamp=alerts_data.alert_time
    alert.Status=alerts_data.alert_status
    db.commit()
    db.refresh(alert)
    return alert

