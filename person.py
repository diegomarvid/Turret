import math

class Person:

    def __init__(self,detection):
        self.x = detection[0]
        self.y = detection[1]
        self.z = detection[2]
        self.id = detection[3]

    def GetDistance(self):
        return  math.sqrt(self.x ** 2 + self.y ** 2 + self.z **2)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.GetDistance() < other.GetDistance()

    def __str__(self):
        return f"[{self.id}] | ({self.x}, {self.y}, {self.z}) mm"