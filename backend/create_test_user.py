from auth import hash_password
import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='1531', database='dsa_tracker')
    cursor = conn.cursor()
    
    hashed = hash_password("testpass123")
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE password=%s",
        ("testuser", "test@example.com", hashed, hashed)
    )
    conn.commit()
    print("Test user created: test@example.com / testpass123")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
