# Customer delivery address class
# Library to get map coordinates via address
from flask import flash
from geopy.geocoders import ArcGIS
from geopy.exc import GeopyError

class Address:
    def __init__(self, name, location):
        try:
            geoLocater = ArcGIS(user_agent="TCMShifu")
            geoLocation = geoLocater.geocode(location)
        except GeopyError:
            self.latitude = 0
            self.longitude = 0
            flash("Error has occurred when getting information from the location provider", category="Error")
        else:
            self.latitude = geoLocation.latitude
            self.longitude = geoLocation.longitude
        finally:
            self.name = name
            self.location = location


    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def setName(self, name):
        self.name = name

    def setLocation(self, location):
        self.location = location
        try:
            geoLocater = ArcGIS(user_agent="TCMShifu")
            geoLocation = geoLocater.geocode(location)
        except GeopyError:
            self.latitude = 0
            self.longitude = 0
        else:
            self.latitude = geoLocation.latitude
            self.longitude = geoLocation.longitude


