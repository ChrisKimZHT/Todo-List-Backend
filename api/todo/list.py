from flask import abort, jsonify, request
from api.todo import todo_bp
import mysql.connector
import os
from utils.jwt_auth import verify_jwt


@todo_bp.route("/list", methods=["GET"])
def todoList():
    # token校验
    header_auth = request.headers.get("Authorization")
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
        sql = "SELECT * FROM todo WHERE userid = %s"
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
        todo_list = []
        for todo in data:
            todo_list.append({
                "id": todo[0],
                "userid": todo[1],
                "title": todo[2],
                "detail": todo[3],
                "begin": todo[4],
                "end": todo[5],
                "isDeadLine": bool(todo[6]),
                "isFinished": bool(todo[7]),
            })
        return jsonify({"data": todo_list, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
