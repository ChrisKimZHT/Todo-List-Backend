from api.todo import todo_bp
from flask import request, abort, jsonify
from jwtauth import verify_jwt
from models import Todo


@todo_bp.route("/get", methods=["GET"])
def todoGet():
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
        request_id = int(request_arg["id"])
    except ValueError as e:
        abort(400, description=f"Request Format Error. {e}")
        return

    # 数据库操作
    selected_todo = Todo.query.filter_by(id=request_id, userID=userID).first()

    # 检测数据是否存在
    if selected_todo is None:
        abort(400, description="Request ID Not Found.")
        return

    # 数据处理操作
    try:
        data = {
            "id": selected_todo.id,
            "title": selected_todo.title,
            "detail": selected_todo.detail,
            "begin": selected_todo.begin,
            "end": selected_todo.end,
            "isDeadLine": selected_todo.isDeadLine,
            "isFinished": selected_todo.isFinished,
        }
        return jsonify({"data": data, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
