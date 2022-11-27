def normalize_path_params_pharmacy(NAME=None, CITY=None, LIMIT=50, OFFSET=0, **data):
    '''normaliza os parametros passados em biblioteca para melhor utilização'''
    if not NAME and not CITY:
        return {
            'LIMIT': LIMIT,
            'OFFSET': OFFSET
        }    
    if not NAME and CITY:
        return {
            'CITY': CITY,
            'LIMIT': LIMIT,
            'OFFSET': OFFSET
        }
    if NAME and not CITY:
        return {
            'NAME': NAME,
            'LIMIT': LIMIT,
            'OFFSET': OFFSET
        }   
    return {
        'NAME': NAME,
        'CITY': CITY,
        'LIMIT': LIMIT,
        'OFFSET': OFFSET
    }

consult_without_CITY = "SELECT * FROM PHARMACIES WHERE NAME = ? LIMIT ? OFFSET ?"
    
consult_without_NAME = "SELECT * FROM PHARMACIES WHERE CITY = ? LIMIT ? OFFSET ?"

consult_without_CITY_NAME = "SELECT * FROM PHARMACIES LIMIT ? OFFSET ?"

consult_with_CITY_NAME = "SELECT * FROM PHARMACIES WHERE NAME = ? and CITY = ? LIMIT ? OFFSET ?"

