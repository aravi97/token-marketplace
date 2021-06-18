from bitcoinaddress import Wallet
from operator import add, sub
from tinydb import TinyDB, Query
import hashlib

block_list = []
tx_temp_list = []

db = TinyDB('db.json')

class User:
    uname = str()
    pwd = str()
    id = int()
    wallet = Wallet()
    balance = int()

class Transaction:
    sender = str()
    receiver = str()
    asset_type = str()
    amount = int()

class TxBlock:
    block_size = 6

    def __init__(self, previous_block_hash, tx_list):
        self.previous_block_hash = previous_block_hash
        self.tx_list = tx_list

        for tx in tx_list:
            db_query = Query()
            return_obj = db.search(tx.sender == db_query.uname)
            sender_address = return_obj[0].get('address')
            return_obj = db.search(tx.receiver == db_query.uname)
            receiver_address = return_obj[0].get('address')

            self.signature = str(sender_address) + str(receiver_address)

        self.signature += previous_block_hash

        #self.block_data = "-".join(tx_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.signature.encode()).hexdigest()

'''
def modify_balance(target, amount, operation):
    user_entry = Query()
    net_value = operation(target.balance, amount)
    
    db.update({'balance': net_value}, user_entry.id == target.id)


def increment_balance(target, amount):
    user_entry = Query()
    db.search(user_entry.id == target.id)


def check_tx(tx_request):
    if(tx_request.sender.balance > tx_request.amount):
        return False

    modify_balance(tx_request.sender, tx_request.amount, sub)
    modify_balance(tx_request.receiver, tx_request.amount, add)
    return True
'''

def create_trasaction(tx_obj):
    tx_temp_list.append(tx_obj)
    
    if(len(tx_temp_list) == TxBlock.block_size):
        if(len(block_list) == 0):
            new_block = TxBlock("Genesis Block", tx_temp_list)
        else:
            new_block = TxBlock(block_list[-1].block_hash, tx_temp_list)
        
        block_list.append(new_block)
        tx_temp_list.clear()
    
    print("\n\n")
    print("*** Printing Ledger ***")
    print(block_list)
    print("\n\n")


