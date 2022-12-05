from api.auth import auth_bp
from flask import request, abort, jsonify
import mysql.connector
import os


@auth_bp.route("/register", methods=["POST"])
def authRegister():
    request_data = request.get_json()

    # 数据校验
    try:
        username = request_data["username"]
        password = request_data["password"]
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
        val = (username,)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        if len(data):
            return jsonify({"status": 1, "message": "User Existed."})
    except Exception as e:
        mydb.close()
        abort(500, description=f"Database Operation Error. {e}")
        return

    try:
        mycursor = mydb.cursor()
        sql = f"INSERT INTO user (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
