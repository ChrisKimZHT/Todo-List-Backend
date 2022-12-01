from api.todo import todo_bp
from flask import request, abort, jsonify
import mysql.connector
import os
import time


@todo_bp.route("/getToday", methods=["GET"])
def todoGetToday():
    request_arg = request.args.to_dict()

    # 数据校验
    try:
        year = int(request_arg["year"])
        month = int(request_arg["month"])
        day = int(request_arg["day"])
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
        sql = f"SELECT * FROM todo"
        mycursor.execute(sql)
        data = mycursor.fetchall()
    except Exception as e:
        abort(500, description=f"Database Operation Error. {e}")
        return
    finally:
        mydb.close()

    # 数据处理操作
    try:
        result = []
        for row in data:
            temp = {
                "id": row[0],
                "title": row[1],
                "detail": row[2],
                "begin": row[3],
                "end": row[4],
                "isDeadLine": bool(row[5]),
                "isFinished": bool(row[6]),
            }
            if temp["isDeadLine"]:
                todo_time = time.localtime(temp["end"])
            else:
                todo_time = time.localtime(temp["begin"])
            if todo_time.tm_year == year and todo_time.tm_mon == month and todo_time.tm_mday == day:
                result.append(temp)
        return jsonify({"data": result, "status": 0, "message": "OK"})
    except Exception as e:
        abort(500, description=f"Process Data Error. {e}")
        return
