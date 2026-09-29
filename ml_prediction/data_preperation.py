import pandas as pd
import os
from apps.database import engine

# get all the data from the database
query="SELECT * FROM sensor_data"

# read the data into a dataframe
df=pd.read_sql(query,engine)

# drop the rows with null values or useless rows for our model
df=df.dropna(
    subset=['Temperature','Humidity','Light','water_required']
)

print("Total Duplicate rows:")
df=df.drop_duplicates()

print("\nConvert Timestamp")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

print("\nConvert Timestamp to Hour")
df["hour"] = df["Timestamp"].dt.hour

print("\nShape of the Dataframe:")
print(df.shape)

print("\nOriginal Dataframe:")
print(df.head())

print("\nDataframe Info:")
print(df.info())

print("\nNull Values:")
print(df.isnull().sum())

# split the data into input features
features = ['Temperature', 'Humidity', 'Light']
x = df[features]

# target variable
y = df['water_required']

print("\nTarget distribution:")
print(y.value_counts())


# save the data into a csv file by making os directory
os.makedirs("data", exist_ok=True)

prepared_data=df[[
    "Temperature",
    "Humidity",
    "Light",
    "water_required"
]]

data_file = "prepared_dataset.csv"
prepared_data.to_csv(data_file, index=False)

print("\nData saved to:", data_file)