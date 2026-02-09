import os
import re

# Paths
base_dir = r"C:\Users\karth\.gemini\antigravity\scratch\oriana-academy"
courses_dir = os.path.join(base_dir, "courses")

# Hardcoded Hex Replacements
colors = {
    "#7C3AED": "#10B981", # Purple
    "#8B5CF6": "#34D399", # Light Purple
    "#6D28D9": "#059669", # Dark Purple
    "#EC4899": "#3B82F6", # Pink
    "#F472B6": "#60A5FA", # Light Pink
    "#764ba2": "#059669", # Hero Dark Purple
    "#667eea": "#10B981", # Hero Blue-Purple
    "#fa709a": "#10B981", # Sunset Pink
    "#fee140": "#3B82F6", # Sunset Yellow -> Blue
    "#1e1b4b": "#064e3b", # Very Dark Navy -> Dark Green
    "#312e81": "#065f46", # Dark Navy -> Darker Green
    "#4c1d95": "#047857", # Deep Purple -> Emerald
    "rgba(124, 58, 237": "rgba(16, 185, 129",
    "rgba(236, 72, 153": "rgba(59, 130, 246",
    "rgba(139, 92, 246": "rgba(52, 211, 153",
    "rgba(244, 114, 182": "rgba(96, 165, 250",
}

# Key Term Replacements
terms = {
    "purple": "green",
    "pink": "blue",
    "Purple": "Green",
    "Pink": "Blue",
}

def process_content(content):
    # 1. Bump CSS version
    content = re.sub(r'main\.css\?v=[0-9\.]+', 'main.css?v=1.5', content)
    content = re.sub(r'main\.css(?!\?v=)', 'main.css?v=1.5', content)
    
    # 2. Hex and RGBA replacements
    for old, new in colors.items():
        content = content.replace(old, new)
        content = content.replace(old.lower(), new)
    
    # 3. Term replacements (for classes and labels)
    for old, new in terms.items():
        # Avoid replacing things inside URLs or image names if possible, 
        # but here we want to catch section-purple-light -> section-green-light
        content = content.replace(old, new)
        
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = process_content(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Process all files recursively
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith((".html", ".css", ".js")):
            process_file(os.path.join(root, file))

print("Aggressive total theme update complete.")
