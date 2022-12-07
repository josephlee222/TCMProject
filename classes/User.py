class User:
    def __init__(self, username, password, email, admin):
        self.username = username
        self.password = password
        self.email = email
        self.admin = admin
        self.phone = None
        self.address = None
        self.postal = None

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getAdmin(self):
        return self.admin

    def getPhone(self):
        return self.phone

    def getAddress(self):
        return  self.address

    def getPostal(self):
        return self.postal

    def setPassword(self, password):
        self.password = password

    def setEmail(self, email):
        self.email = email

    def setAdmin(self, admin):
        self.admin = admin

    def setPhone(self, phone):
        self.phone = phone

    def setAddress(self, address):
        self.address = address

    def setPostal(self, postal):
        self.postal = postal