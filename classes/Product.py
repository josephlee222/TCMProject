from time import time

from marko import convert


class Product:
    def __init__(self, name, description, benefits, price, salePrice=0, onSale=0, quantity=1):
        # Init class with safe measures

        try:
            self.id = int(time() * 1000)
            self.name = str(name)
            self.description = str(description)
            self.benefits = str(benefits)
            self.price = round(float(price), 2)
            self.salePrice = round(float(salePrice), 2)
            self.onSale = bool(onSale)
            self.quantity = quantity
            self.images = []
        except ValueError:
            print("Value error while creating Product class")
            return False

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getConvertedDescription(self):
        return convert(self.description)

    def getBenefits(self):
        return self.benefits

    def getConvertedBenefits(self):
        return convert(self.benefits)

    def getPrice(self):
        return self.price

    def getSalePrice(self):
        return self.salePrice

    def getOnSale(self):
        return self.onSale

    def getImages(self):
        return self.images

    def getQuantity(self):
        return self.quantity

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setBenefits(self, benefits):
        self.benefits = benefits

    def setPrice(self, price):
        self.price = round(float(price), 2)

    def setSalePrice(self, salePrice):
        self.salePrice = round(float(salePrice), 2)

    def setOnSale(self, onSale):
        self.onSale = bool(onSale)

    def setQuantity(self, quantity):
        self.quantity = quantity

    def appendImage(self, path):
        self.images.append(path)

    def deleteImage(self, position):
        self.images.pop(int(position))
