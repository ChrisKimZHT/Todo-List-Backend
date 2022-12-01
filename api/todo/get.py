from api.todo import todo_bp
from flask import request, abort, jsonify
import mysql.connector
import os


@todo_bp.route("/get", methods=["GET"])
def todoGet():
    request_arg = request.args.to_dict()

    # 数据校验
    try:
        request_id = int(request_arg["id"])
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
        sql = f"SELECT * FROM todo WHERE id={request_id}"
        mycursor.execute(sql)
        data = mycursor.fetchall()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()

    # 检测数据是否存在
    if len(data) == 0:
        abort(400, description="Request ID Not Found.")
        return

    # 数据处理操作
    try:
        selected_todo = {
            "id": data[0][0],
            "title": data[0][1],
            "detail": data[0][2],
            "begin": data[0][3],
            "end": data[0][4],
            "isDeadLine": bool(data[0][5]),
            "isFinished": bool(data[0][6]),
        }
        return jsonify({"data": selected_todo, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
