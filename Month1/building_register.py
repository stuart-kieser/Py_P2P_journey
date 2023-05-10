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
                self.room = random.choice(range(0, 500))
            except:
                self.room = None
        else:
            None
        tenants.append(self)
        rooms.append(self.room)
        print(f"Tenant: {fname, lname} has been added to the register")
        print(f"Room {self.room} is available")


Tenant("stuart", "kieser", "071")


def create_tenants(number):
    fnames = ["harry", "george", "barry", "larry", "gary", "ben", "greg"]
    lnames = ["harary", "george", "barary", "larary", "garary", "been", "grog"]

    for tenants in range(number):
        fname = random.choice(fnames)
        lname = random.choice(lnames)
        num = random.choice(range(500, 1000))
        Tenant(fname, lname, num)
    return tenants


create_tenants(50)
for tenant in tenants:
    print(
        f"Tenant Name: {tenant.fname}, Tenant Lname: {tenant.lname}, Tenant Number: {tenant.num}, Tenant room: {tenant.room}"
    )
