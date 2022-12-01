from api.note import note_bp
from flask import abort, request, jsonify
import mysql.connector
import os


@note_bp.route("/delete", methods=["DELETE"])
def noteDelete():
    request_data = request.get_json()

    # 数据校验
    try:
        request_id = int(request_data["id"])
    except ValueError as e:
        abort(400, description=f"Request Format Error. {e}")
        return

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
        sql = f"DELETE FROM note WHERE id={request_id}"
        mycursor.execute(sql)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
