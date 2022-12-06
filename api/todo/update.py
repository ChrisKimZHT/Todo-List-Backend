from api.todo import todo_bp
from flask import request, abort, jsonify
import pydantic.error_wrappers
from pydantic_model.TodoUpdateModel import TodoUpdateModel
from jwtauth import verify_jwt
from models import Todo
from ext import db


@todo_bp.route("/update", methods=["POST"])
def todoUpdate():
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
        validated_data = TodoUpdateModel(**request_data).dict()
    except pydantic.error_wrappers.ValidationError as e:
        abort(400, description=f"Request Format Error. {e}")
        return
    todo_data = validated_data["data"]

    # 数据库操作
    try:
        selected_todo = Todo.query.filter_by(userID=userID, id=todo_data["id"]).first()
        selected_todo.title = todo_data["title"]
        selected_todo.detail = todo_data["detail"]
        selected_todo.begin = todo_data["begin"]
        selected_todo.end = todo_data["end"]
        selected_todo.isDeadLine = todo_data["isDeadLine"]
        selected_todo.isFinished = todo_data["isFinished"]
        db.session.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
