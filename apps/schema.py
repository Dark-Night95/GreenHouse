
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
    Plant_id:Annotated[int,Field(gt=0,title=' Plant Id',description='Id of the plant')]
    Temp_min: Annotated[float,Field(title=' Min Temperature',description='Minimum temperature of plant')]
    Temp_max:  Annotated[float,Field(title=' Max Temperature',description='Maximum temperature of plant')]
    Humidity_min:  Annotated[float,Field(title=' Min Temperature',description='Minimum humidity of plant')]
    Humidity_max: Annotated[float,Field(title=' Min Temperature',description='Maximum Humidity of plant')]
    Light_min:  Annotated[float,Field(title=' Min Temperature',description='Minimum light of plant')]
    Light_max:  Annotated[float,Field(title=' Min Temperature',description='Maximum Light of plant')]

class SensorDataCreate(BaseModel):
    Plant_id:Annotated[int,Field(gt=0,title=' Plant Id',description='Id of the plant')]
    Temperature: Annotated[float,Field(title=' Temperature',description='Temperature of plant')]
    Humidity:  Annotated[float,Field(title=' Humidity',description='Humidity of plant')]
    Soil_moisture: Annotated[float,Field(title=' Soil Moisture',description='Soil Moisture of plant')]
    Light:  Annotated[float,Field(title=' Light',description='Light of plant')]
    #Timestamp: Annotated[date,Field(title=' Timestamp',description='Timestamp of plant')]

class AlertCreate(BaseModel):
    Plant_id:Annotated[int,Field(gt=0,title=' Plant Id',description='Id of the plant')]
    Alert_type:Annotated[str,Field(max_length=30,title=' Alert Type',description='Type of the alert')]
    Message:Annotated[str,Field(max_length=100,title=' Alert Message',description='Message of the alert')]
    #Timestamp: Annotated[datetime,Field(title=' Timestamp',description='Timestamp of alert')]
    Status:Annotated[str,Field(max_length=30,title=' Alert Status',description='Status of the alert')]