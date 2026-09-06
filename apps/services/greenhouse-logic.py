def check_greenhouse_conditions(sensor_data, plant_requirements):
    results = []
    if sensor_data.temperature > plant_requirements.max_temp:
        results.append("Temperature is too high")
    elif sensor_data.temperature < plant_requirements.min_temp:
        results.append("Temperature is too low")
    if sensor_data.humidity > plant_requirements.max_humidity:
        results.append("Humidity is too high")
    elif sensor_data.humidity < plant_requirements.min_humidity:
        results.append("Humidity is too low")
    if sensor_data.light > plant_requirements.max_light:
        results.append("Light is too high")
    elif sensor_data.light < plant_requirements.min_light:
        results.append("Light is too low")
    if not results:
        results.append("All conditions are suitable")

    return results