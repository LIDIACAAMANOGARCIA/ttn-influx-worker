import json
import os
from paho.mqtt import client as mqtt_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

TTN_BROKER = os.getenv("TTN_BROKER")
TTN_PORT = int(os.getenv("TTN_PORT"))
TTN_USERNAME = os.getenv("TTN_USERNAME")
TTN_PASSWORD = os.getenv("TTN_PASSWORD")
TTN_TOPIC = os.getenv("TTN_TOPIC")

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, rc):
    print("Connected to TTN:", rc)
    client.subscribe(TTN_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        uplink = payload.get("uplink_message", {})
        decoded = uplink.get("decoded_payload", {})

        print("Received:", decoded)

        point = Point("sensor_data")

        for key, value in decoded.items():
            if isinstance(value, (int, float)):
                point.field(key, value)

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=point
        )

        print("Written to InfluxDB")

    except Exception as e:
        print("Error:", e)

client = mqtt_client.Client()

client.username_pw_set(
    TTN_USERNAME,
    TTN_PASSWORD
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(TTN_BROKER, TTN_PORT, 60)

client.loop_forever()
