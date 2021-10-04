import json
from types import SimpleNamespace
from paho.mqtt import client as mqtt_client
from multiprocessing.connection import Client

class MQTTReciever:

    def __init__(self):
        self.broker = 'broker.hivemq.com'
        self.port = 1883
        self.hit_topic = "LaserTag"
        self.client_id = "turret_raspberry_pi"

        self.client = self.connect_mqtt()

        self.subscribe(self.client)

        self.encoded_authkey = self.createEncondedAuthkey()
        self.port = 5000
        self.conn = None

        self.initClient()

    def createEncondedAuthkey(self):
        authkey = "secret1"
        return authkey.encode('UTF-8')

    def initClient(self):
        address_mqtt = ('localhost', 5000)

        authkey_mqtt = "secret1"
        encoded_authkey_mqtt = authkey_mqtt.encode('UTF-8')

        self.conn = Client(address_mqtt, authkey=encoded_authkey_mqtt)   

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
        self.conn.send("Targeted player has been changed...")

    def subscribe(self, client: mqtt_client):
        client.subscribe(self.hit_topic)
        client.on_message = self.on_message

    def read(self):
        self.client.loop_forever()

