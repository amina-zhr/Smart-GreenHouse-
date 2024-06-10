##################### don't delete the last commented code #############################
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bson import ObjectId
from pymongo import MongoClient
import pickle
from sklearn.linear_model import LogisticRegression
from datetime import datetime

st.set_page_config(layout='wide')


client = MongoClient('mongodb://localhost:27017/')
db = client['iot_db']
collection = db['iot_db']

# Fetch data from MongoDB collection
cursor = collection.find()

# Convert cursor to DataFrame
df = pd.DataFrame(list(cursor))
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

st.markdown("# Smart Green House")

# Récupération de la dernière donnée saisie
latest_document = collection.find_one(sort=[('date', -1)])


if latest_document:
    date = latest_document['date']
    print(str(date)[0:19])
    temperature = latest_document['tempreature']
    humidity = latest_document['humidity']
    waterLevel = latest_document['water_level']
    N = latest_document['N']
    P = latest_document['P']
    K = latest_document['K']
    fan = latest_document['Fan_actuator_ON']
    w_p_pump = latest_document['Watering_plant_pump_ON']
    w_pump = latest_document['Water_pump_actuator_ON']

dt = datetime.strptime(str(date)[0:19],'%Y-%m-%d %H:%M:%S')
hour = dt.hour
month=dt.month



columns=['tempreature', 'humidity', 'water_level', 'N', 'P', 'K', 'hour', 'month']
values = [[temperature, humidity, waterLevel, N, P, K, hour, month]]

# Créer la DataFrame
X = pd.DataFrame(values, columns=columns)
f=open("AI_models/Fan_actuator_ON.pkl", 'rb')
model = pickle.load(f)
fan_on = model.predict(X)
f.close()

f=open("AI_models/Water_pump_actuator_ON.pkl", 'rb')
model = pickle.load(f)
pump_aw = model.predict(X)
f.close()

f=open("AI_models/Watering_plant_pump_ON.pkl", 'rb')
model = pickle.load(f)
pump_wp = model.predict(X)
f.close()

# Convert NumPy arrays to Python lists
fan_on = fan_on.tolist()
pump_wp = pump_wp.tolist()
pump_aw = pump_aw.tolist()

update_doc = {
    "$set": {
        "Fan_actuator_ON": fan_on,
        "Watering_plant_pump_ON": pump_wp,
        "Water_pump_actuator_ON": pump_aw
    }
}


collection.update_one(
    {"_id": ObjectId(latest_document['_id'])},
    update_doc
)

c1, c2 = st.columns((6, 3))
###########################################Left Side##############################################################
with c1:
    fig1, ax1 = plt.subplots(figsize=(10,2))
    ax1.plot(df['date'], df['tempreature'])
    ax1.get_xaxis().set_visible(False)
    plt.grid(True)
    plt.tight_layout()
    plt.ylabel('Tempreature')
    st.pyplot(fig1, use_container_width=True)

    fig2, ax2 = plt.subplots(figsize=(10,2))
    ax2.plot(df['date'], df['humidity'])
    ax2.get_xaxis().set_visible(False)
    plt.grid(True)
    plt.tight_layout()
    plt.ylabel('Humidity')
    st.pyplot(fig2, use_container_width=True)

    fig3, ax3 = plt.subplots(figsize=(10,3))
    ax3.plot(df['date'], df['N'], label='N')
    ax3.plot(df['date'], df['P'], label='P')
    ax3.plot(df['date'], df['K'], label='K')
    plt.legend()
    plt.xticks(rotation=20)
    plt.grid(True)
    plt.tight_layout()
    plt.ylabel('Element level(0-255)')
    st.pyplot(fig3, use_container_width=True)

###########################################Right Side Side##############################################################
with c2:
    gap1, r1c1, r1c2 = st.columns(3)
    r1c1.metric("Date/Time", str(date)[5:10])
    r1c2.metric("Temperature", f'{temperature} °C')
    gap2, r2c1, r2c2 = st.columns(3)
    r2c1.metric("Humdity", f'{humidity} %')
    r2c2.metric("Water Level", f'{waterLevel} %')
    gap3, r3c1, r3c2 = st.columns(3)
    r3c1.metric("N", f'{N}')
    r3c2.metric("P", f'{P}')
    gap4, r4c1, r4c2 = st.columns(3)
    r4c1.metric("K", f'{K}')
    r4c2.metric("Fan status", 'On' if fan else 'Off')
    gap5, r5c1, r5c2 = st.columns(3)
    r5c1.metric("Water plant pump status", 'On' if w_p_pump else 'Off')
    r5c2.metric("Water pump status", 'On' if w_pump else 'Off')
    gap1, r6 = st.columns((1, 2))

