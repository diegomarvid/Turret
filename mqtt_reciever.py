import json
from types import SimpleNamespace
from paho.mqtt import client as mqtt_client
import sys
import socketio

class MQTTReciever:

    global sio
    sio = socketio.Client()
     

    def __init__(self):
        self.broker = 'broker.hivemq.com'
        self.port = 1883
        self.hit_topic = "LaserTag"
        self.client_id = "turret_raspberry_pi"

        self.client = self.connect_mqtt()

        self.subscribe(self.client)
        self.initClient()

    def initClient(self):
        sio.connect('http://localhost:5000') 

    def connect_mqtt(self) -> mqtt_client:
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def on_message(self, client, userdata, msg):
        if msg.topic == self.hit_topic:
            self.on_hit()

    def on_hit(self):
        sio.emit("hit","")

    def subscribe(self, client: mqtt_client):
        client.subscribe(self.hit_topic)
        client.on_message = self.on_message

    def read(self):
        self.client.loop_forever()

    @sio.event
    def connect():
        print('Connected to local socket server!')

    @sio.event
    def disconnect():
        print('disconnected from server')
        sys.exit()

