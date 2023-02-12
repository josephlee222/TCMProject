from time import time
from datetime import datetime

class Refund:
    def __init__(self, name, email, order, reason):
        self.__id = int(time() * 1000)
        self.__name = name
        self.__email = email
        self.__order = order
        self.__creationDate = datetime
        self.__reason = reason


    def getId(self):
        return self.__id

    def getname(self):
        return self.__name

    def getemail(self):
        return self.__email

    def getorder(self):
        return self.__order

    def getcreationDate(self):
        return self.__creationDate

    def getreason(self):
        return self.__reason

    def setname(self, name):
        self.__name = name

    def setemail(self, email):
        self.__email = email

    def setorder(self, order):
        self.__order = order

    def setreason(self, reason):
        self.__reason = reason