from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.patients import PatientsModel
from datetime import datetime  

class Patients(Resource):
    @jwt_required()
    def get(self):
        '''retorna todos os pacientes do sistema'''
        return {'patients': [patient.json() for patient in PatientsModel.query.all()]}

class Patient(Resource):
    
    args = reqparse.RequestParser()
    args.add_argument('FIRST_NAME', type=str, required=True, help="The field 'first name' cannot be left blank")
    args.add_argument('LAST_NAME', type=str, required=True, help="The field 'Last Name' cannot be left blank")
    args.add_argument('DATE_OF_BIRTH', required=True, help="The field 'Date of Birth' cannot be left blank")

    @jwt_required()
    def post(self):
        '''Adiciona novos pacientes no sistema'''
        data = Patient.args.parse_args()

        data['DATE_OF_BIRTH'] = datetime.strptime(data['DATE_OF_BIRTH'], '%Y-%m-%d').date() # repassando para data object 

        UUID = PatientsModel.create_UUID() # criando a UUID personalizada dos Patients

        patient = PatientsModel(UUID , **data)

        try:
            patient.save_patient()
        except:
            return {'message': 'An internal error ocurred trying to save patient'}, 500 # Internal Server Error
        
        return patient.json(), 200

class ModifyPatient(Resource):
    @jwt_required()
    def put(self, UUID):
        data = Patient.args.parse_args()

        data['DATE_OF_BIRTH'] = datetime.strptime(data['DATE_OF_BIRTH'], '%Y-%m-%d').date() # repassando para data object

        patient_find = PatientsModel.find_by_id(UUID)

        if patient_find:
            patient_find.update_patient(**data)
            try:
                patient_find.save_patient()
            except:
                return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server Error
            return patient_find.json(), 200
        
        patient = PatientsModel(UUID, **data)

        try:
            patient.save_patient()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # Internal Server Error
        return patient.json(), 201 # created criado