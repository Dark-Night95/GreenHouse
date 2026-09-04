from pydantic  import BaseModel,Field
from typing import Annotated
from datetime import date



class CreatePlant(BaseModel):
    Name:Annotated[str,Field(max_length=30,title=' Plant Name',description='Name of the plant')]
    Plant_type:Annotated[str,Field(max_length=30,title=' Plant Type',description='Type of the plant')]
    Location:Annotated[str,Field(max_length=20,title=' Plant Location',description='Location of the plant')]
    Date_added:Annotated[date,Field(title=' Plant Date Added',description='Date the plant was added')]
    Status:Annotated[str,Field(max_length=15,title=' Plant Status',description='Status of the plant')]

class PlantRequirementCreate(BaseModel):
    plant_id:Annotated[int,Field(gt=0,title=' Plant Id',description='Id of the plant')]
    temp_min: Annotated[float,Field(title=' Min Temperature',description='Minimum temperature of plant')]
    temp_max:  Annotated[float,Field(title=' Max Temperature',description='Maximum temperature of plant')]
    humidity_min:  Annotated[float,Field(title=' Min Temperature',description='Minimum humidity of plant')]
    humidity_max: Annotated[float,Field(title=' Min Temperature',description='Maximum Humidity of plant')]
    light_min:  Annotated[float,Field(title=' Min Temperature',description='Minimum light of plant')]
    light_max:  Annotated[float,Field(title=' Min Temperature',description='Maximum Light of plant')]

class SensorDataCreate(BaseModel):
    plant_id:Annotated[int,Field(gt=0,title=' Plant Id',description='Id of the plant')]
    temperature: Annotated[float,Field(title=' Temperature',description='Temperature of plant')]
    humidity:  Annotated[float,Field(title=' Humidity',description='Humidity of plant')]
    soil_moisture: Annotated[float,Field(title=' Soil Moisture',description='Soil Moisture of plant')]
    light:  Annotated[float,Field(title=' Light',description='Light of plant')]
    timestamp: Annotated[date,Field(title=' Timestamp',description='Timestamp of plant')]

class AlertCreate(BaseModel):
    plant_id:Annotated[int,Field(gt=0,title=' Plant Id',description='Id of the plant')]
    alert_type:Annotated[str,Field(max_length=30,title=' Alert Type',description='Type of the alert')]
    message:Annotated[str,Field(max_length=100,title=' Alert Message',description='Message of the alert')]
    timestamp: Annotated[date,Field(title=' Timestamp',description='Timestamp of alert')]
    status:Annotated[str,Field(max_length=30,title=' Alert Status',description='Status of the alert')]