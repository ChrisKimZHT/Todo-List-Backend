from flask import abort, jsonify, request
from api.todo import todo_bp
from jwtauth import verify_jwt
from models import Todo


@todo_bp.route("/list", methods=["GET"])
def todoList():
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
            result.append({
                "id": todo.id,
                "title": todo.title,
                "detail": todo.detail,
                "begin": todo.begin,
                "end": todo.end,
                "isDeadLine": todo.isDeadLine,
                "isFinished": todo.isFinished,
            })
        return jsonify({"data": result, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
