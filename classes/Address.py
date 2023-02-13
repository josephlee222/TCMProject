# Customer delivery address class
# Library to get map coordinates via address
from geopy.exc import GeopyError
from geopy.geocoders import ArcGIS


class Address:
    def __init__(self, name, location):
        try:
            geoLocater = ArcGIS(user_agent="TCMShifu")
            geoLocation = geoLocater.geocode(location)
        except GeopyError:
            self.latitude = None
            self.longitude = None
        else:
            self.latitude = geoLocation.latitude if geoLocation is not None else None
            self.longitude = geoLocation.longitude if geoLocation is not None else None
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

        try:
            geoLocater = ArcGIS(user_agent="TCMShifu")
            geoLocation = geoLocater.geocode(location)
        except GeopyError:
            self.latitude = None
            self.longitude = None
            return False
        else:
            if geoLocation is not None:
                self.location = location
                self.latitude = geoLocation.latitude
                self.longitude = geoLocation.longitude
                return True
            else:
                return False
