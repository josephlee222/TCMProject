class User:
    def __init__(self, name, password, email, accountType):
        self.name = name
        self.password = password
        self.email = email
        self.accountType = accountType
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

    def getAccountType(self):
        return self.accountType

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

    def setAccountType(self, admin):
        self.accountType = admin

    def setbirthday(self, birthday):
        self.birthday = birthday

    def setPhone(self, phone):
        self.phone = phone

    def setAddress(self, address):
        self.address = address

    def setPostal(self, postal):
        self.postal = postal