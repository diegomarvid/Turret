import socketio
import time
import sys

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


start_time = time.monotonic()

sio.emit("ping", "")

sio.wait()