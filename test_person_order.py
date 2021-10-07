from person import Person
import time
import json


p1 = Person([200,0,3000,0])
p2 = Person([-99,0,3000,1])
p3 = Person([200,20,550,2])

persons = [p2, p1, p3]

persons_sorted = sorted(persons)
# persons_sorted = persons_sorted[0:2]

for person in persons_sorted:
    
    print(person)

d = dict()

d[p1.id] = time.monotonic()

# time.sleep(0.6)
# d[p2.id] = time.monotonic()
# time.sleep(0.6)
# d[p3.id] = time.monotonic()

jsonstr = json.dumps([person.__dict__ for person in persons])

print(type(jsonstr))

detections = json.loads(jsonstr)

# for detection in detections:
#     person = Person(**detection)
#     print(person)

# for e in d:
#     print(e, d[e])
