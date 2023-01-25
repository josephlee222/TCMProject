from flask import flash

from classes.Address import Address
from classes.Cart import Cart


class User:
    def __init__(self, name, password, email, accountType, birthday=None, phone=None):
        try:
            self.name = str(name)
            self.password = str(password)
            self.email = str(email)
            self.accountType = str(accountType)
        except ValueError:
            print("Value error while creating User class")

        self.birthday = birthday
        self.phone = phone
        self.address = []
        self.medications = []
        self.cart = []

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
        return self.address

    def getMedications(self):
        return self.medications

    def getCart(self):
        if not hasattr(self, "cart"):
            # Updater code for old accounts
            self.cart = []

        return self.cart

    def getCartGST(self):
        return round(self.getCartSubtotalPrice() * 0.08, 2)

    def getCartSubtotalPrice(self):
        price = 0
        for item in self.cart:
            price += item.getPrice()

        return round(price, 2)

    def getTotalPrice(self):
        # +3 for delivery fee
        return round(self.getCartSubtotalPrice() + self.getCartGST() + 3, 2)

    def setPassword(self, password):
        self.password = password

    def setName(self, name):
        self.name = name

    def setAccountType(self, admin):
        self.accountType = admin

    def setBirthday(self, birthday):
        self.birthday = birthday

    def setPhone(self, phone):
        self.phone = phone

    # ONLY PASS IN ADDRESS CLASSES HERE, NO TEXT
    def setAddress(self, address):
        if isinstance(address, Address):
            self.address.append(address)
        else:
            raise ValueError("Only Address class values are accepted in setAddress")

    def addCartItem(self, cartItem):
        if isinstance(cartItem, Cart):
            self.cart.append(cartItem)
        else:
            raise ValueError("Only Cart class values are accepted in setCartItem")

    def setMedication(self, medication):
        if self.medications is None:
            self.medications = [medication]
        else:
            self.medications.append(medication)

    def setAddresses(self, addresses):
        self.address = addresses

    def setMedications(self, medications):
        self.medications = medications

    # ONLY PASS IN ADDRESS CLASSES HERE, NO TEXT
    def editAddress(self, id, address):
        try:
            self.address[id] = address
        except IndexError:
            flash("Unable to edit address, address does not exist.", category="error")
            return False

    def deleteAddress(self, id):
        try:
            self.address.pop(int(id))
        except IndexError:
            flash("Unable to edit address, address does not exist.", category="error")
            return False

    def deleteMedication(self, id):
        self.medications.pop(int(id))

