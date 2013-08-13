#!/usr/bin/env python

# Joride, 2013

class FieldDictionary(object):
    """ This class represents a headerField for a pass. Initialize an instance with a key and a value. Set
    additional properties as needed. Non-exhaustive validation is performed on setting the values. When 
    assigning an instance of this class to a Pass, make sure the isValid property returns True. If this property
    returns False, you can be sure that the resulting pass will be invalid. If the method returns True, it is NOT
    a guarantee that the pass will be valid. (Check the pass-error messages and iOS-device console log (in that order)
    to find out what went wrong in case passes 'do not work'.
    
    A fieldDictionary contains the following keys:\n\
    'changeMessage': value is localizable format string. Format string for the alert text that is displayed when the pass is updated. The format string must contain the escape %@, which is replaced with the field's new value. For example, 'Gate changed to %@.' If you don't specify a change message, the user isn't notified when the field changes.\
    'key': value is string. Required. The key must be unique within the scope of the entire pass. For example, 'departure-gate'.\n\
    'value': value is a localizable string, ISO 8601 date as a string, or number. Required. Value of the field. For example, 42.\n\
    'label': value is a localizable string. Optional. Label text for the field.\n\
    'textAlignment': value is a string. Optional. Alignment for the field's contents. Must be one of the following values: PKTextAlignmentLeft, PKTextAlignmentCenter, PKTextAlignmentRight, PKTextAlignmentNatural. The default value is natural alignment, which aligns the text appropriately based on its script direction. This key is not allowed for primary fields.\n\n
    If any of the following keys is present, the value of the field is treated as a date. Either specify both a date style and a time style or neither.
    'dateStyle': value is a string. Style of date to display. Must be one of the following values: 'PKDateStyleNone', 'PKDateStyleShort', 'PKDateStyleMedium', 'PKDateStyleLong', 'PKDateStyleFull'\n\
    'timeStyle': value is a string. Style of date to display. Must be one of the following values: 'PKDateStyleNone', 'PKDateStyleShort', 'PKDateStyleMedium', 'PKDateStyleLong', 'PKDateStyleFull'\n\
    'isRelative': \n\
    The following keys are optional if the field's value is a number; otherwise they are not allowed. Only one of these keys is allowed per field.
    'currencyCode': value is a string. ISO 4217 currency code for the field's value.\n\
    'numberStyle': value is a string. Style of number to display. Must be one of the following values: 'PKNumberStyleDecimal', 'PKNumberStylePercent', PKNumberStyleScientific', 'PKNumberStyleSpellOut'."""
    
    _textAlignmentValues = ('PKTextAlignmentLeft', 'PKTextAlignmentCenter', 'PKTextAlignmentRight', 'PKTextAlignmentNatural',)
    _dateAndTimeStyles = ('PKDateStyleNone', 'PKDateStyleShort', 'PKDateStyleMedium', 'PKDateStyleLong', 'PKDateStyleFull',)
    _numberStyles = ('PKNumberStyleDecimal', 'PKNumberStylePercent', 'PKNumberStyleScientific', 'PKNumberStyleSpellOut',)
    
    def __init__(self, key = None, value = None):
        self._changeMessage = None
        self._key = key
        self._value = value
        self._label = None
        self._setTextAlignment = None
        self._dateStyle = None
        self._timeStyle = None
        self._isRelative = None
        self._currencyCode = None
        self._numberStyle = None
        self._textAlignment = None
        
    def _getCurrencyCode(self):
        return self._currencyCode
        
    def _setCurrencyCode(self, currencyCode):
        # make sure the value is of type string
        if (type(currencyCode) != str):
            errorMessage = "currencyCode ('%s') must be of type string" % (currencyCode,)
            raise ValueError(errorMessage)
        
        # make sure there is not currency code
        if self._numberStyle != None:
            raise ValueError("Trying to set currencyCode, but there is already a numberStyle set ('%s'). Either set a numberStyle, or a currencyCode, or neither." % self._numberStyle)
            
        # make sure the value-property is numeric, if it has been set already
        if (self._value != None):
            if (isinstance(self._value, (int, long, float,)) != True): 
                message = "Setting a currencyCode ('%s'), but the value property is not numeric ('%s')." % (currencyCode, self._value)
                raise ValueError(message)
                
        # all clear
        self._currencyCode = None
        
    def _getNumberStyle(self):
        return self._numberStyle
    def _setNumberStyle(self, numberStyle):
        # make sure the value is one of the possible values
        try:
            index = FieldDictionary._numberStyles.index(numberStyle)
        except ValueError: 
            allowedValues = ''
            for anAllowedValue in FieldDictionary._numberStyles:
                allowedValues += ("'"+anAllowedValue+"'" + ' ')
            message = ("Argument '%s', for numberStyle not allowed. Allowed values: %s" % (numberStyle ,allowedValues))
            raise ValueError(message)
        
        # make sure there is not currency code
        if self._currencyCode != None:
            raise ValueError("Trying to set numberStyle, but there is already a currencyCode set ('%s'). Either set a numberStyle, or a currencyCode, or neither." % self._currencyCode)
            
        # make sure the value-property is numeric, if it has been set already
        if (self._value != None):
            if (isinstance(self._value, (int, long, float,)) != True): 
                message = "Setting a numberStyle ('%s'), but the value property is not numeric ('%s')." % (numberStyle, self._value)
                raise ValueError(message)
                
        # all clear
        self._numberStyle = None
        
        
    def _getIsRelative(self):
        return self._isRelative
    def _setIsRelative(self, isRelative):
        if (isRelative != False) and (isRelative != True):
            raise ValueError("Argument should be 'False' or 'True'")
        self._isRelative = isRelative
        
    def _getDateStyle(self):
        return self._dateStyle
    def _setDateStyle(self, dateStyle):
        self._validateDateTimeValue(dateStyle)
        self._dateStyle = dateStyle
        
    def _getTimeStyle(self):
        return self._timeStyle
    def _setTimeStyle(self, timeStyle):
        self._validateDateTimeValue(timeStyle)
        self._timeStyle = timeStyle
    
    def _getTextAlignment(self):
        return self._textAlignment
    def _setTextAlignment(self, textAlignment):
        try:
            index = FieldDictionary._textAlignmentValues.index(textAlignment)
        except ValueError: 
            allowedValues = ''
            for anAllowedValue in FieldDictionary._textAlignmentValues:
                allowedValues += ("'"+anAllowedValue+"'" + ' ')
            message = ("Argument '%s', not allowed. Allowed values: %s" % (styleKey ,allowedValues))
            raise ValueError(message)
            
        self._textAlignment = textAlignment
        
    def _getLabel(self):
        return self._label
    def _setLabel(self, label):
        if (type(label) != str):
            errorMessage = "label ('%s') must be of type string" % (label,)
            raise ValueError(errorMessage)
            
        self._label = label

    def _getValue(self):
        return self._value
    def _setValue(self, value):
        # check the value
        if (type(value) != str) and (isinstance(value, (int, long, float,)) != True):
            errorMessage = "Value '%s' must be of type string or numeric." % (value,)
            raise ValueError(errorMessage)
        
        # make sure that if there is a datestyle of timestyle the value is a string
        if (self._dateStyle != None) or (self._timeStyle != None):
            if type(value != str):
                errorMessage = "Datestyle or timeStyle set, the value must be a string. It is now '%s'." % (value,)
                raise ValueError(errorMessage)
        
        # make sure that if there is a currencyCode of numberStyle the value is a number
        if (self._currencyCode != None) or (self._numberStyle != None):
            if (isinstance(value, (int, long, float,)) != True):
                errorMessage = "CurrencyCode or NumberStyle set, the value must be numeric. It is now '%s'." % (value,)
                raise ValueError(errorMessage)
    
        self._value = value
    
    def _getKey(self):
        return self._key
    def _setKey(self, key):
        # set the key (must be of type string)
        if (type(key) != str):
            errorMessage = "Key ('%s') must be of type string" % (key,)
            raise ValueError(errorMessage)
        
        self._key = key
        
    
    def _getChangeMessage(self):
        return self._changeMessage
    def _setChangeMessage(self, changeMessage):
        # set the message (must be of type string)
        if (type(changeMessage) != str):
            errorMessage = "changeMessage ('%s') must be of type string" % (changeMessage,)
            raise ValueError(errorMessage)
            
        self._changeMessage = changeMessage
        
    def _validateDateTimeValue(self, dateTimeValue):
        if type(dateTimeValue) == str:
            # the value needs to be in the allowed values tuple
            try:
                index = FieldDictionary._dateAndTimeStyles.index(dateTimeValue)
            except ValueError: 
                allowedValues = ''
                for anAllowedValue in FieldDictionary._dateAndTimeStyles:
                    allowedValues += ("'"+anAllowedValue+"'" + ' ')
                message = "Value '%s' must be one of the following values: %s." % allowedValues
                raise ValueError(message)
            
        # the value is allright, now let's make sure that the property value is a string
        if self.value != None:
            # if it is not none, it must be a string (specifically a W3C date)
            if type(self.value) != str:
                message = "A dateStyle or timeStyle is being set, so the value property must be a W3C datestring (it is now '%s')" % self.value
                raise ValueError(message)
                
    def _getIsValid(self):
        if self.key == None:
            print("Property 'key' not set.")
            return False
        if self.value == None:
            print("Property 'value' not set.")
            return False
        if (self.numberStyle != None and self.currencyCode != None):
            print("Property 'numberStyle' set ('%s') and property 'currencyCode' set ('%s'). Only set one of these properties or none." % (self.numberStyle, self.currencyCode))
            return False
        if (self.numberStyle != None or self.currencyCode != None):
            if (isinstance(self._value, (int, long, float,)) != True):
                print("Property 'value' set to a non-numeric value ('%s'), but a currencyCode ('%s') or numberStyle ('%s') has been set requiring the value to be numeric." % (self.value, self.currencyCode, self.numberStyle,))
                return False
            if (self.dateStyle != None) or (self.timeStyle != None):
                print ("Property 'numberStyle' ('%s') or 'currencyCode' ('%s') has been set but also 'dateStyle' ('%s') or 'timeStyle' ('%s'). Either set a numberStyle or currencyCode or set a dateStyle and timeStyle. ")
                return False
        if ((self.dateStyle != None) and (self.timeStyle == None)) or ((self.dateStyle == None) and (self.timeStyle != None)):
            print("Either set both 'timeStyle' ('%s') and 'dateStyle' ('%s') properties or none." % (self.timeStyle, self.dateStyle))
            return False
        if (self.dateStyle != None or self.timeStyle != None):
            if type(self.value) != str:
                print("'dateStyle' and 'timeStyle' ('%s') set, so 'value' ('%s') property ('%s') must be a string indicating a date." % (self.timeStyle, self.dateStyle, self.value))
                return False
        # all OK.
        return True
        
    def _getDictionaryRepresentation(self):
        if self.isValid != True:
            print "not returning dictionaryRepresentation: invalid FieldDictionary:\n%s" % self
            return None
            
        # start out with the required keys
        returnDict = {'key' : self.key,
                      'value': self.value}
        
        # add the optional ones if present. We rely on the isValid
        # method to make sure we only return a valid dictionary
        if self.label != None:
            returnDict['label'] = self.label
        if self.textAlignment != None:
            returnDict['textAlignment'] = self.textAlignment
        if self.numberStyle != None:
            returnDict['numberStyle'] = self.numberStyle
        if self.currencyCode != None:
            returnDict['currencyCode'] = self.currencyCode
        if self.timeStyle != None:
            returnDict['timeStyle'] = self.timeStyle
        if self.dateStyle != None:
            returnDict['dateStyle'] = self.dateStyle
        if self.isRelative != None:
            returnDict['isRelative'] = self.isRelative
        if self.changeMessage != None:
            returnDict['changeMessage'] = self.changeMessage
            
        return returnDict

                
    isValid = property(_getIsValid, None, doc="""This method will True when no invalid or conflicting paramters are detected and all required properties have been set. It is recommended to call this method before placing this object in a Pass""")
    key = property(_getKey, _setKey, doc="""Value is string. Required. The key must be unique within the scope of the entire pass. For example, 'departure-gate'.""")
    value = property(_getValue, _setValue, doc="""Value is a localizable string, ISO 8601 date as a string, or number. Required. Value of the field. For example, 42.""")
    label = property(_getLabel, _setLabel, doc="""Value is a localizable string. Optional. Label text for the field.""")
    textAlignment = property(_getTextAlignment, _setTextAlignment, doc="""Value is a string. Optional. Alignment for the field's contents. Must be one of the following values: 'PKTextAlignmentLeft', 'PKTextAlignmentCenter', PKTextAlignmentRight, 'PKTextAlignmentNatural'. The default value is natural alignment, which aligns the text appropriately based on its script direction. This key is not allowed for primary fields.""")
    
    numberStyle = property(_getNumberStyle, _setNumberStyle, doc="""Value is a string.  Optional. Style of number to display. Must be one of the following values: 'PKNumberStyleDecimal', 'PKNumberStylePercent', 'PKNumberStyleScientific', 'PKNumberStyleSpellOut'. When this property is set, do not set a currencyCode. When a currencyCode is set, trying to set this property will raise an error.""")
    
    currencyCode = property(_getCurrencyCode, _setCurrencyCode, doc="""Value is a string. Optional. ISO 4217 currency code for the field's value. When this property is set, do not set a numberStyle. When a numberStyle is set, trying to set this property will raise an error.""")
    
    timeStyle = property(_getTimeStyle, _setTimeStyle, doc="""Value is a string. Style of date to display. Must be one of the following values: 'PKDateStyleNone', 'PKDateStyleShort', 'PKDateStyleMedium', 'PKDateStyleLong', 'PKDateStyleFull.\n\
        If this property is set, the value of the field-property will be treated as a date. Also specify a date style or don't specify both a dateStyle and a timeStyle.'""")
    dateStyle = property(_getDateStyle, _setDateStyle, doc="""Value is a string. Optional. Style of date to display. Must be one of the following values: 'PKDateStyleNone', 'PKDateStyleShort', 'PKDateStyleMedium', 'PKDateStyleLong', 'PKDateStyleFull.\n\
    If this property is set, the value of the field-property will be treated as a date. Also specify a time style or don't specify both a dateStyle and a timeStyle.'""")
    isRelative = property(_getIsRelative, _setIsRelative, doc="""Boolean, optional. If true, the label's value is displayed as a relative date; otherwise, it is displayed as an absolute date. The default value is false.""")
    
    changeMessage = property(_getChangeMessage, _setChangeMessage, doc="""Value is localizable format string. Optional Format string for the alert text that is displayed when the pass is updated. The format string must contain the escape %@, which is replaced with the field's new value. For example, 'Gate changed to %@.' If you don't specify a change message, the user isn't notified when the field changes.""")
    
    dictionaryRepresentation = property(_getDictionaryRepresentation, None, """Returns a dictonary that can be converted to JSON if isValid property returns True, otherwise this method returns None.""")
    
    def __str__(self):
        # calling the getter for this property WILL print out an error message
        # in case it is not valid
        isValid = self.isValid
        return "{'key': '%s'\n'\
        'value'' : '%s'\n\
        'label' : '%s'\n\
        'textAlignment' : '%s'\n\
        'numberStyle' : '%s'\n\
        'currencyCode' : '%s'\n\
        'timeStyle' : '%s'\n\
        'dateStyle' : '%s'\n\
        'isRelative' : '%s'\n\
        'changeMessage' : '%s'\n\
        'isValid' : '%s'}\n" % (self.key,
        self.value,
        self.label,
        self.textAlignment,
        self.textAlignment,
        self.numberStyle,
        self.currencyCode,
        self.timeStyle,
        self.dateStyle,
        self.isRelative,
        self.changeMessage,)
        
        
            
        
        
        
        
        
        