from api.auth import auth_bp
from flask import request, abort, jsonify
import mysql.connector
import os
from utils.jwt_auth import generate_jwt


@auth_bp.route("/login", methods=["POST"])
def authLogin():
    request_data = request.get_json()

    # 数据校验
    try:
        req_username = request_data["username"]
        req_password = request_data["password"]
    except KeyError as e:
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
        sql = f"SELECT * FROM user WHERE username=%s"
        val = (req_username,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        print(data)
        if len(data) == 0:
            return jsonify({"status": 1, "message": "User Not Found."})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()

    db_uid = data[0][0]
    db_password = data[0][2]
    if db_password != req_password:
        return jsonify({"status": 2, "message": "Password Not Match."})

    jwt = generate_jwt({"uid": db_uid})
    return jsonify({"token": jwt, "status": 0, "message": "OK"})
