import jwt
import os


def hash_info(info):
    hashed_info = jwt.encode(
        info, 
        os.environ.get('SECRET_KEY'), 
        os.environ.get('ALGORITHM')
    )
            
    return hashed_info