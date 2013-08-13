#!/usr/bin/env python

# Joride, 2013

import sys
sys.dont_write_bytecode = True

class WebserviceInfo(object):
    """Information used to update passes using the web service. The dictionary contains the following keys:\n\
        'authenticationToken': value is a string, required. The authentication token to use with the web service. The token must be 16 characters or longer.\n\
        'webServiceURL' : value is a string, required. The URL of a web service that conforms to the API described in Passbook Web Service Reference. The web service must use the HTTPS protocol; the leading https:// is included in the value of this key. On devices configured for development, there is UI in Settings to allow HTTP web services."""
    
    def __init__(self, webserviceURL = None, authToken = None):
        
        if type(authToken) != str or len(authToken) < 16:
            errorMessage = "authToken '%s (%i chars)' should be of type string and be 16 characters or longer" % (authToken , len(authToken),)
            raise ValueError(errorMessage)
        
        if type(webserviceURL) != str:
            errorMessage = "webServiceURL '%s (%i chars)' should be of type string" % webserviceURL
            raise ValueError(errorMessage)

        self._webserviceURL = webserviceURL
        self._authToken = authToken
        
    def _getWebserviceURL(self):
        return self._webserviceURL;
    def _getAuthToken(self):
        return self._authToken
        
    webserviceURL = property(_getWebserviceURL, None, doc="""Returns the websericeURL.""")
    authToken = property(_getAuthToken, None, doc="""Retursn the authentication token.""")