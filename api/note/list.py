from api.note import note_bp
import mysql.connector
import os
from flask import abort, jsonify, request
from utils.jwt_auth import verify_jwt


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
    userid = payload["uid"]

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
        sql = "SELECT * FROM note WHERE userid=%s"
        val = (userid,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()

    # 数据处理操作
    try:
        note_list = []
        for note in data:
            note_list.append({
                "id": note[0],
                "userid": note[1],
                "title": note[2],
                "content": note[3],
                "date": note[4],
                "star": bool(note[5]),
            })
        return jsonify({"data": note_list, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
