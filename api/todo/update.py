from api.todo import todo_bp
from flask import request, abort, jsonify
import pydantic.error_wrappers
from model.TodoUpdateModel import TodoUpdateModel
import mysql.connector
import os
from utils.jwt_auth import verify_jwt


@todo_bp.route("/update", methods=["POST"])
def todoUpdate():
    request_data = request.get_json()

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
        validated_data = TodoUpdateModel(**request_data).dict()
    except pydantic.error_wrappers.ValidationError as e:
        abort(400, description=f"Request Format Error. {e}")
        return
    todo_data = validated_data["data"]

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
        sql = f"UPDATE todo SET title = %s, detail = %s, begin = %s, end = %s, isDeadLine = %s, isFinished = %s WHERE id = %s AND userid = %s"
        val = (todo_data["title"], todo_data["detail"], todo_data["begin"], todo_data["end"],
               todo_data["isDeadLine"], todo_data["isFinished"], todo_data["id"], userid)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
