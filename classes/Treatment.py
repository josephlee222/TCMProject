from classes.Product import Product


class Treatment(Product):
    def __init__(self, name, description, benefits, price, salePrice, onSale, duration):
        super().__init__(name, description, benefits, price, salePrice, onSale)
        try:
            self.duration = float(duration)
        except ValueError:
            print("Value error while creating Treatment class")

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration
