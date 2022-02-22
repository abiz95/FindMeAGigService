import pymysql
from appConfig.db_config import mysql


def get_data_where(query, data):  # conditional data fetching
    conn: any
    cursor: any
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, data)
        print(cursor)
        data = cursor.fetchall()  # The fetchall() get the result set as a list of tuples or an empty list
        return data
    except Exception as e:
        print(e)
        # raise ValueError(e)
    finally:
        cursor.close()
        conn.close()


def get_all_data(query):  # to fetch all data
    conn: any
    cursor: any
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        response = cursor.fetchall()
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def commit_query(query, data):
    conn: any
    cursor: any
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, data)
        print(cursor)
        data = cursor.fetchall()
        conn.commit()
        return data
    except Exception as e:
        print(e)
        # raise ValueError(e)
    finally:
        cursor.close()
        conn.close()
