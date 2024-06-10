import pandas as pd
import numpy as np
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client['iot_db']
collection = db['iot_db']

# Définition des valeurs des variables
date = datetime.datetime.now()
tempreature = 35
humidity = 10
water_level = 70
N = 20
P = 10
K = 5
fan_actuator_on = True
watering_plant_pump_on = False
water_pump_actuator_on = True

# Insertion d'un document avec des variables
document = {
    'date': date,
    'tempreature': tempreature,
    'humidity': humidity,
    'water_level': water_level,
    'N': N,
    'P': P,
    'K': K,
    'Fan_actuator_ON': fan_actuator_on,
    'Watering_plant_pump_ON': watering_plant_pump_on,
    'Water_pump_actuator_ON': water_pump_actuator_on
}

collection.insert_one(document)
