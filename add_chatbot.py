"""
Add chatbot to all pages
"""
import os
import re

# Directory containing HTML files
project_root = r'c:\Users\karth\.gemini\antigravity\scratch\oriana-academy'
courses_dir = os.path.join(project_root, 'courses')

# Chatbot includes to add before </body>
CHATBOT_INCLUDES = '''    <!-- AI Chatbot -->
    <link rel="stylesheet" href="../css/chatbot.css">
    <script src="../js/chatbot.js"></script>
'''

CHATBOT_INCLUDES_ROOT = '''    <!-- AI Chatbot -->
    <link rel="stylesheet" href="css/chatbot.css">
    <script src="js/chatbot.js"></script>
'''

def add_chatbot_to_file(filepath, is_root=False):
    """Add chatbot includes to HTML file if not already present"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if chatbot already added
    if 'chatbot.css' in content or 'chatbot.js' in content:
        print(f"  ✓ Chatbot already in: {os.path.basename(filepath)}")
        return False
    
    # Choose correct includes based on location
    includes = CHATBOT_INCLUDES_ROOT if is_root else CHATBOT_INCLUDES
    
    # Add before </body> tag
    if '</body>' in content:
        content = content.replace('</body>', f'{includes}</body>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Added chatbot to: {os.path.basename(filepath)}")
        return True
    else:
        print(f"  ⚠ No </body> tag in: {os.path.basename(filepath)}")
        return False

# Process root HTML files
print("Adding chatbot to root pages...")
root_files = ['index.html', 'about.html', 'contact.html', 'career-guidance.html']
for filename in root_files:
    filepath = os.path.join(project_root, filename)
    if os.path.exists(filepath):
        add_chatbot_to_file(filepath, is_root=True)

# Process course pages
print("\nAdding chatbot to course pages...")
if os.path.exists(courses_dir):
    for filename in os.listdir(courses_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(courses_dir, filename)
            add_chatbot_to_file(filepath, is_root=False)

print("\n✨ Chatbot integration complete!")
