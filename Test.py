'''
Jonathan Robinson, CS 591
This is a test file implementing the use case discussed in my paper.
Creates a Patient, Provider, and Verifying Third Party.
Runs locally, no network implementation yet.
Some info on the files created:
1) patient_file.txt - this is the patient's vaccine card created by the provider
2) patient_file_enc.txt.aes - the patient's vaccine care that has been encrypted with AES
3) dataout_patient.txt - the vaccine card recieved and decrypted by the patient
4) verifier_patient_record - the vaccine care recieved from the patient and decrypted by the
    third party verifier
'''
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import Provider
import blockchain
import Patient
import Verifier


'''
Create RSA keys for the patient, provider, and verifier
In a real world implementation this would not be done this way
(parties would create their own keys or handled by certificate authority)
'''
provider_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

patient_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

verifier_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

blockchain = blockchain.Blockchain() # the blockchain used in this test

# create a test record for a patient
patient_test_vc = ["Administration Date: MAY-01-2021 10:00 AM",
                   "Patient ID: 10132",
                   "Patient Name: John Doe",
                   "Patient Address: 10 Example St. NE",
                   "Administered by: Dr. Jill Fakeington"]
# additional info is non-personally identifying info stored with transaction
additional_data = ["Vaccine Type: Pfizer",
                   "Vaccine ID: 1234"]

# create the provider
provider = Provider.Provider(provider_key)
# create the patient
patient = Patient.Patient(patient_key)
# create the third party verifier
verifier = Verifier.Verifier(verifier_key, blockchain)
# generate patient vaccine card
provider.generate_card(patient_test_vc)
# provider posts the transaction to the blockchain
provider.post_transaction(blockchain, patient_key.public_key(), additional_data)
# a new block is created
blockchain.new_block()
# provider sends encrypted vaccine care to the patient
provider.send_patient_info(patient)
# Patient sends encrypted record to the verifier to prove his vaccination
patient.send_records(verifier, verifier.get_pub_key())
# verifier verifies the record is in the blockchain
verifier.verify_record(blockchain)




