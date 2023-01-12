import shelve


class Appointment:
    def __init__(self, name, userEmail, doctorEmail, date, time, notes):
        with shelve.open("counter", writeback=True) as counter:
            if "appointment" not in counter:
                id = 1
            else:
                id = counter["appointment"] + 1
            counter["appointment"] = id

            self.id = id
            self.name = str(name)
            self.userEmail = str(userEmail)
            self.doctorEmail = str(doctorEmail)
            self.date = date
            self.time = time
            self.notes = str(notes)

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getUserEmail(self):
        return self.userEmail

    #Returns a user class based on email
    def getUser(self):
        with shelve.open("users") as users:
            return users[self.userEmail]

    def getDoctorEmail(self):
        return self.doctorEmail

    # Returns a user class based on email
    def getDoctor(self):
        with shelve.open("users") as users:
            return users[self.doctorEmail]

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getNotes(self):
        return self.notes

    def setName(self, name):
        self.name = name

    def setUserEmail(self, email):
        self.userEmail = email

    def setDoctorEmail(self, email):
        self.doctorEmail = email

    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time

    def setNotes(self, notes):
        self.notes = notes