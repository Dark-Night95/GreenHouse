from sqlalchemy import Column, Float, String,DateTime,Date,Integer
from .database import Base

class Plant(Base):
    __tablename__="plants"
    Id=Column(Integer,primary_key=True,autoincrement=True)
    Name=Column(String(30))
    Plant_type=Column(String(30))
    Location=Column(String(20))
    Date_added=Column(Date)
    Status=Column(String(15))

class PlantRequirement(Base):
    __tablename__="plant_requirements"
    Id=Column(Integer,primary_key=True,autoincrement=True)
    Plant_id=Column(Integer)
    Min_temp=Column(Float)
    Max_temp=Column(Float)
    Min_humid=Column(Float)
    Max_humid=Column(Float)
    Min_light=Column(Float)
    Max_light=Column(Float)

class SensorData(Base):
    __tablename__="sensor_data"
    Id=Column(Integer,primary_key=True,autoincrement=True)
    Plant_id=Column(Integer)
    Temperature=Column(Float)
    Humidity=Column(Float)
    Soil_moisture=Column(Float)
    Light=Column(Float)
    Timestamp=Column(DateTime)

class Alert(Base):
    __tablename__="alerts"
    Id = Column(Integer, primary_key=True,autoincrement=True)
    Plant_id = Column(Integer)
    Alert_type = Column(String(50))
    Message = Column(String(80))
    Time_stamp = Column(DateTime)
    Status = Column(String(20))