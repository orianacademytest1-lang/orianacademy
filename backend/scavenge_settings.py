import re

db_path = 'oriana_data.db.bak'

def scavenge():
    with open(db_path, 'rb') as f:
        content = f.read()
    
    # Try to find common patterns in SQLite binary
    # Settings are usually stored as key, value pairs
    # In the binary they might look like: 
    # [key_string][value_string] or similar
    
    # Regex for Google App Password: 4 words of 4 letters separated by spaces
    # Or just 16 letters if spaces are stripped, but we saw spaces
    app_pw_pattern = b'[a-z]{4} [a-z]{4} [a-z]{4} [a-z]{4}'
    
    matches = re.findall(app_pw_pattern, content)
    if matches:
         print("\n--- Found Potential App Passwords ---")
         for m in matches:
             print(m.decode('utf-8'))
    else:
        print("No app password pattern found.")

if __name__ == "__main__":
    scavenge()
