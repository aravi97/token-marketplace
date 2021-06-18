from bitcoinaddress import Wallet
from operator import add, sub
from tinydb import TinyDB, Query
import hashlib

alice_wallet = Wallet()
bob_wallet = Wallet()

db = TinyDB('db.json')

db.insert({'uname': 'alice', 'pwd': 'alice', id: 0, 'address': alice_wallet.address.__dict__['pubkeyc'], \
           'key': alice_wallet.key.__dict__['hex'], 'balance': 100})

db.insert({'uname': 'bob', 'pwd': 'bob', id: 1, 'address': bob_wallet.address.__dict__['pubkeyc'], \
           'key': bob_wallet.key.__dict__['hex'], 'balance': 100})

class User:
    uname = str()
    pwd = str()
    id = int()
    wallet = Wallet()
    balance = int()

class Transaction:
    sender = User()
    receiver = User()
    assetType = str()
    amount = int()

class TxBlock:
    block_size = 6

    def __init__(self, previous_block_hash, tx_list):
        self.previous_block_hash = previous_block_hash
        self.tx_list = tx_list
        
        for tx in tx_list:
            self.signature = str(tx.sender.address) + str(tx.receiver.address)
        self.signature += previous_block_hash

        #self.block_data = "-".join(tx_list) + "-" + previous_block_hash
        self.block_hash = hashlib.sha256(self.signature.encode()).hexdigest()

def modify_balance(target, amount, operation):
    user_entry = Query()
    net_value = operation(target.balance, amount)
    
    db.update({'balance': net_value}, user_entry.id == target.id)

'''
def increment_balance(target, amount):
    user_entry = Query()
    db.search(user_entry.id == target.id)
'''

def check_tx(tx_request):
    if(tx_request.sender.balance > tx_request.amount):
        return False

    modify_balance(tx_request.sender, tx_request.amount, sub)
    modify_balance(tx_request.receiver, tx_request.amount, add)
    return True

t1 = "Bob sends 5 coins to Alice"
t2 = "Alice sends 2 coins to Bob"

main_net_chain = []
initial_block = TxBlock("Genesis String", [t1, t2])
main_net_chain.append(initial_block)

print(initial_block.block_data)
print(initial_block.block_hash)

