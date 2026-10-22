import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from odoo.http import request
from odoo.tools import config

SECRET_KEY = config.get('jwt_secret') or 'sendtrack_super_secure_jwt_secret_key_2026'
ALGORITHM = 'HS256'

def generate_token(user_id, partner_id=None):
    payload = {
        'user_id': user_id,
        'partner_id': partner_id,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validate_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return request.make_json_response({'error': 'Token missing or invalid'}, status=401)

        token = auth_header.split(' ', 1)[1]
        payload = validate_token(token)
        if not payload:
            return request.make_json_response({'error': 'Unauthorized or token expired'}, status=401)

        request.update_env(user=payload['user_id'])
        return fn(*args, **kwargs)
    return wrapper
