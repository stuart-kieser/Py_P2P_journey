import random

rooms = []
tenants = []


class Tenant:
    def __init__(self, fname, lname, num):
        self.fname = str(fname)
        self.lname = str(lname)
        self.num = int(num)
        self.room = random.choice(range(0, 500))
        if self.room in rooms:
            try:
                self.room = int(input("Enter a new room number..."))
            except:
                self.room = False
        else:
            None
        tenants.append(self)
        rooms.append(self.room)
        print(f"Room {self.room} is available")


Tenant("Harry", "Potter", 1, 1)
