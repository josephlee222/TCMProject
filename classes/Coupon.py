class Coupon:
    def __init__(self, name, code, discount, validity, description=None):
        # Discount is in percentage
        try:
            self.name = str(name)
            self.description = description
            self.code = str(code)
            self.discount = int(discount)
            self.validity = str(validity)
        except ValueError:
            print("Value error occurred when creating Coupon class")

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getCode(self):
        return self.code

    def getDiscount(self):
        return self.discount

    def getValidity(self):
        return self.validity

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setDiscount(self, discount):
        self.discount = int(discount)

    def setValidity(self, validity):
        self.validity = validity