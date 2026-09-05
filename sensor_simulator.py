import requests
import random
import time


while True:
    data = {
        "plant_id": 1,
        "temperature": random.uniform(25, 35),
        "humidity": random.uniform(50, 80),
        "soil_moisture": random.uniform(30, 60),
        "light_intensity": random.uniform(0.1, 5.0)
    }
    response = requests.post(
        "http://127.0.0.1:8000/sensors/sensor-data",
        json=data
    )
    print(response.json())
    time.sleep(10)