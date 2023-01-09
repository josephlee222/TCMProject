import shelve
from flask import flash
from datetime import datetime, timedelta


class Medication:
    def __init__(self, name, description, duration_of_medication, no_of_pills, frequency_of_pills, notes):

        with shelve.open("tracker_count", writeback=True) as tracker_count:
            if "tracking_id" not in tracker_count:
                id = 1
            else:
                id = tracker_count["tracking_id"] + 1
            tracker_count["tracking_id"] = id

        try:
            self.id = id
            self.date = datetime.now().date()
            self.enddate = self.date + timedelta(days=int(duration_of_medication))
            self.name = str(name)
            self.description = str(description)
            self.duration_of_medication = int(duration_of_medication)
            self.no_of_pills = int(no_of_pills)
            self.frequency_of_pills = str(frequency_of_pills)
            self.notes = str(notes)
        except ValueError as e:
            print("Value error while entering medicine into Tracker class")
            flash(str(e))

    def getDate(self):
        return self.date

    def getEnddate(self):
        return self.enddate

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getDuration_of_medication(self):
        return self.duration_of_medication

    def getNo_of_pills(self):
        return self.no_of_pills

    def getFrequency_of_pills(self):
        return self.frequency_of_pills

    def getNotes(self):
        return self.notes

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

    def setDuration_of_medication(self, duration_of_medication):
        self.duration_of_medication = duration_of_medication
        self.enddate = self.date + timedelta(days=int(duration_of_medication))

    def setNo_of_pills(self, no_of_pills):
        self.no_of_pills = no_of_pills

    def setFrequency_of_pills(self,frequency_of_pills):
        self.frequency_of_pills = frequency_of_pills

    def setNotes(self, notes):
        self.notes = notes
