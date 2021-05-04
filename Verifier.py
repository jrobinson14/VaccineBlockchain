'''
Jonathan Robinson, CS591
Guides used for crypto in this code:
https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
https://pypi.org/project/pyAesCrypt/
'''
from os import path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Verifier(object):

    def __init__(self, crypkey, chain):
        self.key = crypkey
        self.blockchain = chain

    def get_pub_key(self):
        return self.key.public_key()

    def get_patient_file(self, enc_msg):
        orig_msg = self.key.decrypt(
            enc_msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode("utf-8")
        print("VERIFIER MSG: PATIENT RECORD DECRYPTED: \n", orig_msg)
        f = open("verifier_patient_record.txt", 'w')
        f.write(orig_msg)
        f.close()

    def verify_hash(self):
        '''
        Get SHA256 hash the patient's vaccine hard
        :return: digest - hash of patient's vaccine vard OR
            0 if file not found
        '''
        file = "verifier_patient_record.txt"
        if path.exists("patient_file.txt"):
            hasher = hashes.Hash(hashes.SHA256())
            print("VERIFIER: hashing file")
            BLOCK_SIZE = 65536
            with open(file, 'rb') as f:
                fb = f.read(BLOCK_SIZE)
                while len(fb) > 0:
                    hasher.update(fb)
                    fb = f.read(BLOCK_SIZE)
            digest = hasher.finalize()
            print("VERIFIER: NEW HASH: ", digest)
            return digest
        else:
            print("VERIFIER ERROR: Patient File Not Found")
            return 0

    def verify_record(self, blockchain):
        '''
        Verify that the hash provided by the patient is in the blockchain
        Prints message confirming success or failure
        :param blockchain: reference to the blockchain
        :return: none
        '''
        hash = self.verify_hash()
        for block in blockchain.chain:
            transactions = block["transactions"]
            # print(transactions[0]["h_vc"])
            if hash == transactions[0]["h_vc"]:
                print("VERIFIER MESSAGE: PATIENT RECORD VERIFIED")
