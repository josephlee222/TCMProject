from datetime import datetime
from time import time


class Coupon:
    def __init__(self, name, code, discount, startDate, endDate, description=None):
        # Discount is in percentage
        # TODO: IMPROVE TYPE ENFORCEMENT TO REDUCE ERRORS
        try:
            self.id = int(time() * 1000)
            self.name = str(name)
            self.description = description
            self.code = str(code)
            self.discount = int(discount)
            self.startDate = startDate
            self.endDate = endDate
        except ValueError:
            print("Value error occurred when creating Coupon class")

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getCode(self):
        return self.code

    def getDiscount(self):
        return self.discount

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate

    def setName(self, name):
        self.name = name

    def setCode(self, code):
        self.code = code

    def setDescription(self, description):
        self.description = description

    def setDiscount(self, discount):
        self.discount = int(discount)

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    # Check coupon validate
    def isValid(self):
        if self.startDate <= datetime.now().date() <= self.endDate:
            return True

        return False
