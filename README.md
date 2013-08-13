passmaker
=========

A Python implementation to create passes for iOS' PassBook

Additional requirements to make this work:
- two .pem files: one created from the wwdc.cert file and one created from a cert file that was obtained through the Apple Developer portal.
- optional images (can be found in the Apple PassBook companion files)

These classes were created to:
1. ease the packaging of a pass
2. reduce errors when creating the pass.json

Goal one is achieved by creating a class that handles the creation of the manifest.json and signature files, and zipping it up.
Goald two is achieved by implementing some basic validations based on the documentation supplied by Apple. N.B. a pass that does not validation in these classes will certainly not pass valiation in iOS' passbook. If a pass passes validation in these classes, it is not guaranteed to be accespted by iOS' passbook.

About the author:
I am primarily an iOS developer. I only recently picked up Python, and am happy to hear on how this qualifies as a Python-project.
