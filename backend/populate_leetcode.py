import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

load_dotenv()

def fetch_and_populate():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env")
        return

    # Render PostgreSQL might need a slightly different URL for SQLAlchemy if it uses postgres://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(DATABASE_URL)

    # Check if table is already populated
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT count(*) FROM problems"))
            count = result.scalar()
            if count > 0:
                print(f"Database already has {count} problems. Skipping population.")
                return
    except Exception as e:
        print("Table might not exist yet, proceeding to create/populate...")

    url = "https://leetcode.com/api/problems/all/"
    print(f"Fetching problems from LeetCode API...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    problems = data.get("stat_status_pairs", [])
    print(f"Found {len(problems)} problems.")

    diff_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    
    print("Preparing data...")
    problem_list = []
    for p in problems:
        stat = p.get("stat", {})
        title = stat.get("question__title")
        slug = stat.get("question__title_slug")
        level = p.get("difficulty", {}).get("level")
        difficulty = diff_map.get(level, "Medium")
        link = f"https://leetcode.com/problems/{slug}/"
        
        if title and slug:
            problem_list.append({
                "title": title,
                "difficulty": difficulty,
                "topic": "General",
                "leetcode_link": link
            })

    print(f"Inserting {len(problem_list)} problems into the database...")
    df = pd.DataFrame(problem_list)
    
    try:
        # Use 'append' instead of 'replace' to avoid dropping the table
        # We also need to be careful about headers
        df.to_sql("problems", con=engine, if_exists="append", index=False)
        print("Database population complete!")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    fetch_and_populate()
