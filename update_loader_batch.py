import os
import re

old_loader = """    <div class="loader-content">
      <div class="loader-spinner"></div>
      <p class="loader-text">Oriana Academy</p>
    </div>"""

new_loader = """    <div class="loader-content">
      <div class="newtons-cradle">
        <div class="newtons-cradle__dot"></div>
        <div class="newtons-cradle__dot"></div>
        <div class="newtons-cradle__dot"></div>
        <div class="newtons-cradle__dot"></div>
      </div>
      <p class="loader-text">Oriana Academy</p>
    </div>"""

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_loader in content:
        new_content = content.replace(old_loader, new_loader)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")
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
