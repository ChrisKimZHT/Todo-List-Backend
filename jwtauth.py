import jwt
import time
from flask import current_app


def generate_jwt(payload):
    iat = int(time.time())
    exp = iat + current_app.config["JWT_EXP_DELTA"]
    payload["iat"] = iat
    payload["exp"] = exp
    secret = current_app.config["JWT_SECRET_KEY"]
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_jwt(token):
    secret = current_app.config["JWT_SECRET_KEY"]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        payload = None
    return payload
