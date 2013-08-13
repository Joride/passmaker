#!/usr/bin/env python

# Joride, 2013

# prevent cluttering of the working dir
import sys
sys.dont_write_bytecode = True

from Pass import Pass
from PassPackager import PassPackager
from FieldDictionary import FieldDictionary
from BarcodeDictionary import BarcodeDictionary
from Location import Location
from Color import Color
from WebserviceInfo import WebserviceInfo

serialNumber = 'Some Number unique for this pass'
contentDir = '/path/to/passImages/'

# these two value can be found in iTunesConnect / provisioning portal
passTypeIdentifier = 'pass.yourCompanyName.yourPassType'
teamIdentifier = '2R6KT8L4GS' # for example

# create pass
couponPass = Pass()
couponPass.contentDirectory = contentDir

# set required attributes
#couponPass.passID = 'pass.kerrelinc.access'
couponPass.description = 'Your Description'
couponPass.organizationName = 'Your Organization Name'
couponPass.passTypeIdentifier = passTypeIdentifier
couponPass.serialNumber = serialNumber
couponPass.teamIdentifier = teamIdentifier
couponPass.styleKey =  'eventTicket' #'generic'' #'storeCard' #'boardingPass' #'coupon'

# required for styleKey = 'boardingPass', otherwise not allowed
#couponPass.transitType = 'PKTransitTypeBoat'

# optional
couponPass.associatedStoreIdentifiers = [463810843] # retrieved from iTunesConnect ('Apple ID')
aLocation = Location(latitude = 37.332118, longitude = -122.03074) # Apple HQ
aLocation.relevantText = 'Some text'
couponPass.locations = [aLocation]

couponPass.relevantDate = '2013-08-11T17:15+02:00'
barcodeDict = BarcodeDictionary(format = 'PKBarcodeFormatPDF417', message = serialNumber)
barcodeDict.altText = barcodeDict.message
couponPass.barcodeDictionary = barcodeDict

couponPass.backgroundColor = Color(red = 255, green = 100, blue = 0)
couponPass.foregroundColor = Color(red = 255, green = 255, blue = 255)
couponPass.labelColor = Color(red = 255, green = 0, blue = 255)
couponPass.suppressStripShine = True
couponPass.logoText = 'Your company name'
couponPass.webserviceInfoDictionary = WebserviceInfo(webserviceURL = 'https://somewhere.org', authToken = 'abcdefgh12345678')

# headerFields                                    
aHeaderFieldDictionary = FieldDictionary(key = "date", value = '2013-08-11T12:00-05:00')
aHeaderFieldDictionary.label = 'Date'
aHeaderFieldDictionary.dateStyle = 'PKDateStyleShort'
aHeaderFieldDictionary.timeStyle = 'PKDateStyleShort'
couponPass.headerFieldDictionaries = [aHeaderFieldDictionary]

# primaryFields
primaryFieldDictionary1 = FieldDictionary(key = "Venue", value = 'Apple HQ')
primaryFieldDictionary1.label = "Venue"
primaryFieldDictionary2 = FieldDictionary(key = "Reason", value = 'WWDC')
primaryFieldDictionary2.label = "Event:"
couponPass.primaryFieldDictionaries = [primaryFieldDictionary1, primaryFieldDictionary2]

# secondaryFields
secondaryFieldDictionary1 = FieldDictionary(key = 'venuType', value = 'Conference')
secondaryFieldDictionary1.label = 'Style'
secondaryFieldDictionary2 = FieldDictionary(key = 'addres', value = 'Infinite Loop 1')
secondaryFieldDictionary2.label = 'Address'
couponPass.secondaryFieldDictionaries = [secondaryFieldDictionary1, secondaryFieldDictionary2]

# auxiliaryFields
auxiliaryFieldDictionary1 = FieldDictionary(key = 'EntryCode', value = 'AB12')
auxiliaryFieldDictionary1.label = 'entrycode'
auxiliaryFieldDictionary2 = FieldDictionary(key = 'entryGroup', value = '1')
auxiliaryFieldDictionary2.label = 'entrygroup'
couponPass.auxiliaryFieldDictionaries  =[auxiliaryFieldDictionary1, auxiliaryFieldDictionary2]
                                    
# backFields
backFieldDictionary1 = FieldDictionary(key = 'companyName', value = 'Your Company')
backFieldDictionary1.label = 'Company'

backFieldDictionary2 = FieldDictionary(key = 'disclaimer', value = """Don't worry, be happy!""")
backFieldDictionary2.label = 'Disclaimer'
couponPass.backFieldDictionaries  =[backFieldDictionary1, backFieldDictionary2]

# get a distributable package of the pass
passPackager = PassPackager(WWDRCertificatPath = '/path/to/wwdr.pem', passCertificatePath = '/path/to/pass.pem', Pass = couponPass)
passPackager.outputPath = '/path/to/yourPass.pkpass'
passPackager.writePackage()