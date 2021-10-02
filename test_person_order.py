from person import Person



p1 = Person([98,0,3000,0])
p2 = Person([-99,0,3000,1])

persons = [p2, p1]

persons_sorted = sorted(persons)

for person in persons_sorted:
    
    print(person)