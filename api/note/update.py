from api.note import note_bp
from flask import request, abort, jsonify
import pydantic.error_wrappers
from model.NoteUpdateModel import NoteUpdateModel
from jwtauth import verify_jwt
from models import Note
from ext import db


@note_bp.route("/update", methods=["POST"])
def noteUpdate():
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

    request_data = request.get_json()
    # 数据校验
    try:
        validated_data = NoteUpdateModel(**request_data).dict()
    except pydantic.error_wrappers.ValidationError as e:
        abort(400, description=f"Request Format Error. {e}")
        return
    note_data = validated_data["data"]

    # 数据库操作
    try:
        select_note = Note.query.filter_by(userID=userID, id=note_data["id"]).first()
        select_note.title = note_data["title"]
        select_note.content = note_data["content"]
        select_note.date = note_data["date"]
        select_note.isStared = note_data["isStared"]
        db.session.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
