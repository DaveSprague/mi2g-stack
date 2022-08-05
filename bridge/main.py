#!/usr/bin/env python3

"""A MQTT to InfluxDB Bridge
This script receives MQTT data and saves those to InfluxDB.
"""

import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# TODO: bring variables form .env into this script

INFLUXDB_ADDRESS = 'influxdb'
INFLUXDB_USER = 'admin'
INFLUXDB_PASSWORD = 'HighAndLowTides'
INFLUXDB_BUCKET = 'tide_bucket'
INFLUXDB_ORG = 'tide-org'
INFLUXDB_TOKEN = 'H4bMbERkTk17tv8use+MsJudPAbuo09BSkQMLxcOcaE='

MQTT_ADDRESS = 'mosquitto'
MQTT_USER = ''
MQTT_PASSWORD = ''
MQTT_TOPIC = 'tide/+/+'
MQTT_REGEX = 'tide/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

influxdb_client = client = InfluxDBClient(url="http://localhost:8086", token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

class SensorData(NamedTuple):
    location: str
    sensor: str
    value: int


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    print(f"Sensor Data: {sensor_data}")
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        sensor = match.group(2)
        if sensor == 'status':
            return None
        print(f"{location}::{sensor}::{float(payload)}")
        return SensorData(location, sensor, float(payload))
    else:
        return None


def _send_sensor_data_to_influxdb(sensor_data):
    p = Point(sensor_data.sensor). \
        tag('location', sensor_data.location). \
            field("value", sensor_data.value)
    print(str(p.to_line_protocol))
    result = write_api.write(bucket=INFLUXDB_BUCKET, record=p)
    print('result: ' + str(result));

# def _init_influxdb_database():
#     databases = influxdb_client.get_list_database()
#     if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
#         influxdb_client.create_database(INFLUXDB_DATABASE)
#     influxdb_client.switch_database(INFLUXDB_DATABASE)


def main():
    # _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    # mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
