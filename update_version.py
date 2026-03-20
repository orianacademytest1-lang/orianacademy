import os
import glob

def update_html_files():
    html_files = glob.glob('**/*.html', recursive=True)
    count = 0
    for f in html_files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Safe replacement to avoid double versioning if already present
            new_content = content.replace('js/chatbot.js', 'js/chatbot.js?v=2.1')
            new_content = new_content.replace('css/chatbot.css', 'css/chatbot.css?v=2.1')
            
            # Clean up double versioning if any (e.g., .js?v=2.1?v=2.1)
            new_content = new_content.replace('?v=2.1?v=2.1', '?v=2.1')
            new_content = new_content.replace('?v=2.0?v=2.1', '?v=2.1')
            
            if content != new_content:
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                count += 1
        except Exception as e:
            print(f"Error processing {f}: {e}")
    print(f"Updated {count} files.")

if __name__ == "__main__":
    update_html_files()
