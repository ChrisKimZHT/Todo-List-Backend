from flask import abort, jsonify
from api.todo import todo_bp
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


@todo_bp.route("/list", methods=["GET"])
def todoList():
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
        sql = "SELECT * FROM todo"
        mycursor.execute(sql)
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
                "title": todo[1],
                "detail": todo[2],
                "begin": todo[3],
                "end": todo[4],
                "isDeadLine": bool(todo[5]),
                "isFinished": bool(todo[6]),
            })
        return jsonify({"data": todo_list, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
