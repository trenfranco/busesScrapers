import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bus_inventory",
        port=3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )