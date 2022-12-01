import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def init_db() -> None:
    # 连接MySQL服务器
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get("db_host"),
            user=os.environ.get("db_user"),
            password=os.environ.get("db_password"),
        )
        print("连接MySQL服务器成功")
    except Exception as e:
        print(f"连接MySQL服务器失败: {e}")
        return

    # 创建数据库
    try:
        mycursor = mydb.cursor()
        mycursor.execute(f"CREATE DATABASE {os.environ.get('db_name')}")
        print(f"成功创建数据库: {os.environ.get('db_name')}")
    except Exception as e:
        print(f"创建数据库失败: {e}")
    finally:
        mydb.close()

    choice = input("数据库可能已经存在，输入y继续进行建表: ")
    if not choice.lower() == "y":
        return

    # 连接数据库
    try:
        mydb = mysql.connector.connect(
            host=os.environ.get("db_host"),
            user=os.environ.get("db_user"),
            password=os.environ.get("db_password"),
            database=os.environ.get("db_name")
        )
        print("连接数据库成功")
        mycursor = mydb.cursor()
    except Exception as e:
        print(f"连接数据库失败: {e}")
        return

    # 创建数据表
    try:
        mycursor.execute("""
CREATE TABLE todo (
    id int NOT NULL AUTO_INCREMENT,
    title varchar(255),
    detail varchar(255),
    begin int,
    end int,
    isDeadLine boolean,
    isFinished boolean,
    PRIMARY KEY (id)
);
""")
        print("Todo数据表创建完成")
        mycursor.execute("""
CREATE TABLE note (
    id int NOT NULL AUTO_INCREMENT,
    title varchar(255),
    content varchar(255),
    date int,
    star boolean,
    PRIMARY KEY (ID)
);
""")
        print("Note数据表创建完成")
        print("数据库初始化完成")
    except Exception as e:
        print(f"创建数据表失败{e}")
        return
    finally:
        mydb.close()


if __name__ == '__main__':
    init_db()
