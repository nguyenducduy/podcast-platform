import jwt
from flask import current_app


def decode_auth_token(auth_header):
    auth_token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            auth_token, current_app.config['SECRET_KEY'], algorithms='HS256')
        return payload['sub']
        # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        # if is_blacklisted_token:
        #     return 'Token blacklisted. Please log in again.'
        # else:
        #     return payload['sub']
    except jwt.ExpiredSignatureError:
        raise Exception('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token. Please log in again.')
