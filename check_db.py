import sqlite3
import os

DB_PATH = "backend/oriana_data.db"

def check_db():
    print(f"Checking database at {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("❌ Database file not found!")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("📊 Tables found:", [t[0] for t in tables])
        
        if 'settings' not in [t[0] for t in tables]:
            print("❌ 'settings' table missing!")
        else:
            print("✅ 'settings' table exists")
            
        # Try writing
        try:
            print("Testing write access...")
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('test_key', 'test_value')")
            conn.commit()
            print("✅ Write successful")
        except Exception as e:
            print(f"❌ Write failed: {e}")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    check_db()
