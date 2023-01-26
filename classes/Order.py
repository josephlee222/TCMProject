# Delivery Status:
# 1 - Preparing
# 2 - Wait for delivery
# 3 - Delivery
# 4 - Received
# 5 - Cancelled
from time import time

class Order:
    def __init__(self, userId, cart, address=None):
        self.id = int(time() * 1000)
        self.userId = userId
        self.cart = cart
        self.address = address
        self.status = 1

    def getId(self):
        return self.id

    def getUserId(self):
        return self.userId

    def getCart(self):
        return self.cart

    def getAddress(self):
        return self.address

    def getStatus(self):
        return self.status

    def setAddress(self, address):
        self.address = address

    def setStatus(self, status):
        self.status = status if 0 < status < 6 else 1