#!/usr/bin/env python

# Joride, 2013

import unittest, sys
sys.dont_write_bytecode = True

from ..Pass.FieldDictionary import FieldDictionary

class TestFieldDictionary(unittest.TestCase):
    
    def setUp(self):
        self.fd = FieldDictionary()
    def tearDown(self):
        self.fd = None
        
    #############################################
    # --- numberStyle, currencyCode & value ---
    #############################################
    def testValueAccessors(self):
        # test getter and setter
        myString = "A String"
        self.fd.value = myString
        self.assertEqual(myString, self.fd.value)
            
    def testSettingNumberStyleAndCurrencyCode(self):
        # setting both a numberStyle and a currencyCode should raise an error
        self.fd.numberStyle = 'PKNumberStylePercent'
        self.assertRaises(ValueError, self.fd.currencyCode, 'EUR')

    def testValueAsStringWithNumberStyle(self):
        # setting the value to a string prohibits setting a numberstyle
        myString = "A String"
        self.fd.value = myString
        self.assertRaises(ValueError, self.fd.numberStyle, "PKNumberStylePercent")
        
    def testValueAsStringWileCurrencyCodePresent(self):
        # setting the value to a string prohibits setting a numberstyle
        myString = "A String"
        self.fd.value = myString
        self.assertRaises(ValueError, self.fd.currencyCode, "EUR")

    def testSettingValueAsStringWileNumberStylePresent(self):
        # setting a numberstyle prohibits setting the value to a string
        self.fd.numberStyle = 'PKNumberStylePercent'
        self.assertRaises(ValueError, self.fd.value, "Some String")
        
    def testSettingValueAsStringWileCurrencyCodePresent(self):
        # setting a currencyCode prohibits setting the value to a string
        self.fd.currencyCode = 'EUR'
        self.assertRaises(ValueError, self.fd.value, "Some String")
    
    def testSettingCurrencyCodeToNonString(self):
        # setting the currencycode to a non-allowed value raises an error
        self.assertRaises(ValueError, self.fd.currencyCode, 12)
    
    def testSettingNumberStyleToNonAllowedValue(self):
        # non allowed is a number or a string that is not present in
        # list of allowed values
        self.assertRaises(ValueError, self.fd.numberStyle, 12)
        self.assertRaises(ValueError, self.fd.numberStyle, 'nonAllowedString')
        
        
    #############################################
    # --- dateStyle, timeStyle & value ---
    #############################################
    def testSettingDateStyleToNonAllowedValue(self):
        # setting to non allowed value raises an error
        self.assertRaises(ValueError, self.fd.dateStyle, 'nonAllowedString')
        self.assertRaises(ValueError, self.fd.dateStyle, 12)
        
    def testSettingTimeStyleToNonAllowedValue(self):
        # setting time style to non allowe value raises an error
        self.assertRaises(ValueError, self.fd.timeStyle, 'nonAllowedString')
        self.assertRaises(ValueError, self.fd.timeStyle, 12)
    
    def testSettingOnlyTimeStyle(self):
        # without a key, a FieldDictionary is invalid. We are not testing that now, 
        # so we set it
        self.fd.key = "some key"
        # the value needs to be a string when setting a dateStyle or timeStyle
        self.fd.value = "some string"
        
        # setting only the timeStyle should yield a non-valid FieldDictionary
        self.fd.timeStyle = 'PKDateStyleMedium'
        self.assertFalse(self.fd.isValid)
        
    def testSettingOnlyDateStyle(self):
        # without a key, a FieldDictionary is invalid. We are not testing that now, 
        # so we set it
        self.fd.key = "some key"
        self.fd.value = "some string"
        
        # setting only the dateStyle should yield a non-valid FieldDictionary
        self.fd.dateStyle = 'PKDateStyleMedium'
        self.assertFalse(self.fd.isValid)
                
    def testSettingDateAndTimeStyleWhileValueIsNumeric(self):
        # if the value is numeric, then setting a date or timestyle will raise an error
        self.fd.value = 12
        self.assertRaises(ValueError, self.fd.dateStyle, 'PKDateStyleMedium')
        self.assertRaises(ValueError, self.fd.timeStyle, 'PKDateStyleMedium')
                
    def testSettingValueToStringWhileDateOrTimeStylePresent(self):
        pass
            
        
        
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestFieldDictionary)
unittest.TextTestRunner(verbosity=3).run(suite)
























