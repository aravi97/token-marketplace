from bitcoinaddress import Wallet
from tinydb import TinyDB, Query

alice_wallet = Wallet()
bob_wallet = Wallet()

db = TinyDB('db.json')
tokens_market = TinyDB('tokens_market.json')

tokens_market.insert({'id': 0, 'name': 'Code Review', 'owner_id': 'alice', 'quantity': 10, 'price': 10})
tokens_market.insert({'id': 1, 'name': 'Dance Tutor', 'owner_id': 'alice', 'quantity': 10, 'price': 50})
tokens_market.insert({'id': 2, 'name': 'Workout partner', 'owner_id':'bob', 'quantity': 10, 'price': 50})
tokens_market.insert({'id': 3, 'name': 'Carrer Counselor', 'owner_id':'bob', 'quantity': 10, 'price': 20})
tokens_market.insert({'id': 4, 'name': 'Carpool Ride - Home', 'owner_id':'bob', 'quantity': 10, 'price': 30})

db.insert({'uname': 'alice', 'pwd': 'alice', 'id': 0, 'address': alice_wallet.address.__dict__['pubkeyc'], \
           'key': alice_wallet.key.__dict__['hex'], 'balance': 100})

db.insert({'uname': 'bob', 'pwd': 'bob', 'id': 1, 'address': bob_wallet.address.__dict__['pubkeyc'], \
           'key': bob_wallet.key.__dict__['hex'], 'balance': 100})

print("Token Databases Populated")
