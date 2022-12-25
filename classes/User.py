from flask import flash


class User:
    def __init__(self, name, password, email, accountType):
        self.name = name
        self.password = password
        self.email = email
        self.accountType = accountType
        self.birthday = None
        self.phone = None
        self.address = None

    def getName(self):
        return self.name

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getAccountType(self):
        return self.accountType

    def getBirthday(self):
        return self.birthday

    def getPhone(self):
        return self.phone

    def getAddress(self):
        return  self.address

    def setPassword(self, password):
        self.password = password

    def setName(self, name):
        self.name = name

    def setAccountType(self, admin):
        self.accountType = admin

    def setbirthday(self, birthday):
        self.birthday = birthday

    def setPhone(self, phone):
        self.phone = phone

    # ONLY PASS IN ADDRESS CLASSES HERE, NO TEXT
    def setAddress(self, address):
        if self.address == None:
            self.address = [address]
        else:
            self.address.append(address)

    # ONLY PASS IN ADDRESS CLASSES HERE, NO TEXT
    def editAddress(self, id, address):
        try:
            self.address[id] = address
        except IndexError:
            flash("Unable to edit address, address does not exist.", category="error")
            return False

    def deleteAddress(self, id):
        try:
            self.address.pop(id)
        except IndexError:
            flash("Unable to edit address, address does not exist.", category="error")
            return False