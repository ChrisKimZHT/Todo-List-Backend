from api.note import note_bp
from flask import request, abort, jsonify
from jwtauth import verify_jwt
from models import Note


@note_bp.route("/get", methods=["GET"])
def noteGet():
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
    try:
        selected_note = Note.query.filter_by(userID=userID, id=request_id).first()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return

    # 检测数据是否存在
    if selected_note is None:
        abort(400, description="Request ID Not Found.")
        return

    # 数据处理操作
    try:
        data = {
            "id": selected_note.id,
            "title": selected_note.title,
            "content": selected_note.content,
            "date": selected_note.date,
            "isStared": selected_note.isStared,
        }
        return jsonify({"data": data, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
