#!/usr/bin/env python

# Joride, 2013

import sys
sys.dont_write_bytecode = True

class BarcodeDictionary(object):
    """An instance of this class represents the barcode field in a passbook class.
    It performs some basic (i.e. non-exhaustive) validation on property values.
    If isValid property returns False, you can be sure that this object is not
    a valid barcode dictionary for a pass. However, if isValid returns True,
    this is not a guarantee that the barcode is really valid. Use iOS-devices
    console log to see what is wrong with the pass when it 'does not work'.
    """
    
    _formatValues = ('PKBarcodeFormatQR', 'PKBarcodeFormatPDF417', 'PKBarcodeFormatAztec',)
    
    def __init__(self, format = None, message = None, messageEncoding = 'iso-8859-1'):
        self._altText = None
        self._format = format
        self._message = message
        self._messageEncoding = messageEncoding

    def _setFormat(self, format):
        try:
            index = BarcodeDictionary._formatValues.index(format)
        except ValueError: 
            allowedValues = ''
            for anAllowedValue in BarcodeDictionary._formatValues:
                allowedValues += ("'"+anAllowedValue+"'" + ' ')
            message = ("Argument '%s', not allowed. Allowed values: %s" % (format ,allowedValues))
            raise ValueError(message)
            
        self._format = format
    def _getFormat(self):
        return self._format
        
    def _setAltText(self, altText):
        if type(altText ) != str:
            raise ValueError("Argument '%s' is not of type string" % altText)
        
        self._altText = altText
    def _getAltText(self):
        return self._altText
        
    def _getMessage(self):
        return self._message
    def _setMessage(self, message):
        if type(message ) != str:
            raise ValueError("Argument '%s' is not of type string" % message)
        
        self._message = message
    
    def _getMessageEncoding(self):
        return self._messageEncoding
    def _setMessageEncoding(self, messageEncoding):
        if type(messageEncoding ) != str:
            raise ValueError("Argument '%s' is not of type string" % messageEncoding)
        
        self._messageEncoding = messageEncoding
        
    def _isValid(self):
        # make sure the required properties are set (the setters take care of basic
        # value-checking, so we just check if those are not None)
        isValid = True
        invalidProperties = {}
        if self.format == None:
            invalidProperties['format'] = self.format
            isValid = False
        if self.message == None:
            invalidProperties['message'] = self.message
            isValid = False
        if self.messageEncoding == None:
            invalidProperties['messageEncoding'] = self.messageEncoding
            isValid = False
            
        if isValid == False:
            print "BarcodeDictionary invalid; erroneous properties: %s" % invalidProperties
            
        return isValid
        
    def _getDictionaryRepresentation(self):
        if self.isValid != True:
            print "not returning dictionaryRepresentation: invalid BarcodeDictionary:\n%s" % self
            return None
            
        # start out with the required keys
        returnDict = {'format' : self.format,
                      'message': self.message,
                      'messageEncoding' : self.messageEncoding}
        
        # add the optional ones if present. We rely on the isValid
        # method to make sure we only return a valid dictionary
        if self.altText != None:
            returnDict['altText'] = self.altText
            
        return returnDict
        
    def __str__(self):
        isValid = self.isValid
        return "{'altText': '%s'\n'\
        'format'' : '%s'\n\
        'message' : '%s'\n\
        'messageEncoding' : '%s'\n\
        'isValid' : '%s'}\n" % (self.altText,
        self.format,
        self.message,
        self.messageEncoding,
        isValid)
        
    altText = property(_getAltText, _setAltText, """String, optional. Text displayed near the barcode. For example, a human-readable version of the barcode data in case the barcode doesn't scan.""")
    format = property(_getFormat, _setFormat, """String, required. Barcode format. Must be one of the following values: 'PKBarcodeFormatQR', 'PKBarcodeFormatPDF417', 'PKBarcodeFormatAztec'.
    message
    string
""")
    message = property(_getMessage, _setMessage, """String, required. Message or payload to be displayed as a barcode.""")
    messageEncoding = property(_getMessageEncoding, _setMessageEncoding, """IANA character set name, as a string. Required. Text encoding that is used to convert the message from the string representation to a data representation to render the barcode. The value is typically iso-8859-1, but you may use another encoding that is supported by your barcode scanning infrastructure.""")
    
    dictionaryRepresentation = property(_getDictionaryRepresentation, None, """Returns a dictonary that can be converted to JSON if isValid property returns True, otherwise this method returns None.""")
    isValid = property(_isValid, None, """This method will True when no invalid or conflicting paramters are detected and all required properties have been set. It is recommended to call this method before placing this object in a Pass""")