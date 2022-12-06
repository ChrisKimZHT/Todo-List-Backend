from api.auth import auth_bp
from flask import request, abort, jsonify, current_app
from ext import db
from models import User


@auth_bp.route("/register", methods=["POST"])
def authRegister():
    request_data = request.get_json()

    # 数据校验
    try:
        username = request_data["username"]
        password = request_data["password"]
        if not current_app.config["USERNAME_LEN_MIN"] <= len(username) <= current_app.config["USERNAME_LEN_MAX"]:
            abort(400, description="Username Length Invaild.")
            return
        if not current_app.config["PASSWORD_LEN_MIN"] <= len(password) <= current_app.config["PASSWORD_LEN_MAX"]:
            abort(400, description="Password Length Invaild.")
            return
    except Exception as e:
        abort(400, description=f"Request Format Error. {e}")
        return

    # 数据库操作
    try:
        # 先查重
        data = User.query.filter_by(username=username).first()
        if data is not None:
            return jsonify({"status": 1, "message": "User Existed."})

        # 再插入
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": 0, "message": "OK", "uid": new_user.id})
    except Exception as e:
        abort(500, description=f"Database Error. {e}")
        return
