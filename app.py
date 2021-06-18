from operator import truediv
from bitcoinaddress import Wallet
from tinydb import TinyDB, Query
from chain_logic import Transaction, TxBlock, create_trasaction

from flask import (
    Flask, 
    render_template, 
    url_for, 
    request, 
    session,
    g
)

from werkzeug.utils import redirect

db = TinyDB('db.json')
tokens_market = TinyDB('tokens_market.json')

#TODO: provenance, wallet-token representation, distributed ledger, consensus algorithm, earning vpoints
'''
alice_wallet = Wallet()
bob_wallet = Wallet()

tokens_market.insert({'id': 0, 'name': 'Code Review', 'owner_id': 0, 'quantity': 10, 'price': 20})
tokens_market.insert({'id': 0, 'name': 'Dance Tutor', 'owner_id': 0, 'quantity': 10, 'price': 20})
tokens_market.insert({'id': 0, 'name': 'Workout partner', 'owner_id':1, 'quantity': 10, 'price': 20})
tokens_market.insert({'id': 0, 'name': 'Carrer Counselor', 'owner_id':1, 'quantity': 10, 'price': 20})


db.insert({'uname': 'alice', 'pwd': 'alice', 'id': 0, 'address': alice_wallet.address.__dict__['pubkeyc'], \
           'key': alice_wallet.key.__dict__['hex'], 'balance': 100})

db.insert({'uname': 'bob', 'pwd': 'bob', 'id': 1, 'address': bob_wallet.address.__dict__['pubkeyc'], \
           'key': bob_wallet.key.__dict__['hex'], 'balance': 100})
'''

global_user_name = ""

app = Flask(__name__)
app.secret_key = "itsasecret"

@app.before_request
def before_request():
    if 'user_id' in session:
        user_entry = Query()
        return_obj = db.search(user_entry.id == session['user_id'])

        g.user = return_obj[0]
        g.all_tokens = tokens_market.all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login_method():
    if(request.method == 'POST'):
        session.pop('user_id', None)
        
        Username = request.form['Username']
        Password = request.form['Password']

        #Query Database
        user_entry = Query()
        return_obj = db.search(user_entry.uname == Username.lower())
        
        if(len(return_obj) != 0):
            password = return_obj[0].get('pwd')
            unique_id = return_obj[0].get('id')
        
            if(password == Password):
                session['user_id'] = int(unique_id)
                return redirect(url_for('homepage'))

        return redirect(url_for('fail_login'))
    
    return render_template("login.html")

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")

@app.route('/wallet')
def main_wallet():
    return render_template("wallet.html")

@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    if(request.method == 'POST'):
        token_id = (request.form.get("token"))
        print(token_id)
        token_query = Query()
        
        return_obj = tokens_market.search(token_query.id == int(token_id))
        
        if(len(return_obj) != 0):
            token_price = int(return_obj[0].get('price'))
            owner = str(return_obj[0].get('owner_id'))
            asset_type = return_obj[0].get('name')

            if(g.user["balance"] < int(token_price)):
                return redirect("fail_buy")
            
            if(g.user["uname"] != owner):
                db_update = Query()
                return_obj = db.search(db_update.uname == owner)
                balance = int(return_obj[0].get('balance'))
                db.update({'balance': int(g.user["balance"] - int(token_price))}, db_update.id == int(g.user["id"]))
                db.update({'balance': int(balance + int(token_price))}, db_update.uname == owner)

            ### Update Blockchain ###
            transaction_record = Transaction()
            transaction_record.sender = str(g.user["uname"])
            transaction_record.receiver = str(owner)
            transaction_record.asset_type = str(asset_type)
            transaction_record.amount = int(token_price)
            create_trasaction(transaction_record)

            return redirect("success_buy")
    
    return render_template("marketplace.html")

@app.route('/create_token', methods=['GET', 'POST'])
def create_token():
    if(request.method == 'POST'):
        
        token_name = request.form['token_name']
        token_price = int(request.form['price'])

        #Query Database
        user_entry = Query()
        return_obj = db.search(user_entry.id == session['user_id'])
        token_creator = return_obj[0].get('uname')
        token_id = int(len(tokens_market.all()) + 1)

        tokens_market.insert({'id': int(token_id), 'name': str(token_name), 'owner_id': str(token_creator), 'quantity': 10, 'price': int(token_price)})
        return redirect("success_token")
    
    return render_template("create_token.html")

@app.route('/fail_buy')
def fail_buy():
    return render_template("fail_buy.html")

@app.route('/success_buy')
def success_buy():
    return render_template("success_buy.html")

@app.route('/fail_login')
def fail_login():
    return render_template("fail_login.html")

@app.route('/success_token')
def success_token():
    return render_template("success_token.html")

if __name__ == "__main__":
    app.run(debug=True)