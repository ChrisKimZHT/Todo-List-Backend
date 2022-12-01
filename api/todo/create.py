import pydantic.error_wrappers
from flask import abort, request, jsonify
from api.todo import todo_bp
import mysql.connector
import os
from request_model.TodoCreateModel import TodoCreateModel


@todo_bp.route("/create", methods=["POST"])
def todoCreate():
    request_data = request.get_json()

    # 数据校验
    try:
        validated_data = TodoCreateModel(**request_data).dict()
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
        sql = f"INSERT INTO todo (title, detail, begin, end, isDeadLine, isFinished) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (todo_data["title"], todo_data["detail"], todo_data["begin"],
               todo_data["end"], todo_data["isDeadLine"], todo_data["isFinished"])
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({"status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()
