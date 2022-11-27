from flask_restful import Resource, reqparse
from datetime import datetime 
from flask_jwt_extended import jwt_required
from models.transactions import TransactionsModel
from models.pharmcies import PharmacieModel
from models.patients import PatientsModel 

class Transactions(Resource):
    @jwt_required()
    def get(self):
        '''Retorna todas as transações do sistema'''
        return {'transactions': [transaction.json() for transaction in TransactionsModel.query.all()]}

class Transaction(Resource):
    
    args = reqparse.RequestParser()
    args.add_argument('PATIENT_UUID', type=str, required=True, help="The field 'PATIENT' cannot be left blank")
    args.add_argument('PHARMACY_UUID', type=str, required=True, help="The field 'PHARMACY' cannot be left blank")
    args.add_argument('AMOUNT', type=float, required=True, help="The field 'Date of Birth' cannot be left blank")
    args.add_argument('TIMESTAMP', required=True, help="The field 'TIMESTAMP' cannot be left blank")

    @jwt_required()
    def post(self):
        '''Adiciona uma nova transação no sistema'''
        data = Transaction.args.parse_args()

        pharmacie_exist = PharmacieModel.find_by_id(data['PHARMACY_UUID'])

        if not pharmacie_exist:
            return {'message': 'PHARMACY_UUID not found'}, 400
        
        patient_exist = PatientsModel.find_by_id(data['PATIENT_UUID'])

        if not patient_exist:
            return {'message': 'PATIENT_UUID not found'}, 400

        data['TIMESTAMP'] = datetime.strptime(data['TIMESTAMP'], '%Y-%m-%d %I:%M:%S.%f') # repassando para data object 

        UUID = TransactionsModel.create_UUID() # criando a UUID personalizada dos Patients

        transaction = TransactionsModel(UUID , **data)

        try:
            transaction.save_patient()
        except:
            return {'message': 'An internal error ocurred trying to save transactions'}, 500 # Internal Server Error
        
        return transaction.json(), 200