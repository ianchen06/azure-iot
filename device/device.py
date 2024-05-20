import time
import json
import os
import traceback

from azure.iot.device import IoTHubDeviceClient, MethodResponse
from dotenv import load_dotenv

load_dotenv()

IOTHUB_CONNECTION_STRING = os.getenv("IOTHUB_CONNECTION_STRING")
DEVICE_ID = os.getenv("DEVICE_ID")

client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_CONNECTION_STRING)

device_settings = {
    "mode": "celcius",
}


def message_received_handler(message):
    print("Message received: {}".format(message))


def method_request_handler(method_request):
    print("Method request received: {}".format(method_request))
    try:
        if method_request.name == "SetMode":
            payload = method_request.payload
            device_settings["mode"] = payload
        resp = MethodResponse(method_request.request_id, 200, "OK")
        client.send_method_response(resp)
    except Exception as e:
        print(traceback.format_exc())
        raise e


client.on_message_received = message_received_handler
client.on_method_request_received = method_request_handler

while True:
    print("Sending message...")
    data = {
        "device_id": DEVICE_ID,
        "mode": device_settings["mode"],  # "celcius" or "fahrenheit
        "temperature": 25.0,
    }
    client.send_message(json.dumps(data))
    time.sleep(60)
