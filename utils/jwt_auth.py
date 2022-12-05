import jwt
import os
import time


def generate_jwt(payload):
    iat = int(time.time())
    exp = iat + int(os.environ.get("jwt_expiration_delta"))
    payload["iat"] = iat
    payload["exp"] = exp
    secret = os.environ.get("jwt_secret")
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_jwt(token):
    secret = os.environ.get("jwt_secret")
    try:
        payload = jwt.decode(token, secret, algorithm="HS256")
    except jwt.PyJWTError:
        payload = None
    return payload
