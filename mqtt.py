import random
import json
from types import SimpleNamespace

from paho.mqtt import client as mqtt_client


broker = 'broker.hivemq.com'
port = 1883
topic = "LaserTag"
# generate client ID with pub prefix randomly
client_id = 'diego'

def connect_mqtt() -> mqtt_client:
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = msg.payload.decode()
        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        print(f"Received {x.msg} from {msg.topic}")   
    client.subscribe(topic)
    client.on_message = on_message



client = connect_mqtt()
subscribe(client)
client.loop_forever()