import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="localhost" 

client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker) 

while True:
    randNumber = uniform(20.0, 21.0)
    topic = "tide_bucket/Belfast"
    msg = f"Weather,room=basement value={randNumber}"
    result = client.publish(topic, msg)
    print(f"Just published {msg} to topic {topic} with result {result}")
    time.sleep(1)
