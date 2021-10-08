import socketio
import time
import sys
import sched
import json
from person import Person

sio = socketio.Client()

global start_time

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def pong(data):
    global start_time
    print("Latency: ", (time.time() - start_time)* 1000)
    time.sleep(1)
    start_time = time.time()
    sio.emit("ping", "")

@sio.event
def disconnect():
    print('disconnected from server')
    sys.exit()

sio.connect('http://localhost:5000')


s = sched.scheduler(time.time, time.sleep)

p1 = Person([100,0,2000,0])
p2 = Person([-50, 100, 5540,1])
p3 = Person([50, 442, 120,2])

detections = [p1,p2,p3]

jsonstr = json.dumps([person.__dict__ for person in detections])

def send_detections(sc): 
    print("Sending detections...")
    sio.emit("camera", {'detections': jsonstr})
    # do your stuff
    s.enter(1, 1, send_detections, (sc,))

s.enter(1, 1, send_detections, (s,))
s.run()

start_time = time.monotonic()

# sio.emit("ping", "")

# sio.wait()