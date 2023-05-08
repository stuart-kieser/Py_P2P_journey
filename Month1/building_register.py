import random

rooms = [1]
tenants = []


class Tenant:
    def __init__(self, fname, lname, num, room):
        self.fname = str(fname)
        self.lname = str(lname)
        self.num = int(num)
        self.room = room
        if self.room in rooms:
            self.room = room
            try:
                self.room = int(input("Enter a new room number..."))
                self.room != room
            except:
                self.room = False
        else:
            None
        tenants.append(self)
        rooms.append(room)
        print(f"Room {self.room} is available")


Tenant("Harry", "Potter", 1, 1)
