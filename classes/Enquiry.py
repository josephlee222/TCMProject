from datetime import datetime
from time import time

from flask import flash


class Enquiry:
    def __init__(self, name, email, purpose, subject, query):

        try:
            self.id = int(time() * 1000)
            self.date = datetime.now().date()
            self.name = str(name)
            self.email = email
            self.purpose = purpose
            self.subject = subject
            self.query = query
            self.resolved = 'Not resolved'
        except ValueError as e:
            print("Value error while entering enquiry into Enquiry class")
            flash(str(e))

    def getId(self):
        return self.id

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getPurpose(self):
        return self.purpose

    def getSubject(self):
        return self.subject

    def getQuery(self):
        return self.query

    def getResolved(self):
        return self.resolved

    def setName(self, name):
        self.name = name

    def setEmail(self, email):
        self.email = email

    def setPurpose(self, purpose):
        self.purpose = purpose

    def setSubject(self, subject):
        self.subject = subject

    def setQuery(self, query):
        self.query = query

    def setResolved(self, resolved):
        if resolved != None:
            self.resolved = resolved
        else:
            self.resolved = 'Not resolved'
