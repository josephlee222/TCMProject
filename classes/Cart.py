import shelve


class Cart:
    def __init__(self, itemId, quantity, type, item):
        self.itemId = itemId
        self.quantity = quantity
        self.consume = False
        self.storedItem = item
        if type != "treatments" or type != "products":
            self.type = type
        else:
            raise ValueError("Incorrect cart item type. Acceptable cart types are 'treatments' and 'products'.")

    def getItemId(self):
        return self.itemId

    def getItem(self):
        try:
            with shelve.open(self.type) as items:
                item = items[self.itemId]
                self.storedItem = item
                return item
        except KeyError:
            return False

    def updateStoredItem(self):
        with shelve.open(self.type) as items:
            self.storedItem = items[self.itemId]

    def getStoredItem(self):
        return self.storedItem

    def getQuantity(self):
        return self.quantity

    def getType(self):
        return self.type

    def isConsumed(self):
        return self.consume

    def consumeCart(self):
        self.consume = True

    # For order history where price is fixed already
    def getStoredPrice(self):
        item = self.storedItem
        if item.getOnSale():
            return item.getSalePrice() * float(self.quantity)
        else:
            return item.getPrice() * float(self.quantity)

    def getPrice(self):
        # This one calculates the total price of one item with multiple quantities (price * quantity)
        with shelve.open(self.type) as items:
            item = items[self.itemId]

            if item.getOnSale():
                return item.getSalePrice() * float(self.quantity)
            else:
                return item.getPrice() * float(self.quantity)

    def setQuantity(self, quantity):
        self.quantity = quantity
