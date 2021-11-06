from paho.mqtt import client as mqtt_client
import sys
import socketio
import random

class MQTTReciever:

    global sio
    sio = socketio.Client()

    global connected
    connected = False
     

    def __init__(self):
        self.broker = 'broker.hivemq.com'
        self.port = 1883
        self.hit_topic = "LaserTag"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

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

        def on_disconnect(self, client, userdata, rc):
            print("Unexpected MQTT disconnection. Will auto-reconnect")

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.connect(self.broker, self.port)
        return client

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def on_message(self, client, userdata, msg):
        if msg.topic == self.hit_topic:
            self.on_hit()

    def on_hit(self):
        print("Sending a hit...")
        if connected:
            sio.emit("hit","")

    def subscribe(self, client: mqtt_client):
        client.subscribe(self.hit_topic)
        client.on_message = self.on_message

    def read(self):
        self.client.loop_forever()

    @sio.event
    def connect():
        global connected
        print('Connected to Local Web Server!')
        connected = True

    @sio.event
    def disconnect():
        global connected
        print('disconnected from Local Web Server')
        connected = False
        # sys.exit()

