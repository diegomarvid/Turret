from person import Person
from Turret import Turret
from PersonSelector import PersonSelector

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

turret = Turret()
personSelector = PersonSelector()

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def ping(sid, data):
    sio.emit("pong", "")

@sio.event
def hit(sid,data):
    print("Ouch!")
    # personSelector.GotAHit()

@sio.event
def camera(sid,data):
    detections = data.detections
    detectedPerson = personSelector.Select(detections)
    turret.MoveTurretToPerson(detectedPerson)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)