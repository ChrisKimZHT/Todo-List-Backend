from api.auth import auth_bp
from flask import request, abort, jsonify
from utils.jwt_auth import verify_jwt


@auth_bp.route("/check", methods=["POST"])
def authCheck():
    # token校验
    header_auth = request.headers.get("Authorization")
    if header_auth is None:
        abort(401, description="Unauthorized.")
        return
    token = header_auth[7:]
    payload = verify_jwt(token)
    if payload is None:
        abort(401, description="Invaild Token.")
        return
    userid = payload["uid"]
    return jsonify({"status": 0, "message": "OK", "uid": userid})
