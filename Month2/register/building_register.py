import random

rooms = []
tenants = []


class Tenant:
    def __init__(self, fname, lname, num):
        self.account = 0
        self.fname = str(fname)
        self.lname = str(lname)
        self.num = num
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

    def remove_tenant(self):
        tenants.remove(self)
        rooms.remove(self.room)

    def pay_tenant(self, amt):
        self.account += amt

    def check_account(self):
        return self.account


def pay_tenant_(fname, recepientname, amt):
    # finding the tenant that is paying
    for tenant in tenants:
        if tenant.fname == fname:
            for r in tenants:
                if r.fname == recepientname:
                    tenant.pay_tenant((-amt))
                    r.pay_tenant(amt)


# create_tenants(50)
def show_tenants():
    for tenant in tenants:
        print(
            f"Tenant Name: {tenant.fname}, Tenant Lname: {tenant.lname}, Tenant Number: {tenant.num}, Tenant room: {tenant.room}"
        )


def find_tenant(attr):
    for tenant in tenants:
        if (
            tenant.fname == attr
            or tenant.lname == attr
            or tenant.num == attr
            or tenant.room == attr
        ):
            print(
                f"Tenant: {tenant.fname}, {tenant.lname}, number: {tenant.num}, room: {tenant.room} "
            )


def remove_tenant_(fname, lname):
    removal_list = []
    for tenant in tenants:
        if tenant.fname == fname and tenant.lname == lname:
            removal_list.append(tenant)
    for tenant in removal_list:
        if len(removal_list) > 1:
            print("More than one tenant with that name...")
            num = input("Please enter tenant number: ")
            if tenant.num == num:
                tenant.remove_tenant()
                print(f"Tenant: {fname, lname}, has been removed")
                return
            else:
                tenant.remove_tenant()
                print(f"Tenant: {fname, lname}, has been removed")
                return


def check_tenant_account(attr):
    for tenant in tenants:
        if tenant.fname == attr:
            return f"{tenant.fname}: {tenant.account}"


Tenant("stuart", "kieser", 171)
Tenant("nick", "fox", 909)


def create_tenants(number):
    fnames = ["harry", "george", "barry", "larry", "gary", "ben", "greg"]
    lnames = ["harary", "george", "barary", "larary", "garary", "been", "grog"]

    for tenants in range(number):
        fname = random.choice(fnames)
        lname = random.choice(lnames)
        num = random.choice(range(500, 1000))
        Tenant(fname, lname, num)
    return tenants


create_tenants(70)
