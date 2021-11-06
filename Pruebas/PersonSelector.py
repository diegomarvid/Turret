from person import Person
import time

class PersonSelector:

    def __init__(self):
        self.time_selected = 3
        self.current_index = -1
        self.last_index = 0
        self.start_time = 0
        self.current_time = 0
        

    def Select(self, msg):

        self.current_time = time.monotonic()

        if self.current_time - self.start_time >= self.time_selected:

            self.last_index = len(msg) - 1

            if self.current_index < self.last_index:
                self.current_index = self.current_index + 1
                self.start_time = self.current_time

            elif self.current_index == self.last_index:
                self.current_index = 0
                self.start_time = self.current_time

        if len(msg) > 0:
            return Person(msg[self.current_index])


            




        
