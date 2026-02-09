import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import get_smtp_settings, get_db_connection

def debug_setup():
    print("🔍 Checking SMTP Settings in Database...")
    try:
        settings = get_smtp_settings()
        print(f"SMTP Email: {settings.get('smtp_email')}")
        print(f"SMTP Password: {'*' * len(settings.get('smtp_password', '')) if settings.get('smtp_password') else 'MISSING'}")
        print(f"Receiver Email: {settings.get('receiver_email')}")
        
        if not all([settings.get('smtp_email'), settings.get('smtp_password'), settings.get('receiver_email')]):
            print("❌ Some SMTP settings are MISSING in the database.")
        else:
            print("✅ All SMTP settings found in database.")
            
        # Check raw table content
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM settings")
        rows = cursor.fetchall()
        print(f"\nRaw Settings Table ({len(rows)} rows):")
        for row in rows:
            print(f"- {row['key']}: {row['value'][:5]}...")
        conn.close()

    except Exception as e:
        print(f"❌ Error checking settings: {e}")

if __name__ == "__main__":
    debug_setup()
