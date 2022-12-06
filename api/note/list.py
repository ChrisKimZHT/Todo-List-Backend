from api.note import note_bp
from flask import abort, jsonify, request
from jwtauth import verify_jwt
from models import Note


@note_bp.route("/list", methods=["GET"])
def noteList():
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
        all_note = Note.query.filter_by(userID=userID).all()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return

    # 数据处理操作
    try:
        res = []
        for note in all_note:
            res.append({
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "date": note.date,
                "isStared": note.isStared,
            })
        return jsonify({"data": res, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
