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