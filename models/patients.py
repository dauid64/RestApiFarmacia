from sql_alchemy import banco

class PatientsModel(banco.Model):
    __tablename__ = 'PATIENTS'

    UUID = banco.Column(banco.String(256), primary_key=True)
    FIRST_NAME = banco.Column(banco.String(30))
    LAST_NAME = banco.Column(banco.String(30))
    DATE_OF_BIRTH = banco.Column(banco.Date())

    def __init__(self, UUID, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH):
        self.UUID = UUID
        self.FIRST_NAME = FIRST_NAME
        self.LAST_NAME = LAST_NAME
        self.DATE_OF_BIRTH = DATE_OF_BIRTH

    @classmethod
    def create_UUID(cls):
        '''Função para criar o UUID personalizado de Patients em ordem'''
        patient = cls.query.order_by(cls.UUID.desc()).first()
        if patient:
            number = int(patient.UUID[7:]) + 1
            return "PATIENT" + str(number).zfill(4)
        else:
            return "PATIENT0000"

    @classmethod
    def find_by_id(cls, UUID):
        '''encontra o paciente de acordo com o UUID passado'''
        patient = cls.query.filter_by(UUID=UUID).first()
        if patient:
            return patient
        return None

    def json(self):
        return {
            'UUID': self.UUID,
            'FIRST NAME': self.FIRST_NAME,
            'LAST NAME': self.LAST_NAME,
            'DATE OF BIRTH': self.DATE_OF_BIRTH.isoformat()
        }

    def save_patient(self):
        banco.session.add(self)
        banco.session.commit()
