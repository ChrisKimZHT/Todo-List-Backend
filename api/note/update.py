from api.note import note_bp
from flask import request, abort, jsonify
import mysql.connector
import os
import pydantic.error_wrappers
from model.NoteUpdateModel import NoteUpdateModel


@note_bp.route("/update", methods=["POST"])
def noteUpdate():
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
        sql = f"UPDATE note SET title = %s, content = %s, date = %s, star = %s WHERE id = %s"
        val = (note_data["title"], note_data["content"], note_data["date"], note_data["star"], note_data["id"])
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
