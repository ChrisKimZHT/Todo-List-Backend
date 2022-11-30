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
        return
    finally:
        mydb.close()

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
CREATE TABLE Todo (
    ID int NOT NULL AUTO_INCREMENT,
    Title varchar(255),
    Detail varchar(255),
    BeginTime int,
    EndTime int,
    IsDeadLine boolean,
    IsFinished boolean,
    PRIMARY KEY (ID)
);
""")
        print("Todo数据表创建完成")
        mycursor.execute("""
CREATE TABLE Note (
    ID int NOT NULL AUTO_INCREMENT,
    Title varchar(255),
    Content varchar(255),
    CreateTime int,
    IsStar boolean,
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
