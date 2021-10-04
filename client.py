from multiprocessing.connection import Listener
from person import Person
from Turret import Turret
from PersonSelector import PersonSelector

PORT_CAMERA = 6000
PORT_MQTT = 5000

# address_camera = ('localhost', PORT_CAMERA)

# authkey_camera = "secret"
# encoded_authkey_camera = authkey_camera.encode('UTF-8')

# conn_camera = Client(address_camera, authkey=encoded_authkey_camera)

# address_mqtt = ('localhost', PORT_MQTT)

# authkey_mqtt = "secret1"
# encoded_authkey_mqtt = authkey_mqtt.encode('UTF-8')

# conn_mqtt = Client(address_mqtt, authkey=encoded_authkey_mqtt)

def createEncondedAuthkey():
        authkey = "secret1"
        return authkey.encode('UTF-8')

def initServer():
    address = ('localhost', 5000)     # family is deduced to be 'AF_INET'

    encoded_authkey = createEncondedAuthkey()

    listener = Listener(address, authkey = encoded_authkey)
    print(f"Server started at port: {5000}")
    print("Waiting for client...")

    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)   
    return conn
    

turret = Turret()
personSelector = PersonSelector()

def PrintPersons(detections):
    for person in detections:
        print(person, end = " ")
    print("")

conn = initServer()

while True:

    while conn.poll():
        msg = conn.recv()
        print(msg)
    # msg_camera = conn_camera.recv()
    # msg_mqtt = conn_mqtt.recv()

    # print(msg_camera, msg_mqtt)
    # PrintPersons(msg)

    # detectedPerson = personSelector.Select(msg)

    # turret.MoveTurretToPerson(detectedPerson)



conn.close()