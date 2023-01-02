import shelve
from datetime import datetime
class Coupon:
    def __init__(self, name, code, discount, startDate, endDate, description=None):
        # Discount is in percentage
        # TODO: IMPROVE TYPE ENFORCEMENT TO REDUCE ERRORS

        with shelve.open("counter", writeback=True) as counter:
            if "coupon" not in counter:
                id = 1
            else:
                id = counter["coupon"] + 1
            counter["coupon"] = id

        try:
            self.id = id
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
        return self.validity

    def getEndDate(self):
        return self.validity

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setDiscount(self, discount):
        self.discount = int(discount)

    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    #Check coupon validate
    def isValid(self):
        if self.startDate <= datetime.now().date() <= self.endDate:
            return True

        return False