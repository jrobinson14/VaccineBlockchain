'''
Jonathan Robinson, CS 591
Simple blockchain implementation
Guide used:
https://medium.com/coinmonks/python-tutorial-build-a-blockchain-713c706f6531
'''
import time
import hashlib

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def new_block(self):
        block = { "index" : len(self.chain) + 1,
                  "timestamp" : time.time(),
                  "transactions" : self.pending_transactions}
        self.pending_transactions = []  # reset the pending tansactions to empty list
        self.chain.append(block)  # append new block
        print("BLOCKCHAIN MSG: New Block Posted: ", self.chain[-1])

    def get_last_block(self):
        if len(self.chain) > 0:
            return self.chain[-1]
        else:
            return None

    def new_transaction(self, mpk, ppk, time, h_vc, data):
        transaction = {"Provider" : mpk,
                       "Patient" : ppk,
                       "Timestamp" : time,
                       "h_vc" : h_vc,
                       "data" : data}
        self.pending_transactions.append(transaction)
        return_val = self.get_last_block()
        print("BLOCKCHAIN MSG: New Transaction Posted")
        if return_val:
            return self.get_last_block()["index"] + 1
        else:
            return 0
