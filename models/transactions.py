from sql_alchemy import banco

class TransactionsModel(banco.Model):

    __tablename__ = 'TRANSACTIONS'

    UUID = banco.Column(banco.String(256), primary_key=True)
    PATIENT_UUID = banco.Column(banco.Integer, banco.ForeignKey('PATIENTS.UUID'))
    PHARMACY_UUID = banco.Column(banco.Integer, banco.ForeignKey('PHARMACIES.UUID'))
    AMOUNT = banco.Column(banco.Numeric)
    TIMESTAMP = banco.Column(banco.DateTime)
    patient = banco.relationship('PatientsModel', foreign_keys=PATIENT_UUID)
    pharmacy = banco.relationship('PharmacieModel', foreign_keys=PHARMACY_UUID)
    

    def __init__(self, UUID, PATIENT_UUID, PHARMACY_UUID, AMOUNT, TIMESTAMP):
        self.UUID = UUID
        self.PATIENT_UUID = PATIENT_UUID
        self.PHARMACY_UUID = PHARMACY_UUID
        self.AMOUNT = AMOUNT
        self.TIMESTAMP = TIMESTAMP

    @classmethod
    def create_UUID(cls):
        '''Função para criar o UUID personalizado das Transações em ordem'''
        patient = cls.query.order_by(cls.UUID.desc()).first()
        if patient:
            number = int(patient.UUID[5:]) + 1
            return "TRAN" + str(number).zfill(4)
        else:
            return "TRAN0000"

    def json(self):
        return {
            'UUID': self.UUID,
            'PATIENT': self.patient.json(),
            'PHARMACY': self.pharmacy.json(),
            'AMOUNT': float(self.AMOUNT),
            'TIMESTAMP': str(self.TIMESTAMP)
        }

    def save_patient(self):
        banco.session.add(self)
        banco.session.commit()