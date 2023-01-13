import itertools
import shelve


class Product:
    def __init__(self, name, description, benefits, price, details="", salePrice=0, onSale=0, images=[]):
        # Init class with safe measures
        with shelve.open("counter", writeback=True) as counter:
            if "shop" not in counter:
                id = 1
            else:
                id = counter["shop"] + 1
            counter["shop"] = id

        try:
            if type(images) != list:
                raise ValueError

            self.id = id
            self.name = str(name)
            self.description = str(description)
            self.benefits = str(benefits)
            self.details = str(details)
            self.price = float(price)
            self.salePrice = float(salePrice)
            self.onSale = bool(onSale)
            self.images = images
        except ValueError:
            print("Value error while creating Product class")
            return False

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getBenefits(self):
        return self.benefits

    def getDetails(self):
        return self.details

    def getPrice(self):
        return self.price

    def getSalePrice(self):
        return self.salePrice

    def getOnSale(self):
        return self.onSale

    def getImages(self):
        return self.images

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setBenefits(self, benefits):
        self.benefits = benefits

    def setDetails(self, details):
        self.details = details

    def setPrice(self, price):
        self.price = float(price)

    def setSalePrice(self, salePrice):
        self.salePrice = float(salePrice)

    def setOnSale(self, onSale):
        self.onSale = bool(onSale)

    def appendImage(self, path):
        self.images.append(path)

    def deleteImage(self, position):
        self.images.pop(int(position))
