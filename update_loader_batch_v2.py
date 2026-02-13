import os
import re

# More robust regex pattern
pattern = re.compile(r'(\s*)<div class="loader-spinner"></div>', re.DOTALL)

new_structure = r'''\1<div class="newtons-cradle">
\1    <div class="newtons-cradle__dot"></div>
\1    <div class="newtons-cradle__dot"></div>
\1    <div class="newtons-cradle__dot"></div>
\1    <div class="newtons-cradle__dot"></div>
\1</div>'''

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="loader-spinner"></div>' in content:
        new_content = pattern.sub(new_structure, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
    else:
        # Check if already updated
        if 'newtons-cradle' in content:
             print(f"Already updated: {file_path}")
        else:
             print(f"Skipped (not found): {file_path}")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Root HTML files
    for f in os.listdir(root_dir):
        if f.endswith('.html'):
            update_file(os.path.join(root_dir, f))
            
    # Courses directory
    courses_dir = os.path.join(root_dir, 'courses')
    if os.path.exists(courses_dir):
        for f in os.listdir(courses_dir):
            if f.endswith('.html'):
                update_file(os.path.join(courses_dir, f))

if __name__ == "__main__":
    main()
