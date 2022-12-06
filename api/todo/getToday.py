from api.todo import todo_bp
from flask import request, abort, jsonify
import time
from jwtauth import verify_jwt
from models import Todo


@todo_bp.route("/getToday", methods=["GET"])
def todoGetToday():
    request_arg = request.args.to_dict()

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
        year = int(request_arg["year"])
        month = int(request_arg["month"])
        day = int(request_arg["day"])
    except ValueError as e:
        abort(400, description=f"Request Format Error. {e}")
        return

    # 数据库操作
    try:
        all_todo = Todo.query.filter_by(userID=userID).all()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return

    # 数据处理操作
    try:
        result = []
        for todo in all_todo:
            temp = {
                "id": todo.id,
                "title": todo.title,
                "detail": todo.detail,
                "begin": todo.begin,
                "end": todo.end,
                "isDeadLine": todo.isDeadLine,
                "isFinished": todo.isFinished,
            }
            if temp["isDeadLine"]:
                todo_time = time.localtime(temp["end"])
            else:
                todo_time = time.localtime(temp["begin"])
            if todo_time.tm_year == year and todo_time.tm_mon == month and todo_time.tm_mday == day:
                result.append(temp)
        return jsonify({"data": result, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
