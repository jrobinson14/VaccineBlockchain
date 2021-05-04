'''
Jonathan Robinson, CS591
Guides used for crypto in this code:
https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
https://pypi.org/project/pyAesCrypt/
'''
import pyAesCrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Patient(object):

    def __init__(self, crypkey):
        self.key = crypkey
        # pubkey = self.key.public_key()

    def get_pub_key(self):
        return self.key.public_key()

    def get_records(self, aes_key):
        bufferSize = 64 * 1024
        # decrypt aes key using patient private key
        orig_msg = self.key.decrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
        )
        orig_msg = orig_msg.decode("utf-8")
        print("PATIENT MSG: Patient AES Key Retieved Successfully: ", orig_msg)

        # use AES key to decrypt original msg
        pyAesCrypt.decryptFile("patient_file_enc.txt.aes",
                               "dataout_patient.txt", (orig_msg), bufferSize)
        print("PATIENT MSG: DECRYPTED MESSAGE SUCCESSFULLY, STORED AS "
              "dataout_patient.txt")

    def send_records(self, verifier, vpk):
        '''
        Send records to third party to be verified
        :return:
        '''

        # encrypt record using verifier public key
        f = open("dataout_patient.txt", 'rb')
        vc = f.read()
        f.close()
        enc_vc = vpk.encrypt(
            bytes(vc),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None)
        )
        print("PATIENT MSG: VACCINE CARD FOR VERIFIER ENCRYPTIOIN COMPLETED")
        verifier.get_patient_file(enc_vc)
