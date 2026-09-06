def get_recommendations(sensor_data, plant_requirements):

    recommendations = []

    if sensor_data.temperature > plant_requirements.Max_temp:
        recommendations.append("Reduce the greenhouse temperature.")

    if sensor_data.Temperature < plant_requirements.Min_temp:
        recommendations.append("Increase the greenhouse temperature.")

    if sensor_data.Humidity < plant_requirements.Min_humid:
        recommendations.append("Increase humidity.")

    if sensor_data.Humidity > plant_requirements.Max_humid:
        recommendations.append("Reduce humidity.")

    if sensor_data.Light < plant_requirements.Min_light:
        recommendations.append("Provide additional lighting.")

    if sensor_data.Light > plant_requirements.Max_light:
        recommendations.append("Reduce light exposure.")

    return recommendations