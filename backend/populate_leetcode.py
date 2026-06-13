import requests
import pymysql
import time

def fetch_and_populate():
    url = "https://leetcode.com/api/problems/all/"
    print("Fetching problems from LeetCode API...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    problems = data.get("stat_status_pairs", [])
    print(f"Found {len(problems)} problems.")

    # Mapping difficulty levels
    diff_map = {1: "Easy", 2: "Medium", 3: "Hard"}

    try:
        conn = pymysql.connect(host='localhost', user='root', password='1531', database='dsa_tracker')
        cursor = conn.cursor()

        # Clear existing problems or just insert new ones
        # For simplicity, we'll use REPLACE INTO if we had a unique constraint, 
        # but let's just insert and avoid duplicates manually or use TRUNCATE
        print("Clearing old problems...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE problems;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        print("Inserting new problems...")
        batch_size = 100
        current_batch = []
        
        # We also need a way to assign 'topic' since the simple API doesn't give topics.
        # We can default to 'General' or try to guess. 
        # For 'all', we'll just use 'LeetCode' as topic for now.

        for p in problems:
            stat = p.get("stat", {})
            title = stat.get("question__title")
            slug = stat.get("question__title_slug")
            level = p.get("difficulty", {}).get("level")
            difficulty = diff_map.get(level, "Medium")
            link = f"https://leetcode.com/problems/{slug}/"
            
            if title and slug:
                current_batch.append((title, difficulty, "General", link))
                
            if len(current_batch) >= batch_size:
                cursor.executemany(
                    "INSERT INTO problems (title, difficulty, topic, leetcode_link) VALUES (%s, %s, %s, %s)",
                    current_batch
                )
                conn.commit()
                current_batch = []
        
        if current_batch:
            cursor.executemany(
                "INSERT INTO problems (title, difficulty, topic, leetcode_link) VALUES (%s, %s, %s, %s)",
                current_batch
            )
            conn.commit()

        print("Database population complete.")
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    fetch_and_populate()
