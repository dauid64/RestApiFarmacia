from sql_alchemy import banco

class PharmacieModel(banco.Model):
    __tablename__ = 'PHARMACIES'

    UUID = banco.Column(banco.String(256), primary_key=True)
    NAME = banco.Column(banco.String(50))
    CITY = banco.Column(banco.String(50))

    def __init__(self, UUID, NAME, CITY):

        self.UUID = UUID
        self.NAME = NAME
        self.CITY = CITY

    @classmethod
    def create_UUID(cls):
        '''Função para criar o UUID personalizado das Pharmacias em ordem'''
        pharmacy = cls.query.order_by(cls.UUID.desc()).first()
        if pharmacy:
            number = int(pharmacy.UUID[6:]) + 1
            return "PHARM" + str(number).zfill(4)
        else:
            return "PHARM0000"

    @classmethod
    def find_by_id(cls, UUID):
        '''encontra a farmácia de acordo com o UUID passado'''
        pharmacy = cls.query.filter_by(UUID=UUID).first()
        if pharmacy:
            return pharmacy
        return None

    def json(self):
        return {
            'UUID': self.UUID,
            'NAME': self.NAME,
            'CITY': self.CITY
        }

    def save_patient(self):
        banco.session.add(self)
        banco.session.commit()