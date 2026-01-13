
import sqlite3
import sys

def main():
    conn = sqlite3.connect('extracted_results/elements.db')
    cursor = conn.cursor()
    
    keywords = ["cyberpunk", "neon", "blade runner", "warrior", "futuristic", "armor", "sci-fi"]
    
    print("Checking keywords in DB...")
    for kw in keywords:
        cursor.execute("SELECT count(*) FROM elements WHERE ai_prompt_template LIKE ? OR name LIKE ?", (f'%{kw}%', f'%{kw}%'))
        count = cursor.fetchone()[0]
        print(f"'{kw}': {count} matches")
        
        if count > 0:
            cursor.execute("SELECT name, category_id, ai_prompt_template FROM elements WHERE ai_prompt_template LIKE ? OR name LIKE ? LIMIT 3", (f'%{kw}%', f'%{kw}%'))
            rows = cursor.fetchall()
            for r in rows:
                print(f"   - {r[0]} ({r[1]}): {r[2][:50]}...")

    conn.close()

if __name__ == "__main__":
    main()
