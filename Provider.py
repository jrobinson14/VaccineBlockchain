'''
Jonathan Robinson, CS591
Guides used for crypto in this code:
https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
https://pypi.org/project/pyAesCrypt/
https://www.cryptoexamples.com/python_cryptography_string_signature_rsa.html
'''
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from Crypto.Cipher import AES
import blockchain
import time
import hashlib
from os import path
import pyAesCrypt

class Provider(object):
    def __init__(self, crypkey):
        self.key = crypkey

    def generate_card(self, patient_card):
        '''
        Create a local file with patient info
        :param patient_card: patient info used to create vaccine card
        :return: none
        '''
        patient_file = open("patient_file.txt", "w")
        for line in patient_card:
            patient_file.write(line)
        patient_file.close()

    def hash_file(self):
        '''
        Get SHA256 hash the patient's vaccine hard
        :return: digest - hash of patient's vaccine vard OR
            0 if file not found
        '''
        file = "patient_file.txt"
        if path.exists("patient_file.txt"):
            hasher = hashes.Hash(hashes.SHA256())
            # print("hashing file")
            BLOCK_SIZE = 65536
            with open(file, 'rb') as f:
                fb = f.read(BLOCK_SIZE)
                while len(fb) > 0:
                    hasher.update(fb)
                    fb = f.read(BLOCK_SIZE)
            digest = hasher.finalize()
            print("PROVDER MSG: NEW HASH OF PATIENT FILE CREATED: \n", digest)
            return digest
        else:
            print("ERROR: Patient File Not Found")
            return 0

    def post_transaction(self, blockchain, ppk, data):
        h_vc = self.hash_file()
        signed = self.key.sign(h_vc,
                               padding.PSS(
                                   mgf=padding.MGF1(hashes.SHA256()),
                                   salt_length=padding.PSS.MAX_LENGTH
                               ),
                               utils.Prehashed(hashes.SHA256())
                               )

        blockchain.new_transaction(self.key.public_key(),
                                   ppk,
                                   time.time(),
                                   h_vc,
                                   data)
    def send_patient_info(self, patient):
        '''
        Send encrypted vaccine card and encryption key to patient
        :return:
        '''
        # encrypt the patient's vaccine card using AES
        bufferSize = 64 * 1024
        password = "example01"
        pyAesCrypt.encryptFile("patient_file.txt", "patient_file_enc.txt.aes", password, bufferSize)

        #encrypt the AES key using patient public key
        pub_key = patient.get_pub_key()
        encryptedAES = pub_key.encrypt(
            b'example01',
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
            )
        )
        print("PROVIDER MSG: Encrypted AES Key Created: ", encryptedAES)
        patient.get_records(encryptedAES)