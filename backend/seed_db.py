import pymysql

problems = [
    ("Two Sum", "Easy", "Arrays", "https://leetcode.com/problems/two-sum/"),
    ("Add Two Numbers", "Medium", "Linked List", "https://leetcode.com/problems/add-two-numbers/"),
    ("Longest Substring Without Repeating Characters", "Medium", "Two Pointers", "https://leetcode.com/problems/longest-substring-without-repeating-characters/"),
    ("Median of Two Sorted Arrays", "Hard", "Arrays", "https://leetcode.com/problems/median-of-two-sorted-arrays/"),
    ("Reverse Integer", "Medium", "Sorting", "https://leetcode.com/problems/reverse-integer/"),
    ("Palindrome Number", "Easy", "Arrays", "https://leetcode.com/problems/palindrome-number/"),
    ("Regular Expression Matching", "Hard", "Dynamic Programming", "https://leetcode.com/problems/regular-expression-matching/"),
    ("Container With Most Water", "Medium", "Two Pointers", "https://leetcode.com/problems/container-with-most-water/"),
]

try:
    conn = pymysql.connect(host='localhost', user='root', password='1531', database='dsa_tracker')
    cursor = conn.cursor()
    
    # Check if problems table has data
    cursor.execute("SELECT COUNT(*) FROM problems")
    count = cursor.fetchone()[0]
    
    if count == 0:
        for title, diff, topic, link in problems:
            cursor.execute(
                "INSERT INTO problems (title, difficulty, topic, leetcode_link) VALUES (%s, %s, %s, %s)",
                (title, diff, topic, link)
            )
        conn.commit()
        print(f"Seeded {len(problems)} problems.")
    else:
        print("Problems table already has data.")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
