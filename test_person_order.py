from person import Person



p1 = Person([98,0,3000,0])
p2 = Person([-99,0,3000,1])
p3 = Person([200,20,550,2])

persons = [p2, p3]

persons_sorted = sorted(persons)
persons_sorted = persons_sorted[0:2]

for person in persons_sorted:
    
    print(person)

print(p1 not in persons_sorted)