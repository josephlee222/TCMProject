import shelve

class Cart:
    def __init__(self, itemId, quantity, type):
        self.itemId = itemId
        self.quantity = quantity
        if type != "treatments" or type != "products":
            self.type = type
        else:
            raise ValueError("Incorrect cart item type. Acceptable cart types are 'treatments' and 'products'.")

    def getItemId(self):
        return self.itemId

    def getItem(self):
        with shelve.open(self.type) as items:
            item = items[self.itemId]
            return item

    def getQuantity(self):
        return self.quantity

    def getType(self):
        return self.type

    def getPrice(self):
        #This one calculates the total price of one item with multiple quantities (price * quantity)
        with shelve.open(self.type) as items:
            item = items[self.itemId]

            return item.getPrice() * float(self.quantity)

    def setQuantity(self, quantity):
        self.quantity = quantity