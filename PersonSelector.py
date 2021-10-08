from person import Person
import time

class AllHitException(Exception):
    pass

class PersonSelector:

    def __init__(self):
        self.time_selected = 10
        self.current_index = -1
        self.last_index = 0
        self.start_time = 0
        self.current_time = 0
        self.hit_persons = dict()
        self.remove_time = 20
    
        
    def MaximumTimeHasPassed(self):  
        return self.current_time - self.start_time >= self.time_selected

    def ChangeIndex(self):

        self.SetLastIndex()

        if self.current_index < self.last_index:
            self.current_index += 1
            self.start_time = self.current_time

        elif self.current_index == self.last_index:
            self.current_index = 0
            self.start_time = self.current_time

    def SetLastIndex(self):
        self.last_index = len(self.msg) - 1


    def GetPersonInIndex(self):
        if len(self.msg) > 0:
            return self.msg[self.current_index]

    def PersonHasNotBeenHitted(self, person):
        return person.id not in self.hit_persons

    def GotAHit(self):
        # self.ChangeIndex()
        HittedPerson = self.GetPersonInIndex()
        self.hit_persons[HittedPerson.id] = time.monotonic()

    def ChangeIndexToFirstAvailable(self):

        foundPerson = False

        begin_index = self.current_index

        while not foundPerson:

            self.ChangeIndex()

            nextPerson = self.GetPersonInIndex()

            foundPerson = self.PersonHasNotBeenHitted(nextPerson)

            #Si ya recorri la lista y volvi al mismo punto significa
            #Que todos estan manchados
            if begin_index == self.current_index:
                foundPerson = True
                raise AllHitException("Todas las personas estas manchadas")
                #Hacer algo

    #La persona esta manchada por un maximo de tiempo
    #Despues de este tiempo pasa como si no la mancho nunca
    def RemovePersonsFromListIfNecessary(self):

        for key in list(self.hit_persons.keys()):

            if self.current_time - self.hit_persons[key] > self.remove_time:

                del self.hit_persons[key]

    def GetFirstPersonNotHit(self):
        try:
            self.ChangeIndexToFirstAvailable()
            #Ahora trackeo a esta persona
            PersonaTrackeada = self.GetPersonInIndex()
            return PersonaTrackeada
        except AllHitException as e:
            print(e)
            return None
         
    def Select(self, msg):

        self.msg = msg

        self.current_time = time.monotonic()

        self.RemovePersonsFromListIfNecessary()

        if self.MaximumTimeHasPassed():

            self.ChangeIndex()

        # Aca esta trackeando a la persona en self.current_index
        PersonaTrackeada = self.GetPersonInIndex()

        if self.PersonHasNotBeenHitted(PersonaTrackeada):
            return PersonaTrackeada
        else:
            return self.GetFirstPersonNotHit()

            




        
