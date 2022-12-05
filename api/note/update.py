from api.note import note_bp
from flask import request, abort, jsonify
import mysql.connector
import os
import pydantic.error_wrappers
from model.NoteUpdateModel import NoteUpdateModel
from utils.jwt_auth import verify_jwt


@note_bp.route("/update", methods=["POST"])
def noteUpdate():
    # token校验
    header_auth = request.headers.get("Authorization")
    token = header_auth[7:]
    payload = verify_jwt(token)
    if payload is None:
        abort(401, description="Invaild Token.")
        return
    userid = payload["uid"]

    request_data = request.get_json()
    # 数据校验
    try:
        validated_data = NoteUpdateModel(**request_data).dict()
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
        sql = f"UPDATE note SET title = %s, content = %s, date = %s, star = %s WHERE id = %s AND userid = %s"
        val = (note_data["title"], note_data["content"], note_data["date"], note_data["star"], note_data["id"], userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
