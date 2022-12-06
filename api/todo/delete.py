from api.todo import todo_bp
from flask import request, abort, jsonify
from jwtauth import verify_jwt
from models import Todo
from ext import db


@todo_bp.route("/delete", methods=["DELETE"])
def todoDelete():
    request_data = request.get_json()

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
    userID = payload["uid"]

    # 数据校验
    try:
        request_id = int(request_data["id"])
    except ValueError as e:
        abort(400, description=f"Request Format Error. {e}")
        return

    # 数据库操作
    try:
        need_delete = Todo.query.filter_by(id=request_id, userID=userID).first()
        db.session.delete(need_delete)
        db.session.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
