import pymysql
from config.db_config import mysql


def getData(query):
    conn: any
    cursor: any
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchall()
        # response = jsonify(data)
        # return response
        return data
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def saveData(query, data):
    conn: any
    cursor: any
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, data)
        print(cursor)
        data = cursor.fetchall()
        conn.commit()
        # response = jsonify(data)
        # return response
        return data
    except Exception as e:
        print(e)
        # raise ValueError(e)
    finally:
        cursor.close()
        conn.close()
