from datetime import datetime

from apps.models import Alert, Plant, PlantRequirement, SensorData


def check_greenhouse(sensor_data, plant_requirements):

    problems = []

    if sensor_data.Temperature > plant_requirements.Max_temp:
        problems.append({
            "type": "temperature_high",
            "message": "Temperature is too high",
            "severity": "WARNING"
        })

    if sensor_data.Temperature < plant_requirements.Min_temp:
        problems.append({
            "type": "temperature_low",
            "message": "Temperature is too low",
            "severity": "WARNING"
        })

    if sensor_data.Humidity < plant_requirements.Min_humid:
        problems.append({
            "type": "humidity_low",
            "message": "Humidity is too low",
            "severity": "WARNING"
        })

    if sensor_data.Humidity > plant_requirements.Max_humid:
        problems.append({
            "type": "humidity_high",
            "message": "Humidity is too high",
            "severity": "WARNING"
        })

    if sensor_data.Light < plant_requirements.Min_light:
        problems.append({
            "type": "light_low",
            "message": "Light level is too low",
            "severity": "WARNING"
        })

    if sensor_data.Light > plant_requirements.Max_light:
        problems.append({
            "type": "light_high",
            "message": "Light level is too high",
            "severity": "WARNING"
        })

    return problems


def sync_plant_condition(db, plant, sensor_data, plant_requirements):
    problems = check_greenhouse(sensor_data, plant_requirements)
    plant.Status = "Warning" if problems else "Healthy"

    active_alert = db.query(Alert).filter(
        Alert.Plant_id == plant.Id,
        Alert.Alert_type == "SENSOR_CONDITION",
        Alert.Status == "ACTIVE",
    ).first()

    if problems:
        message = "; ".join(problem["message"] for problem in problems)[:80]
        if active_alert:
            active_alert.Message = message
            active_alert.Time_stamp = datetime.now()
        else:
            db.add(Alert(
                Plant_id=plant.Id,
                Alert_type="SENSOR_CONDITION",
                Message=message,
                Severity="WARNING",
                Time_stamp=datetime.now(),
                Status="ACTIVE",
            ))
    elif active_alert:
        active_alert.Status = "RESOLVED"

    return problems


def sync_latest_sensor_conditions(db):
    for plant in db.query(Plant).all():
        requirement = db.query(PlantRequirement).filter(
            PlantRequirement.Plant_id == plant.Id
        ).first()
        sensor_data = db.query(SensorData).filter(
            SensorData.Plant_id == plant.Id
        ).order_by(SensorData.Timestamp.desc()).first()

        if requirement and sensor_data:
            sync_plant_condition(db, plant, sensor_data, requirement)

    latest_alerts = db.query(Alert).order_by(
        Alert.Time_stamp.desc(),
        Alert.Id.desc(),
    ).limit(5).all()
    alerted_plant_ids = {alert.Plant_id for alert in latest_alerts}

    for plant in db.query(Plant).all():
        plant.Status = "Warning" if plant.Id in alerted_plant_ids else "Healthy"

    db.commit()
