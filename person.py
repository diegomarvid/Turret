class Person:

    def __init__(self,detection):
        self.x = detection[0]
        self.y = detection[1]
        self.z = detection[2]
        self.id = detection[3]

    def __str__(self):
        return f"[{self.id}] | ({self.x}, {self.y}, {self.z}) mm"