from flask import abort, jsonify
from api.todo import todo_bp
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


@todo_bp.route("/nextID", methods=["GET"])
def todoNextID():
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
