from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import sqlite3
from models.pharmcies import PharmacieModel
from resources.filters import normalize_path_params_pharmacy, consult_without_CITY, consult_with_CITY_NAME, consult_without_NAME, consult_without_CITY_NAME

path_param = reqparse.RequestParser()
path_param.add_argument('CITY', type=str)
path_param.add_argument('NAME', type=str)
path_param.add_argument('LIMIT', type=int)
path_param.add_argument('OFFSET', type=int)

class Pharmacies(Resource):
    @jwt_required()
    def get(self):
        '''Retorna as informações do sistemas das farmácias com a opção de utilizar filtros'''
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        data = path_param.parse_args()

        data = path_param.parse_args()

        data_valid = {key:data[key] for key in data if data[key] is not None}

        parameters = normalize_path_params_pharmacy(**data_valid)

        if not parameters.get('CITY') and not parameters.get('NAME'):
            content = tuple([parameters[key] for key in parameters])
            result = cursor.execute(consult_without_CITY_NAME, content)
        elif not parameters.get('NAME'):
            content = tuple([parameters[key] for key in parameters])
            result = cursor.execute(consult_without_NAME, content)
        elif not parameters.get('CITY'):
            content = tuple([parameters[key] for key in parameters])
            result = cursor.execute(consult_without_CITY, content)
        else:
            content = tuple([parameters[key] for key in parameters])
            result = cursor.execute(consult_with_CITY_NAME, content)  

        pharmacies = []

        if result:
            for line in result:
                pharmacies.append({
                    'UUID': line[0],
                    'NAME': line[1],
                    'CITY': line[2]
                })

            return {'PHARMACIES': pharmacies}, 200   

        return {'message': 'Not found'}, 400




class Pharmacie(Resource):
    
    args = reqparse.RequestParser()
    args.add_argument('NAME', type=str, required=True, help="The field 'NAME' cannot be left blank")
    args.add_argument('CITY', type=str, required=True, help="The field 'CITY' cannot be left blank")

    @jwt_required()
    def post(self):
        '''Adiciona novas farmácias no sistema'''
        data = Pharmacie.args.parse_args()

        UUID = PharmacieModel.create_UUID() # criando a UUID personalizada das Pharmacies

        pharmacie = PharmacieModel(UUID , **data)

        try:
            pharmacie.save_patient()
        except:
            return {'message': 'An internal error ocurred trying to save patient'}, 500 # Internal Server Error
        
        return pharmacie.json(), 200