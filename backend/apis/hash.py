import jwt
import os


def hash_info(info):
    hashed_info = jwt.encode(
        {"info": info},
        os.environ.get('ALGORITHM')
    )
            
    return hashed_info