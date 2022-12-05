from flask import abort, jsonify, request
from api.todo import todo_bp
import mysql.connector
import os
from utils.jwt_auth import verify_jwt


@todo_bp.route("/nextID", methods=["GET"])
def todoNextID():
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
        sql = "SHOW TABLE STATUS LIKE 'todo'"
        mycursor.execute(sql)
        data = mycursor.fetchall()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()

    # 数据处理操作
    try:
        next_id = data[0][10]
        if next_id is None:
            next_id = 1
        return jsonify({"nextID": next_id, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
