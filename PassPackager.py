#!/usr/bin/env python

# Joride, 2013

import sys, os
from glob import glob
import json
import M2Crypto as m2
from hashlib import sha1
from zipfile import ZipFile, ZIP_DEFLATED

from Pass import Pass

class PassPackager(object):
    """
    This class creates a manifest file, a signature file and
    a ZIP-archive of a given Pass.
    It will output this to a directory that must be set on the object.
    Example usage:
    passPackager = PassPackager(WWDRCertificatPath = '/past/to/WWDRcertificate', passCertificatePath = '/past/to/passCertPath', Pass = myPass)
    Call writePackage() to write out the package. This class validates the passID and teamID from the pass with the in formation in the certificate.
    """
    
    def __init__(self, WWDRCertificatPath = None, passCertificatePath = None, Pass = None):
        # validate input
        if ((WWDRCertificatPath == None) or (os.path.exists(WWDRCertificatPath) == False)):
            raise ValueError("Argument 'WWDRCertificatPath' must be a path to an existing file")
        if (passCertificatePath == None) or (os.path.exists(passCertificatePath) == False):
            raise ValueError("Argument 'passCertificatePath' must be a path to an existing file")
        if Pass == None:
            raise ValueError("Argument 'Pass' must be an Pass")
            
        # set ivars
        self._WWDRCertificatPath = WWDRCertificatPath
        self._passCertificatePath = passCertificatePath
        self._Pass = Pass
        self._outputPath = None
        
    def _setOutputPath(self, outputPath = None):
        self._outputPath = outputPath
    def _getOutputPath(self):
        return self._outputPath
            
    def writePackage(self):
        # perfom vlaidation on pass-certifcate combination
        teamID = self._Pass._teamIdentifier
        passID = self._Pass.passTypeIdentifier
        
        certFile = open(self._passCertificatePath, 'r')
        certFileContent = certFile.read()
        certFile.close()
        
        teamIDValidated = self._validateTeamID(teamID, certFileContent)
        passIDValidated = self._validatePassID(passID, certFileContent)
        if passIDValidated == False:
            print "passID did not pass validation with certfile"
        if teamIDValidated == False:
            print "teamID did not pass validation with certfile"
        
        if teamIDValidated and passIDValidated:
            directory = self._Pass.contentDirectory
            
            # delete file if it exists
            signaturePath = directory + 'signature'
            if os.path.exists(signaturePath):
                os.unlink(signaturePath)
            
            manifestPath = directory + 'manifest.json'
            # delete file if it exists 
            if os.path.exists(manifestPath):
                os.unlink(manifestPath)
            
            passFilePath = directory + 'pass.json'
            # delete file if it exists 
            if os.path.exists(passFilePath):
                os.unlink(passFilePath)
            
            passFile = open(passFilePath,'wa')
            jsonRepresentation = self._Pass.jsonRepresentation
            passFile.write(self._Pass.jsonRepresentation)
            passFile.close()
                
            self._createManifestFile() 
            self._createSignatureFile()
            self._createZIPArchive()
            
            # delete the files after we're done
            if os.path.exists(signaturePath):
                os.unlink(signaturePath)
            if os.path.exists(manifestPath):
                os.unlink(manifestPath)
            if os.path.exists(passFilePath):
                os.unlink(passFilePath)

            
    def _createManifestFile(self):
        # From Apple Documentation ('Passbook Programming Guide):
        # (http://developer.apple.com/library/ios/documentation/UserExperience/Conceptual/PassKit_PG/Chapters/Creating.html#//apple_ref/doc/uid/TP40012195-CH4-SW55)
        # To create the manifest file, recursively list the files in
        # the package (except the manifest file and signature), calculate
        # the SHA-1 hash of the contents of those files, and store the data
        # in a dictionary. The keys are relative paths to the file from
        # the pass package. The values are the SHA-1 hash (hex encoded)
        # of the data at that path. 
        
        directory = self._Pass.contentDirectory
        manifestPath = directory + 'manifest.json'
                
        listOfFiles = glob(directory + '*')
       
        hashOfFilesDict = {}
        for aFilePath in listOfFiles:
            # open (r for reading, b for indicating binary file)
            aFile = open(aFilePath,'rb')
            sha1Hash = sha1(aFile.read())
            hexEncodedHash = sha1Hash.hexdigest()
            
            lastPathComponent = os.path.basename(os.path.normpath(aFilePath))
            hashOfFilesDict[lastPathComponent] = hexEncodedHash
            
        # turn the dictionary into a JSON-string and write that JSON
        # string out the a file with a specific name
        hashOfFilesJSON = json.dumps(hashOfFilesDict, indent=1)
        open(manifestPath,'wb').write(hashOfFilesJSON)
        
    def _createSignatureFile(self):
        directory = self._Pass.contentDirectory
        signaturePath = directory + 'signature'
        manifestPath = directory + 'manifest.json'
                    
        # From Apple Documentation ('Passbook Programming Guide):
        # (http://developer.apple.com/library/ios/documentation/UserExperience/Conceptual/PassKit_PG/Chapters/Creating.html#//apple_ref/doc/uid/TP40012195-CH4-SW55)
        # To create the signature file, make a PKCS #7 detached signature of
        # the manifest file, using the private key associated with your
        # signing certificate. Include the WWDR intermediate certificate
        # as part of the signature;
        stack = m2.X509.X509_Stack()
        WWDRCertificate = open(self._WWDRCertificatPath,'rb').read()
        stack.push(m2.X509.load_cert_string(WWDRCertificate))

        smime = m2.SMIME.SMIME() 
        passCertificate = self._passCertificatePath
        smime.load_key(passCertificate)
        smime.set_x509_stack(stack)
        
        signatureData = open(manifestPath,'rb').read()
        signatureBuffer = m2.BIO.MemoryBuffer(signatureData)
         
        pkcs7 = smime.sign(signatureBuffer, m2.SMIME.PKCS7_DETACHED | m2.SMIME.PKCS7_BINARY)
         
        signatureBuffer = m2.BIO.MemoryBuffer()
        pkcs7.write_der(signatureBuffer)
        w = open(signaturePath,'wb')
        w.write(signatureBuffer.read_all())
        w.close()

    
    def _createZIPArchive(self):
        # To compress the pass, create a ZIP archive of the contents
        # of the pass package. This ZIP archive is what you distribute to users.
        
        zipFile = ZipFile(self.outputPath,'w', compression=ZIP_DEFLATED)
        directory = self._Pass.contentDirectory
        listOfFiles = glob(directory + '*')
        for aFilePath in listOfFiles:
            lastPathComponent = os.path.basename(os.path.normpath(aFilePath))
            zipFile.write(aFilePath, arcname = lastPathComponent)
        zipFile.close()   
  
    def _getPass(self):
        return self._Pass
    
    # make sure this pem file contains the passID and teamID this pass contains
    def _validateTeamID(self, teamID, pemFileContents):
        teamIDPresent = pemFileContents.find(r'/OU=%s/' % teamID)
        if teamIDPresent < 0:
            message = "TeamID '%s' not found in .pem file '%s'" % (teamID, self._passCertificatePath,)
            raise ValueError(message)
            return False
            
        return True

    def _validatePassID(self, passID, pemFileContents):
        passIDFound = pemFileContents.find(r'/CN=Pass Type ID: %s/' % passID)
        if passIDFound < 0:
            message = "PassID '%s' not found in .pem file '%s' at 'CN=Pass Type ID: '" % (passID, self._passCertificatePath,)
            raise ValueError(message)
            return False
        return True
            
        passIDFound = pemFileContents.find(r'friendlyName: Pass Type ID: %s' % passID)
        if passIDFound < 0:
            message = "PassID '%s' not found in .pem file '%s' at 'friendlyName: Pass Type ID: '" % (passID, self._passCertificatePath,)
            raise ValueError(message)
            return False
        return True

        passIDFound = pemFileContents.find(r'/UID=%s/' % passID)
        if passIDFound < 0:
            message = "PassID '%s' not found in .pem file '%s' at '/UID='" % (passID, self._passCertificatePath,)
            raise ValueError(message)
            return False
        return True
        
    
    Pass = property(_getPass)
    outputPath = property(_getOutputPath, _setOutputPath)