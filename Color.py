#!/usr/bin/env python

# Joride, 2013

import sys
sys.dont_write_bytecode = True

class Color(object):
    """Represents a solid RGB color (no transparency). Initialize it with all
    its values (RG and B). Call stringRepresentation to get a representation that is
    usabel in a passbook-pass"""
    
    def __init__(self, red = None, green = None, blue = None):        
        if red == None or green == None or blue == None:
            raise ValueError("A Color object must be initialized with all three colors (red, green and blue")
        
        self._red = red
        self._green = green
        self._blue = blue
        
    def _getStringRepresentation(self):
        return "rgb(%s, %s, %s)" % (self._red, self._green, self._blue)
        
    stringRepresentation = property(_getStringRepresentation, None, doc="""Returns a string of the form 'rgb(rrr, ggg, bbb)', where rrr is the redvalue, ggg the green value and bbb the blue value. These range 0-255. For example: 'rgb(255, 100, 0)'.""")