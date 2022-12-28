class Product:
    def __init__(self, name, description, benefits, price, salePrice, onSale, images):
        # Init class with safe measures
        try:
            if type(benefits) != list or type(images) != list:
                raise ValueError

            self.name = str(name)
            self.description = str(description)
            self.benefits = benefits
            self.price = float(price)
            self.salePrice = float(salePrice)
            self.onSale = bool(onSale)
        except ValueError:
            print("Value error while creating Product class")

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getBenefits(self):
        return self.benefits

    def getPrice(self):
        return self.price

    def getSalePrice(self):
        return self.name

    def getOnSale(self):
        return self.onSale

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setBenefits(self, benefits):
        self.benefits = benefits

    def setPrice(self, price):
        self.price = float(price)

    def setSalePrice(self, salePrice):
        self.salePrice = float(salePrice)

    def setOnSale(self, onSale):
        self.salePrice = bool(onSale)
