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

    def clearCart(self):
        self.cart = []

    def getCart(self, fixed=False):
        if not fixed:
            self.checkCart()
        return self.cart

    def checkCart(self):
        changed = False
        for index, item in enumerate(self.cart):
            product = item.getItem()
            if not product:
                # Check if product is deleted
                self.cart.pop(index)
                changed = True
            else:
                # Check quantity status
                if item.getType() == "products":
                    if product.getQuantity() == 0:
                        self.cart.pop(index)
                        changed = True
                    elif product.getQuantity() < item.getQuantity():
                        self.cart[index].setQuantity(product.getQuantity())
                        changed = True

        if changed:
            flash("Your cart has been modified to reflect stock changes and product deletion.", category="warning")

    def updateCart(self):
        for item in self.cart:
            item.updateStoredItem()

    def getCartGST(self):
        return round(self.getCartSubtotalPrice() * 0.08, 2)

    def getCartSubtotalPrice(self):
        self.updateCart()
        price = 0
        for item in self.cart:
            price += item.getPrice()

        return round(price, 2)

    def getTotalPrice(self):
        # +3 for delivery fee
        return round(self.getCartSubtotalPrice() + self.getCartGST() + self.getDeliveryPrice(), 2)

    def getDeliveryPrice(self):
        for item in self.cart:
            if item.getType() == "products":
                return 3

        return 0

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
            return True
        except IndexError:
            # Fuck me
            return False

    def deleteMedication(self, id):
        self.medications.pop(int(id))
