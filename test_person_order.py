from person import Person
import time


p1 = Person([200,0,3000,0])
p2 = Person([-99,0,3000,1])
p3 = Person([200,20,550,2])

persons = [p2, p1, p3]

persons_sorted = sorted(persons)
# persons_sorted = persons_sorted[0:2]

for person in persons_sorted:
    
    print(person)

d = dict()

# d[p1.id] = time.monotonic()
# time.sleep(0.6)
# d[p2.id] = time.monotonic()
# time.sleep(0.6)
# d[p3.id] = time.monotonic()


for key in list(d.keys()):

    if time.monotonic() - d[key] > 0.5:
        del d[key]

for e in d:
    print(e, d[e])
