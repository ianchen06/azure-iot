import os

import streamlit as st
import psycopg2
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

IOTHUB_CONNECTION_STRING = os.getenv("IOTHUB_CONNECTION_STRING")
DEVICE_ID = os.getenv("DEVICE_ID")

con = psycopg2.connect(DATABASE_URL)

st.title("Azure IoT with PostgreSQL")

temp_mode = st.selectbox("Select a mode", ["Celsius", "Fahrenheit"])
if st.button("Send command"):
    registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)
    method = CloudToDeviceMethod(method_name="SetMode", payload=temp_mode)
    result = registry_manager.invoke_device_method(DEVICE_ID, method)
    st.write("Method result:")
    st.write(result)

with con:
    with con.cursor() as cur:
        cur.execute("SELECT * FROM temperature ORDER BY created_at DESC LIMIT 10")
        rows = cur.fetchall()

        st.write("Temperature data:")
        st.write(rows)