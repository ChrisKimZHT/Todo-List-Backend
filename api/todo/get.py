from api.todo import todo_bp
from flask import request, abort, jsonify
import mysql.connector
import os
from utils.jwt_auth import verify_jwt


@todo_bp.route("/get", methods=["GET"])
def todoGet():
    request_arg = request.args.to_dict()

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
        sql = f"SELECT * FROM todo WHERE id={request_id} AND userid={userid}"
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
            "userid": data[0][1],
            "title": data[0][2],
            "detail": data[0][3],
            "begin": data[0][4],
            "end": data[0][5],
            "isDeadLine": bool(data[0][6]),
            "isFinished": bool(data[0][7]),
        }
        return jsonify({"data": selected_todo, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
