from operator import truediv
from bitcoinaddress import Wallet
from tinydb import TinyDB, Query

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

#TODO: provenance, wallet-token representation, distributed ledger, consensus algorithm
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
        g.all_db = db.all()
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
                session['user_id'] = unique_id
                return redirect(url_for('homepage'))
        
        return redirect(url_for('login_method'))
    
    else:
        pass
    
    return render_template("login.html")

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")

@app.route('/wallet')
def main_wallet():
    return render_template("wallet.html")

@app.route('/marketplace')
def marketplace():
    return render_template("marketplace.html")

if __name__ == "__main__":
    app.run(debug=True)