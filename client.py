from multiprocessing.connection import Client
from person import Person
from Turret import Turret
from PersonSelector import PersonSelector

PORT = 6000
address = ('localhost', PORT)

authkey = "secret"
encoded_authkey = authkey.encode('UTF-8')

conn = Client(address, authkey=encoded_authkey)

turret = Turret()
personSelector = PersonSelector()

def PrintPersons(detections):
    for person in detections:
        print(person, end = " ")
    print("")

while True:
    msg = conn.recv()

    # PrintPersons(msg)

    detectedPerson = personSelector.Select(msg)

    turret.MoveTurretToPerson(detectedPerson)



conn.close()