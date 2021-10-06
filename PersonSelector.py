from person import Person
import time

class PersonSelector:

    def __init__(self):
        self.time_selected = 3
        self.current_index = -1
        self.last_index = 0
        self.start_time = 0
        self.current_time = 0
        self.hit_persons = dict()
        self.remove_time = 2
        
    def MaximumTimeHasPassed(self):  
        return self.current_time - self.start_time >= self.time_selected

    def ChangeIndex(self, msg):

        self.SetLastIndex(msg)

        if self.current_index < self.last_index:
            self.current_index += 1
            self.start_time = self.current_time

        elif self.current_index == self.last_index:
            self.current_index = 0
            self.start_time = self.current_time

    def SetLastIndex(self, msg):
        self.last_index = len(msg) - 1


    def GetPersonInIndex(self, msg):
        if len(msg) > 0:
            return msg[self.current_index]

    def PersonHasNotBeenHitted(self, person):
        return self.hit_persons.get(person.id) == None

    def GotAHit(self, msg):
        HittedPerson = self.GetPersonInIndex(msg)
        self.hit_persons[HittedPerson.id] == time.monotonic()

    def ChangeIndexToFirstAvailable(self, msg):

        foundPerson = False

        begin_index = self.current_index

        while not foundPerson:

            self.ChangeIndex(msg)

            nextPerson = self.GetPersonInIndex(msg)

            foundPerson = self.PersonHasNotBeenHitted(nextPerson)

            #Si ya recorri la lista y volvi al mismo punto significa
            #Que todos estan manchados
            if begin_index == self.current_index:
                foundPerson = True
                #Hacer algo

    def RemovePersonsFromListIfNecessary(self):

        for key in list(self.hit_persons.keys()):

            if self.current_time - self.hit_persons[key] > self.remove_time:

                del self.hit_persons[key]

   
         
    def Select(self, msg):

        self.current_time = time.monotonic()

        self.RemovePersonsFromListIfNecessary()

        if self.MaximumTimeHasPassed():

            self.ChangeIndex(msg)

        # Aca esta trackeando a la persona en self.current_index
        PersonaTrackeada = self.GetPersonInIndex(msg)

        if self.PersonHasNotBeenHitted(PersonaTrackeada):
            return PersonaTrackeada
        else:
            #Cambio el indice al primero que no este manchado
            self.ChangeIndexToFirstAvailable(msg)
            #Ahora trackeo a esta persona
            PersonaTrackeada = self.GetPersonInIndex(msg)
            return PersonaTrackeada

            




        
