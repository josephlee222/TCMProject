class Tracker:
    def __init__(self, doctor_email, duration, notes):
        try:
            self.doctor_email = str(doctor_email)
            self.duration = float(duration)
            self.notes = str(notes)
        except ValueError:
            print("Value error while entering medicine into Tracker class")

    def getDuration(self):
        return self.duration

    def getNotes(self):
        return self.notes

    def setDuration(self,duration):
        self.duration = duration

    def setNotes(self, notes):
        self.notes = notes

class Medicine:

    def __init__(self, name, description, dosage):
        try:
            self.name = str(name)
            self.description = str(description)
            self.dosage = int(dosage)
        except ValueError:
            print('Value error while entering medicine into Medicine class')

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getDosage(self):
        return self.dosage

    def setName(self,name):
        self.name = name

    def setDescription(self,description):
        self.description = description

    def setDosage(self,dosage):
        self.dosage = dosage
