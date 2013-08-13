#!/usr/bin/env python

# Joride, 2013

import sys
sys.dont_write_bytecode = True

class Location(object):
    """
    Location dictionaries contain the followwing keys:\n\
        'altitude': value is a double, optional. Altitude in meters.\n\
        'latitude': value is a double, required. Latitude in degrees.\n\
        'longitude:'value is a double, required. Longitude in degrees.\n\
        'relevantText': value is a string, optional. Text displayed on the lock screen when the pass is currently relevant. For example, a description of the nearby location such as 'Store nearby on 1st and Main."""
    
    
    def __init__(self, latitude = None, longitude = None):
        if latitude == None or longitude == None:
            raise ValueError("Invalid arguments, both latitude ('%s') and longitude ('%s') required." % (latitude, longitude))
                    
        self.latitude = latitude
        self.longitude = longitude
        self._altitude = None
        self._relevantText = None
        
    def _setLatitude(self, latitude):
        if latitude > 90 or latitude < -90:
            raise ValueError("Invalid latitude ('%s'). Latitude ranges from -90 up to and including 90." % latitude)
        self._latitude = latitude
    def _getLatitude(self):
        return self._latitude
    
    def _setLongitude(self, longitude):
        if longitude > 180 or longitude < -180:
            raise ValueError("Invalid longitude ('%s'). Longitude ranges from -180 up to and including 180." % longitude)
        self._longitude = longitude
    def _getLongitude(self):
        return self._longitude
        
    def _setAltitude(self, altitude):    
        self._altitude = altitude
    def _getAltitude(self):
        return self._altitude
    def _setRelevantText(self, relevantText):
        self._relevantText = relevantText
    def _getRelevantText(self):
        return self._relevantText        
        
    def _getDictionaryRepresentation(self):
        # create a dict with required keys
        returnDict = {'longitude': self.longitude,
                      'latitude' : self.latitude}
                        
        # add optional keys when present
        if self.altitude != None:
            returnDict['altitude'] = self.altitude
        if self.relevantText != None:
            returnDict['relevantText'] = self.relevantText
            
        return returnDict
        
        
    dictionaryRepresentation = property(_getDictionaryRepresentation, None, """Returns the location as a dicitonary. Does not return None.""")
    longitude = property(_getLongitude, _setLongitude, doc="""value is a double, required. Longitude in degrees.""")
    latitude = property(_getLatitude, _setLatitude, doc="""value is a double, required. Latitude in degrees.""")
    altitude = property(_getAltitude, _setAltitude, doc="""value is a double, optional. Altitude in meters.""")
    relevantText = property(_getRelevantText, _setRelevantText, """value is a string, optional. Text displayed on the lock screen when the pass is currently relevant. For example, a description of the nearby location such as 'Store nearby on 1st and Main.""")