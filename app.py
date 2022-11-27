from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.patients import Patients, Patient
from resources.pharmacies import Pharmacies, Pharmacie
from resources.transactions import Transactions, Transaction
from resources.users import User, UserRegister, UserLogin, UserLogout
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLE'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_acess_invalid(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'})

api.add_resource(Patients, '/patients') 
api.add_resource(Patient, '/patient')
api.add_resource(Pharmacies, '/pharmacies')
api.add_resource(Pharmacie, '/pharmacie')
api.add_resource(Transactions, '/transactions')
api.add_resource(Transaction, '/transaction')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:USERNAME>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True, host="0.0.0.0" ,port=5000)