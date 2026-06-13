import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='1531')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS dsa_tracker")
    print("Database dsa_tracker created or already exists")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
