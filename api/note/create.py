from api.note import note_bp
from flask import request, abort, jsonify
import mysql.connector
import os
import pydantic.error_wrappers
from model.NoteCreateModel import NoteCreateModel
from utils.jwt_auth import verify_jwt


@note_bp.route("/create", methods=["POST"])
def noteCreate():
    request_data = request.get_json()

    # token校验
    header_auth = request.headers.get("Authorization")
    token = header_auth[7:]
    payload = verify_jwt(token)
    if payload is None:
        abort(401, description="Invaild Token.")
        return
    userid = payload["uid"]

    # 数据校验
    try:
        request_data["data"]["id"] = 0  # 用于通过数据校验，此数据没有实际意义（数据库会自增ID
        validated_data = NoteCreateModel(**request_data).dict()
    except pydantic.error_wrappers.ValidationError as e:
        abort(400, description=f"Request Format Error. {e}")
        return
    note_data = validated_data["data"]

    # 连接数据库
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get("db_host"),
            user=os.environ.get("db_user"),
            password=os.environ.get("db_password"),
            database=os.environ.get("db_name")
        )
    except Exception as e:
        abort(500, description=f"Database Connection Error. {e}")
        return

    # 数据库操作
    try:
        mycursor = mydb.cursor()
        sql = f"INSERT INTO note (userid, title, content, date, star) VALUES (%s, %s, %s, %s, %s)"
        val = (userid, note_data["title"], note_data["content"], note_data["date"], note_data["star"])
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
