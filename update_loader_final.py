import os
import re

new_loader = """
    <!-- PAGE LOADER -->
    <div class="page-loader" id="pageLoader">
        <div class="loader-content">
            <div class="newtons-cradle">
                <div class="newtons-cradle__dot"></div>
                <div class="newtons-cradle__dot"></div>
                <div class="newtons-cradle__dot"></div>
                <div class="newtons-cradle__dot"></div>
            </div>
            <p class="loader-text">Oriana Academy</p>
        </div>
    </div>
"""

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. If old structure exists, replace it
    if '<div class="loader-spinner"></div>' in content:
        # Simple replacement for known pattern
        pattern = re.compile(r'(\s*)<div class="loader-spinner"></div>', re.DOTALL)
        content = pattern.sub(r'''\1<div class="newtons-cradle">
\1    <div class="newtons-cradle__dot"></div>
\1    <div class="newtons-cradle__dot"></div>
\1    <div class="newtons-cradle__dot"></div>
\1    <div class="newtons-cradle__dot"></div>
\1</div>''', content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated (replaced): {file_path}")
        return

    # 2. If no loader at all, insert after <body>
    if 'page-loader' not in content:
        if '<body>' in content:
            new_content = content.replace('<body>', '<body>' + new_loader)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated (inserted): {file_path}")
        else:
            print(f"Skipped (no body): {file_path}")
    else:
        print(f"Already updated or has loader: {file_path}")

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
