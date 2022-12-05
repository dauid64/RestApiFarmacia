from flask_restful import Resource, reqparse
from models.users import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('USERNAME', type=str, required=True, help="The field 'USERNAME' cannot be left blank")
args.add_argument('PASSWORD', type=str, required=True, help="The field 'PASSWORD' cannot be left blank")

class User(Resource):
    def get(self, USERNAME):
        user = UserModel.find_by_login(USERNAME)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 # not found
    
    @jwt_required()
    def delete(self, USERNAME):
        user = UserModel.find_by_login(USERNAME)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500 # Internal Server Error
                
            return {'message': 'User Deleted.'}

        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    
    def post(self):
        data = args.parse_args()
    
        if UserModel.find_by_login(data['USERNAME']):
            return {"message": f"The USERNAME '{data['USERNAME']}' already exists."}, 400
        
        UUID = UserModel.create_UUID() # criando a UUID personalizada dos usuarios
        
        user = UserModel(UUID, **data)
        
        try:
            user.save_user()
        except:
            return {'message': 'An internal error ocurred trying to create a new user .'}, 500 # Internal Server Error
        return {'message': 'User created successfully'}, 201 # Created
    
class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = args.parse_args()
        user = UserModel.find_by_login(data['USERNAME'])

        if user and hmac.compare_digest(user.PASSWORD, data['PASSWORD']):
            token_acess = create_access_token(identity=user.UUID)
            return {'acess_token': token_acess}, 200
        
        return {'message': 'The USERNAME or PASSWORD is incorrect.'}, 401 # Unauthorize 

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logget out sucessfully'}, 200
