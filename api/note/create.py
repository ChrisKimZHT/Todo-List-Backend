from api.note import note_bp
from flask import request, abort, jsonify
import pydantic.error_wrappers
from pydantic_model.NoteCreateModel import NoteCreateModel
from jwtauth import verify_jwt
from models import Note
from ext import db


@note_bp.route("/create", methods=["POST"])
def noteCreate():
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
        request_data["data"]["id"] = 0  # 用于通过数据校验，此数据没有实际意义（数据库会自增ID
        validated_data = NoteCreateModel(**request_data).dict()
    except pydantic.error_wrappers.ValidationError as e:
        abort(400, description=f"Request Format Error. {e}")
        return
    note_data = validated_data["data"]

    # 数据库操作
    try:
        new_note = Note(userID, note_data["title"], note_data["content"], note_data["date"], note_data["isStared"])
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
