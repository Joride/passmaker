#!/usr/bin/env python
# coding: utf-8

# Joride, 2013

import json
from glob import glob
from FieldDictionary import FieldDictionary
from BarcodeDictionary import BarcodeDictionary
from Location import Location
from Color import Color
from WebserviceInfo import WebserviceInfo

class Pass(object):
    _requiredImageFileNames = (('icon.png',       'icon@2x.png',),
                               ('logo.png',       'logo@2x.png',),
                              )
    _possibleStyleKeyValues =('boardingPass', 'coupon', 'eventTicket', 'generic', 'storeCard',)
    _possibleBarcodeFormats = ('PKBarcodeFormatQR', 'PKBarcodeFormatPDF417', 'PKBarcodeFormatAztec',)    
    _possibleTransitTypes = ('PKTransitTypeAir', 'PKTransitTypeBoat', 'PKTransitTypeBus', 'PKTransitTypeGeneric', 'PKTransitTypeTrain',)
    _possibleDateAndTimeStyles = ('PKDateStyleNone', 'PKDateStyleShort', 'PKDateStyleMedium', 'PKDateStyleLong', 'PKDateStyleFull',)
    _possibleNumberStyles = ('PKNumberStyleDecimal', 'PKNumberStylePercent', 'PKNumberStyleScientific', 'PKNumberStyleSpellOut',)
    
    def __init__(self):
        self._contentDirectory = None
        
        # set all the required, but fixed properties
        self._formatVersion = 1
        
        # init ivars
        self._description = None
        self._organizationName = None
        self._passTypeIdentifier = None
        self._serialNumber = None
        self._teamIdentifier = None
        self._associatedStoreIdentifiers = None
        self._locations = None
        self._relevantDate = None
        self._styleKey = None
        self._barcodeDictionary = None
        self._backgroundColor = None
        self._foregroundColor = None
        self._labelColor = None
        self._suppressStripShine = None
        self._logoText = None
        self._webserviceInfoDictionary = None
        self._transitType = None
        self._headerFieldDictionaries = None
        self._primaryFieldDictionaries = None
        self._secondaryFieldDictionaries = None
        self._auxiliaryFieldDictionaries = None
        self._backFieldDictionaries = None
        
        # this dictionary contains as keys the value of the key 'key' in
        # all fieldDictionaries. Used to make sure they are all unique.
        self._fieldDictionaryKeyValues = {}
        
    def _getFormatVersion(self):
        return self._formatVersion;
    
    def _getContentDirectory(self):
        return self._contentDirectory
        
    def _setContentDirectory(self, contentDirectory = None):
        # when setting the contentDirectory, we need to make sure all the neccessary files are here
        listOfFiles = glob(contentDirectory + '*')
        
        # the direcotry needs to contain all neccessay files before it can be srt
        for aTupleOfImageNames in Pass._requiredImageFileNames:
            imageInDirectory = False
            try:
                index = listOfFiles.index(contentDirectory+ aTupleOfImageNames[0])
                imageInDirectory = True
                break
            except ValueError: 
                try:
                    index = listOfFiles.index(contentDirectory+ aTupleOfImageNames[0])
                    imageInDirectory = True
                    break
                except ValueError:
                    message = ("Image needed for pass not found: %s or %s (note case)" % aTupleOfImageNames)
                    raise ValueError(message)
        
        self._contentDirectory = contentDirectory
    
    def _getJSONRepresentation(self, prettyPrinted = False): 
        # make sure all info to create a JSON is here
        if self.formatVersion == None:
            raise ValueError("formatVersion not set, cannot create JSONRepresentation")
        if self.description == None:
            raise ValueError("description not set, cannot create JSONRepresentation")
        if self.organizationName == None:
            raise ValueError("organizationName not set, cannot create JSONRepresentation")
        if self.passTypeIdentifier == None:
            raise ValueError("passTypeIdentifier not set, cannot create JSONRepresentation")
        if self.serialNumber == None:
            raise ValueError("serialNumber not set, cannot create JSONRepresentation")
        if self.teamIdentifier == None:
            raise ValueError("teamIdentifier not set, cannot create JSONRepresentation")
        if self.associatedStoreIdentifiers == None:
            raise ValueError("associatedStoreIdentifiers not set, cannot create JSONRepresentation")
        if self.styleKey == None:
            raise ValueError("styleKey not set, cannot create JSONRepresentation")

        # all we need is present, create the json
        passDict = {"formatVersion" : self.formatVersion,
                    "passTypeIdentifier" : self.passTypeIdentifier,
                    "serialNumber" : self.serialNumber,
                    "teamIdentifier" : self.teamIdentifier,
                    "webServiceURL" : "https://example.com/passes/",
                    "authenticationToken" : "vxwxd7J8AlNNFPS8k0a0FfUFtq0ewzFdc",
                    "organizationName" : self.organizationName,
                    "description" : self.description,
                    self.styleKey : {
                    }
                } 
                     
        # add optional parameters if present
        if self.webserviceInfoDictionary != None:
            passDict['webServiceURL'] = self.webserviceInfoDictionary.webserviceURL
            passDict['authenticationToken'] = self.webserviceInfoDictionary.authToken
        if self.barcodeDictionary != None:
            passDict['barcode'] = self.barcodeDictionary.dictionaryRepresentation
        if self.associatedStoreIdentifiers != None:
            passDict['associatedStoreIdentifiers'] = self.associatedStoreIdentifiers
        if self.relevantDate != None:
            passDict['relevantDate'] = self.relevantDate
        if self.backgroundColor != None:
            passDict['backgroundColor'] = self.backgroundColor.stringRepresentation
        if self.foregroundColor != None:
            passDict['foregroundColor'] = self.foregroundColor.stringRepresentation
        if self._labelColor != None:
            passDict['labelColor'] = self._labelColor.stringRepresentation      
        if self.suppressStripShine != None:
            passDict['suppressStripShine'] = self.suppressStripShine
        if self.logoText != None:
            passDict['logoText'] = self.logoText
        if self.locations != None:
            passDict['locations'] = [aLocation.dictionaryRepresentation for aLocation in self.locations]
        
        if self.styleKey == 'boardingPass':
            # when we are of type boarding pass, we MUST have a transitType
            if self.transitType == None:
                raise ValueError("styleKey is 'boardingPass' but transitType is not set.")
            else:
                # add transitType to the self.styleKey-dict
                passDict[self.styleKey]['transitType'] = self.transitType
        else:
            # when we are not of type boarding pass, we CANNOT have a transitType
            if self.transitType != None:
                raise ValueError("styleKey is not 'boardingPass' but transitType has been set.")
                
        if self.headerFieldDictionaries != None:            
            passDict[self.styleKey]['headerFields'] = [afieldDict.dictionaryRepresentation for afieldDict in self.headerFieldDictionaries]
        if self.primaryFieldDictionaries != None:
            passDict[self.styleKey]['primaryFields'] = [afieldDict.dictionaryRepresentation for afieldDict in self.primaryFieldDictionaries]
        if self.secondaryFieldDictionaries != None:
            passDict[self.styleKey]['secondaryFields'] = [afieldDict.dictionaryRepresentation for afieldDict in self.secondaryFieldDictionaries]
        if self.auxiliaryFieldDictionaries != None:
            passDict[self.styleKey]['auxiliaryFields'] = [afieldDict.dictionaryRepresentation for afieldDict in self.auxiliaryFieldDictionaries]
        if self.backFieldDictionaries != None:
            passDict[self.styleKey]['backFields'] = [afieldDict.dictionaryRepresentation for afieldDict in self.backFieldDictionaries]
        
        returnValue = None
        if prettyPrinted == True:
            returnValue = json.dumps(passDict, sort_keys=True, indent=4)
        else:
            returnValue = json.dumps(passDict)
        return returnValue


    def _setDescription(self, description):
        self._description = description
    def _getDescription(self):
        return  self._description
    def _setOrganizationName(self, organizationName):
        self._organizationName = organizationName
    def _getOrganizationName(self):
        return  self._organizationName
    def _getPassTypeIdentifier(self):
        return self._passTypeIdentifier
    def _setPassTypeIdentifier(self, passTypeIdentifier):
        self._passTypeIdentifier = passTypeIdentifier
    def _getSerialNumber(self):
        return self._serialNumber
    def _setSerialNumber(self, serialNumber):
        self._serialNumber = serialNumber
    def _getTeamIdentifier(self):
        return self._teamIdentifier
    def _setTeamIdentifier(self, teamIdentifier):
        self._teamIdentifier = teamIdentifier
    def _getAssociatedStoreIdentifiers(self):
        return self._associatedStoreIdentifiers
    def _setAssociatedStoreIdentifiers(self, associatedStoreIdentifiers):
        self._associatedStoreIdentifiers = associatedStoreIdentifiers
    def _getLocations(self):
        return self._locations
    def _setLocations(self, locations): 
        self._locations = locations
    def _setRelevantDate(self, relevantDate):
        self._relevantDate = relevantDate
    def _getRelevantDate(self):
        return self._relevantDate
        
    def _getStyleKey(self):
        return self._styleKey
    def _setStyleKey(self, styleKey):
        try:
            index = Pass._possibleStyleKeyValues.index(styleKey)
        except ValueError: 
            allowedValues = ''
            for anAllowedValue in Pass._possibleStyleKeyValues:
                allowedValues += ("'"+anAllowedValue+"'" + ' ')
            message = ("Argument '%s', not allowed. Allowed values: %s" % (styleKey ,allowedValues))
            raise ValueError(message)
            
        self._styleKey = styleKey
    def _setBarcodeDictionary(self, barcodeDictionary):
        if barcodeDictionary.isValid != True:
            raise ValueError("barcodeDictionary '%s' is not valid")
        self._barcodeDictionary = barcodeDictionary
        
    def _getBarcodeDictionary(self):
        return self._barcodeDictionary
    def _getBackgroundColor(self):
        return self._backgroundColor
    def _setBackgroundColor(self, backgroundColor):
        self._backgroundColor = backgroundColor
    def _getForegroundColor(self):
        return self._foregroundColor
    def _setForegroundColor(self, foregroundColor):
        self._foregroundColor = foregroundColor
    def _getLabelColor(self):
        return self._labelColor
    def _setLabelColor(self, labelColor):
        self._labelColor = labelColor
    def _setSuppressStripShine(self, suppressStripShine):
        self._suppressStripShine = suppressStripShine
    def _getSuppressStripShine(self):
        return self._suppressStripShine
    def _setLogoText(self, logoText):
        self._logoText = logoText
    def _getLogoText(self):
        return self._logoText
    def _getWebserviceInfoDictionary(self):
        return self._webserviceInfoDictionary
    def _setWebserviceInfoDictionary(self, webserviceInfoDictionary):        
        self._webserviceInfoDictionary = webserviceInfoDictionary
        
    def _getTransitType(self):
        return self._transitType
    def _setTransitType(self, transitType):
        try:
            index = Pass._possibleTransitTypes.index(transitType)
        except ValueError: 
            allowedValues = ''
            for anAllowedValue in Pass._possibleTransitTypes:
                allowedValues += ("'"+anAllowedValue+"'" + ' ')
            message = ("Argument '%s', not allowed. Allowed values: %s" % (transitType ,allowedValues))
            raise ValueError(message)
            
        self._transitType = transitType
        
    def _setFieldDictionariesForKey(self, fieldDictionaries, key):
        for aFieldDictionary in fieldDictionaries:
            if aFieldDictionary.isValid != True:
                raise ValueError("At least one fieldDictionary for key '%s' is invalid: %s" % (key, aFieldDictionary))
                
            # add the values for the given to the array (ivar)
            valuePresent = False
            valueForKeyKey = aFieldDictionary.key
            try: 
                valuePresent = self._fieldDictionaryKeyValues[valueForKeyKey]
            except KeyError:
                # good, the this value for the key 'key' was not yet present, we add it now
                self._fieldDictionaryKeyValues[valueForKeyKey] = True
            if valuePresent:
                errorMessage = "Value ('%s') for key '%s' in %s has already been used as value for a key\
                 'key' in some other fieldDictionary. Those values must be unique within the scope of the pass." %(valueForKeyKey, key, aFieldDictionary)
                raise ValueError(errorMessage)
            
        if key == 'headerField':
            self._headerFieldDictionaries = fieldDictionaries
        elif key == 'primaryFields':
            self._primaryFieldDictionaries = fieldDictionaries
        elif key == 'secondaryFields':
            self._secondaryFieldDictionaries = fieldDictionaries
        elif key == 'auxiliaryFields':
            self._auxiliaryFieldDictionaries = fieldDictionaries
        elif key == 'backFields':
            self._backFieldDictionaries = fieldDictionaries
        else:
            raise ValueError("Internal programming error: setting fieldDictionaries for unknwon key '%s'." % key)
        
    def _setHeaderFieldDictionaries(self, headerFieldDictionaries):
        self._setFieldDictionariesForKey(headerFieldDictionaries, 'headerField')
    def _getHeaderFieldDictionaries(self):
        return self._headerFieldDictionaries
        
    def _getPrimaryFieldDictionaries(self):
        return self._primaryFieldDictionaries
    def _setPrimaryFieldDictionaries(self, primaryFieldDictionairies):
        self._setFieldDictionariesForKey(primaryFieldDictionairies, 'primaryFields')
        
    def _getSecondaryFieldDictionaries(self):
        return self._secondaryFieldDictionaries
    def _setSecondaryFieldDictionaries(self, secondaryFieldDictionairies):
        self._setFieldDictionariesForKey(secondaryFieldDictionairies, 'secondaryFields')
        
    def _getAuxiliaryFieldDictionaries(self):
        return self._auxiliaryFieldDictionaries
    def _setAuxiliaryFieldDictionaries(self, auxiliaryFieldDictionairies):
        self._setFieldDictionariesForKey(auxiliaryFieldDictionairies, 'auxiliaryFields') 
               
    def _getBackFieldDictionaries(self):
        return self._backFieldDictionaries
    def _setBackFieldDictionaries(self, backFieldDictionairies):
        self._setFieldDictionariesForKey(backFieldDictionairies, 'backFields')
             
        
    # properties
    jsonRepresentation = property(_getJSONRepresentation, None, doc = """ Returns the pass as a JSON string.""")
    contentDirectory = property(_getContentDirectory, _setContentDirectory, doc="""The directory that contains the imgages for this pass.""")  
    
    # pass contents
     #######################
    # -- Top Level Keys --
    #######################
    # The top level of the pass.json file is a dictionary. The following sections
    # list the required and optional keys used in this dictionary. For each key 
    # whose value is a dictionary or an array of dictionaries, there is also a
    # section in "Lower-Level Keys” that lists the keys for that dictionary.
    
    # Standard Keys
    # =====================
    # - Information that is required for all passes.
    description = property(_getDescription, _setDescription, doc="""String, Required.Brief description of the pass, used by the iOS accessibility technologies. Don't try to include all of the data on the pass in its description, just include enough detail to distinguish passes of the same type.""")
    
    formatVersion = property(_getFormatVersion, doc="""Integer, required, readonly. Version of the file format. The value must be 1, so there is no setter.""")
    
    organizationName = property(_getOrganizationName, _setOrganizationName, doc="""String, reqquired. Display name of the organization that originated and signed the pass.""")
    
    passTypeIdentifier = property(_getPassTypeIdentifier, _setPassTypeIdentifier, doc="""String, requited. Pass type identifier, as issued by Apple. The value must correspond with your signing certificate.""")
    
    serialNumber = property(_getSerialNumber, _setSerialNumber, doc="""String, required. Serial number that uniquely identifies the pass. No two passes with the same pass type identifier may have the same serial number.""") # string
    
    teamIdentifier = property(_getTeamIdentifier, _setTeamIdentifier, doc="""String. Required. Team identifier of the organization that originated and signed the pass, as issued by Apple.""")
    
    # Associated App Keys
    # =====================
    # - Information about an app that is associated with a pass.
    
    associatedStoreIdentifiers = property(_getAssociatedStoreIdentifiers, _setAssociatedStoreIdentifiers, doc="""Array of numbers. Optional. A list of iTunes Store item identifiers (also known as Adam IDs) for the associated apps. Only one item in the list is used: the first item identifier for an app compatible with the current device. If the app is not installed, the link opens the App Store and shows the app. If the app is already installed, the link launches the app.""")
    
    # Relevance Keys
    # =====================
    # - Information about where and when a pass is relevant.
    locations = property(_getLocations, _setLocations, doc="""Array of Location objects. Optional. Locations where the pass is relevant. For example, the location of your store.""")
        
    relevantDate = property(_getRelevantDate, _setRelevantDate, doc="""String, optional. W3C date. Date and time when the pass becomes relevant. For example, the start time of a movie. The value must be a complete date with hours and minutes, and may optionally include seconds.\nFrom 'http://www.w3.org/TR/NOTE-datetime':\
    Year:
      YYYY (eg 1997)
   Year and month:
      YYYY-MM (eg 1997-07)
   Complete date:
      YYYY-MM-DD (eg 1997-07-16)
   Complete date plus hours and minutes:
      YYYY-MM-DDThh:mmTZD (eg 1997-07-16T19:20+01:00)
   Complete date plus hours, minutes and seconds:
      YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)
   Complete date plus hours, minutes, seconds and a decimal fraction of a second
      YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)
    
    where:
     YYYY = four-digit year
     MM   = two-digit month (01=January, etc.)
     DD   = two-digit day of month (01 through 31)
     hh   = two digits of hour (00 through 23) (am/pm NOT allowed)
     mm   = two digits of minute (00 through 59)
     ss   = two digits of second (00 through 59)
     s    = one or more digits representing a decimal fraction of a second
     TZD  = time zone designator (Z or +hh:mm or -hh:mm)""")
    
    styleKey = property(_getStyleKey, _setStyleKey, doc="""String, required. Required possible values: 'boardingPass', 'coupon', 'eventTicket', 'generic', 'storeCard' """)
    
    barcodeDictionary = property(_getBarcodeDictionary, _setBarcodeDictionary, doc="""An instance of a BarcodeDictionary. Optional""") 
    
    backgroundColor = property(_getBackgroundColor, _setBackgroundColor, doc="""A Color object, optional""")
    
    foregroundColor = property(_getForegroundColor, _setForegroundColor, doc="""String, optional. Foreground color of the pass, specified as an CSS-style RGB triple. For example, 'rgb(23, 187, 82)'.""")
    
    labelColor = property(_getLabelColor, _setLabelColor, doc="""String, optional. Label color of the pass, specified as an CSS-style RGB triple. For example, 'rgb(23, 187, 82)'.""")
    suppressStripShine = property(_getSuppressStripShine, _setSuppressStripShine, doc="""Boolean, optional.If true, the strip image is displayed without a shine effect. The default value is false.""")
    
    logoText = property(_getLogoText, _setLogoText, doc="""Localizable string, optional. Text displayed next to the logo on the pass""")
    
    webserviceInfoDictionary = property(_getWebserviceInfoDictionary, _setWebserviceInfoDictionary, doc="""WebsericeInfo object. Optional.""")
    
    transitType = property(_getTransitType, _setTransitType, doc="""String, required for boarding passes; otherwise not allowed. Type of transit. Must be one of the following values: 'PKTransitTypeAir', 'PKTransitTypeBoat', 'PKTransitTypeBus', 'PKTransitTypeGeneric', 'PKTransitTypeTrain'.""")
    
    headerFieldDictionaries = property(_getHeaderFieldDictionaries, _setHeaderFieldDictionaries, doc="""Array of HeaderFieldDictionary objects. Optional. These all need to return 'True' for their property 'isValid.""")
    
    primaryFieldDictionaries = property(_getPrimaryFieldDictionaries, _setPrimaryFieldDictionaries, doc="""Array of HeaderFieldDictionary objects. Optional. These all need to return 'True' for their property 'isValid.""")
    
    secondaryFieldDictionaries = property(_getSecondaryFieldDictionaries, _setSecondaryFieldDictionaries, doc="""Array of HeaderFieldDictionary objects. Optional. These all need to return 'True' for their property 'isValid.""")
                
    auxiliaryFieldDictionaries = property(_getAuxiliaryFieldDictionaries, _setAuxiliaryFieldDictionaries, doc="""Array of HeaderFieldDictionary objects. Optional. These all need to return 'True' for their property 'isValid.""")

    backFieldDictionaries = property(_getBackFieldDictionaries, _setBackFieldDictionaries, doc="""Array of HeaderFieldDictionary objects. Optional. These all need to return 'True' for their property 'isValid.""")

    
    
    
    
    
    
            

    
    
    
    
    
    
    
    
    
    