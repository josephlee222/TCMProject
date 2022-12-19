class User:
    def __init__(self, name, password, email, admin):
        self.name = name
        self.password = password
        self.email = email
        self.admin = admin
        self.birthday = None
        self.phone = None
        self.address = None
        self.postal = None

    def getName(self):
        return self.name

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getAdmin(self):
        return self.admin

    def getBirthday(self):
        return self.birthday

    def getPhone(self):
        return self.phone

    def getAddress(self):
        return  self.address

    def getPostal(self):
        return self.postal

    def setPassword(self, password):
        self.password = password

    def setName(self, name):
        self.name = name

    def setAdmin(self, admin):
        self.admin = admin

    def setbirthday(self, birthday):
        self.birthday = birthday

    def setPhone(self, phone):
        self.phone = phone

    def setAddress(self, address):
        self.address = address

    def setPostal(self, postal):
        self.postal = postal