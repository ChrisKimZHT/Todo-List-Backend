from api.note import note_bp
import mysql.connector
import os
from flask import abort, jsonify


@note_bp.route("/list", methods=["GET"])
def noteList():
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
        sql = "SELECT * FROM note"
        mycursor.execute(sql)
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
                "title": note[1],
                "content": note[2],
                "date": note[3],
                "star": bool(note[4]),
            })
        return jsonify({"data": note_list, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
