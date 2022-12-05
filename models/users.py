from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'USERS'

    UUID = banco.Column(banco.String(256), primary_key=True)
    USERNAME = banco.Column(banco.String(50))
    PASSWORD = banco.Column(banco.String(256))

    def __init__(self, UUID, USERNAME, PASSWORD):
        self.UUID = UUID
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD

    def json(self):
        return {
            'UUID': self.UUID,
            'USERNAME': self.USERNAME
        }

    @classmethod
    def find_by_login(cls, USERNAME):
        '''encontra no sistema o User através do nome passado'''
        user = cls.query.filter_by(USERNAME=USERNAME).first() # SELECT * FROM user WHERE user_id = user_id LIMIT 1
        if user:
            return user
        return None 

    @classmethod
    def create_UUID(cls):
        '''Função para criar o UUID personalizado dos usuarios em ordem'''
        user = cls.query.order_by(cls.UUID.desc()).first()
        if user:
            number = int(user.UUID[5:]) + 1
            return "USER" + str(number).zfill(4)
        else:
            return "USER0000"

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
