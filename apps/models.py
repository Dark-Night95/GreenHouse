from sqlalchemy import Column, Integer, String,DateTime,Date
from .database import Base

class Plant(Base):
    __tablename__="plants"
    Id=Column(Integer,primary_key=True)
    Name=Column(String(30))
    Plant_type=Column(String(30))
    Location=Column(String(20))
    Date_added=Column(Date)
    Status=Column(String(15))

class PlantRequirement(Base):
    __tablename__="plant_requirements"
    Id=Column(Integer,primary_key=True)
    Plant_id=Column(Integer)
    Min_temp=Column(Integer)
    Max_temp=Column(Integer)
    Min_humid=Column(Integer)
    Max_humid=Column(Integer)
    Min_light=Column(Integer)
    Max_light=Column(Integer)

class SensorData(Base):
    __tablename__="sensor_data"
    Id=Column(Integer,primary_key=True)
    Plant_id=Column(Integer)
    Temperature=Column(Integer)
    Humidity=Column(Integer)
    Soil_moisture=Column(Integer)
    Light=Column(Integer)
    Timestamp=Column(DateTime)

class Alert(Base):
    __tablename__="alerts"
    Id = Column(Integer, primary_key=True)
    Plant_id = Column(Integer)
    Message = Column(String(255))
    Created_at = Column(DateTime)