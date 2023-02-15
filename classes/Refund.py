from datetime import datetime
from time import time


class Refund:
    def __init__(self, name, email, order, reason):
        self.__id = int(time() * 1000)
        self.__name = name
        self.__email = email
        self.__order = order
        self.__creationDate = datetime.now()
        self.__reason = reason
        self.__resolved = False

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getEmail(self):
        return self.__email

    def getOrder(self):
        return self.__order

    def getCreationDate(self):
        return self.__creationDate

    def getReason(self):
        return self.__reason

    def getResolved(self):
        return self.__resolved

    def setName(self, name):
        self.__name = name

    def setEmail(self, email):
        self.__email = email

    def setReason(self, reason):
        self.__reason = reason

    def setResolved(self):
        self.__resolved = True
