import os
import re

def final_polish(directory='.'):
    version_pattern = re.compile(r'v=[0-9]+(\.[0-9]+)?')
    png_pattern = re.compile(r'\.png')
    
    # Specific known broken paths from my inspection
    BROKEN_MAP = {
        'data-science-3d.webp': 'data-science.webp',
        'data-analytics-3d.webp': 'data-analytics.webp',
        'machine-learning-3d.webp': 'machine-learning.webp',
        'generative-ai-3d.webp': 'generative-ai.webp',
        'digital-marketing-3d.webp': 'digital-marketing.webp',
        'python-3d.webp': 'python.webp',
        'java-3d.webp': 'java.webp',
    }

    count = 0
    for root, dirs, files in os.walk(directory):
        if any(skip in root for skip in ['.git', '.venv', 'chroma_db', '__pycache__']):
            continue
            
        for file in files:
            if file.lower().endswith(('.html', '.css', '.js')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    
                    # 1. Standardize versioning
                    new_content = version_pattern.sub('v=33.0', new_content)
                    
                    # 2. Ensure .webp
                    new_content = png_pattern.sub('.webp', new_content)
                    
                    # 3. Fix known broken image names (from legacy code)
                    for broken, fixed in BROKEN_MAP.items():
                        new_content = new_content.replace(broken, fixed)
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ Polished: {os.path.relpath(path, directory)}")
                        count += 1
                except Exception as e:
                    print(f"❌ Error on {file}: {e}")
                    
    print(f"✨ Total files polished: {count}")

if __name__ == "__main__":
    final_polish()
