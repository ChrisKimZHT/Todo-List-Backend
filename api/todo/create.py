import pydantic.error_wrappers
from flask import abort, request, jsonify
from api.todo import todo_bp
from pydantic_model.TodoCreateModel import TodoCreateModel
from jwtauth import verify_jwt
from models import Todo
from ext import db


@todo_bp.route("/create", methods=["POST"])
def todoCreate():
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

    request_data = request.get_json()

    # 数据校验
    try:
        validated_data = TodoCreateModel(**request_data).dict()
    except pydantic.error_wrappers.ValidationError as e:
        abort(400, description=f"Request Format Error. {e}")
        return
    todo_data = validated_data["data"]

    # 数据库操作
    try:
        new_todo = Todo(userid, todo_data["title"], todo_data["detail"], todo_data["begin"],
                        todo_data["end"], todo_data["isDeadLine"], todo_data["isFinished"])
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
