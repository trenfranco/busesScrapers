import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bus_inventory",
        port=3306,  # Default MySQL port
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

try:
    conn = get_connection()
    print("MYSQL connection ok")
    conn.close()
except Exception as e:
    print(f"MYSQL Connection failed {e}")
