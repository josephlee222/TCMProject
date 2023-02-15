# Delivery Status:
# 1 - Preparing
# 2 - Wait for delivery
# 3 - Delivery
# 4 - Received
# 5 - Cancelled
# 6 - Refunded
from datetime import datetime
from time import time


class Order:
    def __init__(self, userId, cart, address=None, discount=0):
        self.id = int(time() * 1000)
        self.datetime = datetime.now()
        self.userId = userId
        self.cart = cart
        self.address = address
        self.status = 4
        self.discount = discount

        # Check the cart consists of products that needs delivering. If only treatments, set to finished because
        # there is nothing to deliver
        for item in self.cart:
            if item.getType() == "products":
                self.status = 1
                break

    def getId(self):
        return self.id

    def getUserId(self):
        return self.userId

    def getDateTime(self):
        return self.datetime

    def getCart(self):
        return self.cart

    def getAddress(self):
        return self.address

    def getStatus(self):
        return self.status

    def getStatusText(self):
        # I know there is match...case in python but I am writing this to be compatible with Python 3.9
        if self.status == 1:
            return "Preparing"
        elif self.status == 2:
            return "Wait for delivery"
        elif self.status == 3:
            return "Delivering"
        elif self.status == 4:
            return "Delivered"
        elif self.status == 5:
            return "Cancelled"
        elif self.status == 6:
            return "Refunded"
        else:
            return "Unknown"

    def setAddress(self, address):
        self.address = address

    def setStatus(self, status):
        self.status = status if 0 < status < 7 else 1

    def getCartGST(self):
        return round(self.getCartSubtotalPrice() * 0.08, 2)

    def getDiscount(self):
        return self.discount

    def getCartSubtotalPrice(self):
        price = 0
        for item in self.cart:
            price += item.getStoredPrice()

        return round(price, 2)

    def getTotalPrice(self):
        # +3 for delivery fee
        return round(self.getCartSubtotalPrice() + self.getCartGST() + self.getDeliveryPrice() - self.discount, 2)

    def getDeliveryPrice(self):
        for item in self.cart:
            if item.getType() == "products":
                return 3

        return 0
