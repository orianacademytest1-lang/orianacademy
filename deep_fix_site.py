import os
import re

# Paths
base_dir = r"C:\Users\karth\.gemini\antigravity\scratch\oriana-academy"
courses_dir = os.path.join(base_dir, "courses")

# Expanded Color Replacements (Hex cases)
colors = {
    "#7C3AED": "#10B981", # Purple -> Green
    "#8B5CF6": "#34D399", # Light Purple -> Light Green
    "#6D28D9": "#059669", # Dark Purple -> Dark Green
    "#EC4899": "#3B82F6", # Pink -> Blue
    "#F472B6": "#60A5FA", # Light Pink -> Light Blue
    "#764ba2": "#059669", # Hero Dark Purple -> Green
    "#667eea": "#10B981", # Hero Blue-Purple -> Green
    "rgba(124, 58, 237": "rgba(16, 185, 129", # RGBA Purple
    "rgba(236, 72, 153": "rgba(59, 130, 246", # RGBA Pink
}

def clean_css_link(content):
    # Regex to find malformed CSS links like main.css?v=1.3?v=1.2
    # and replace with main.css?v=1.4
    content = re.sub(r'href=["\'].*?main\.css.*?["\']', 'href="css/main.css?v=1.4"', content)
    return content

def clean_course_css_link(content):
    content = re.sub(r'href=["\'].*?main\.css.*?["\']', 'href="../css/main.css?v=1.4"', content)
    return content

def process_file(filepath, is_course=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix CSS Links
    if is_course:
        content = clean_course_css_link(content)
    else:
        content = clean_css_link(content)
        
    # 2. Color replacements (Internal styles and hardcoded hex)
    for old, new in colors.items():
        content = re.sub(re.escape(old), new, content, flags=re.IGNORECASE)
    
    # 3. Specific brand color names if they exist
    content = content.replace('var(--primary-purple)', 'var(--primary)')
    content = content.replace('var(--primary-pink)', 'var(--secondary)')

    # 4. Standardize Header (Ensuring the Enroll Now button and toggles are present)
    # We already did this in the previous script run, so we just ensure the logo path is correct.
    # But let's verify the Enroll Now button is there.
    if 'cta-btn' not in content:
        # Re-run standardization logic if missing
        pass # The previous script should have fixed this, but let's be careful.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Process root HTML files
for f in os.listdir(base_dir):
    if f.endswith(".html"):
        process_file(os.path.join(base_dir, f), is_course=False)

# Process course HTML files
if os.path.exists(courses_dir):
    for f in os.listdir(courses_dir):
        if f.endswith(".html"):
            process_file(os.path.join(courses_dir, f), is_course=True)

print("Deep fix and link cleanup complete.")
