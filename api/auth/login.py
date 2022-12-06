from api.auth import auth_bp
from flask import request, abort, jsonify
from jwtauth import generate_jwt
from models import User


@auth_bp.route("/login", methods=["POST"])
def authLogin():
    request_data = request.get_json()

    # 数据校验
    try:
        req_username = request_data["username"]
        req_password = request_data["password"]
    except KeyError as e:
        abort(400, description=f"Request Format Error. {e}")
        return

    # 数据库操作
    try:
        # 先检查用户是否存在
        data = User.query.filter_by(username=req_username).first()
        if data is None:
            return jsonify({"status": 1, "message": "User Not Found."})
    except Exception as e:
        abort(500, description=f"Database Error. {e}")
        return

    db_uid = data.id
    db_password = data.password
    if db_password != req_password:
        return jsonify({"status": 2, "message": "Password Not Match."})

    jwt = generate_jwt({"uid": db_uid})

    return jsonify({"token": jwt, "status": 0, "message": "OK", "uid": db_uid})
