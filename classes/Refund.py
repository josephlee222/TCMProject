class Refund:
    def __init__(self, fname, lname, email, product, reason):
        self.__fname = fname
        self.__lname = lname
        self.__email = email
        self.__product = product
        self.__reason = reason

    def getfname(self):
        return self.__fname

    def getlname(self):
        return self.__lname

    def getemail(self):
        return self.__email

    def getproduct(self):
        return self.__product

    def getreason(self):
        return self.__reason

    def setfname(self, fname):
        self.__fname = fname

    def setlname(self, lname):
        self.__lname = lname

    def setemail(self, email):
        self.__email = email

    def setproduct(self,product):
        self.__product = product

    def setreason(self, reason):
        self.__reason = reason