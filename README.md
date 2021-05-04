# VaccineBlockchain
Submission for UNM CS 591 Final Project

Created by Jonathan Robinson for UNM CS 591

The code in this repository implements the general framework and use case described in my paper "Blockchain Technology for Medical Records Sharing andCOVID-19 Vaccine Verification". 

The code uses several guides to implement a blockchain and RSA and AES encryption. These guides are: 

(Crypto guides)

https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

https://pypi.org/project/pyAesCrypt/

https://www.cryptoexamples.com/python_cryptography_string_signature_rsa.html

(Blockchain guides)

https://medium.com/coinmonks/python-tutorial-build-a-blockchain-713c706f6531

# Files:

Test.py - main code for the demo, run this. This runs through the use case described in the paper
Patient.py - implements class for a Patient node. Receives record from a Provider node and can share the record with a Third Party Verifier
Verifier.py - A Third Party verifier that checks to see if a patient's record is valid
Blockchain.py - basic implementation of a blockchain

During the test, several txt files are generated. Please see a detailed description of each in the comments of Test.py

# Dependencies:

Python 3.8

Libraires used - 
cryptography
pyAesCrypt

# Running the code:

Ensure all files mentioned above are in the same directory

You can run the test file using the command python3 test.py
