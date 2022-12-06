from api.note import note_bp
from flask import abort, request, jsonify
from jwtauth import verify_jwt
from models import Note
from ext import db


@note_bp.route("/delete", methods=["DELETE"])
def noteDelete():
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
        need_delete = Note.query.filter_by(userID=userID, id=request_id).first()
        db.session.delete(need_delete)
        db.session.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
