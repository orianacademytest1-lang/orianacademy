import os
import re

base_dir = r"C:\Users\karth\.gemini\antigravity\scratch\oriana-academy"

# Map the SVG content (or identifiers) to the new 3D image tags
# We'll use regex to find the SVGs within their containers

replacements = [
    # Stats Items
    (r'<div class="stat-icon"><svg[^>]*>.*?</svg></div>(?=\s*<span class="stat-number"[^>]*>.*?(?:95%|Placement Rate))', 
     '<div class="stat-icon"><img src="assets/images/icons/icon-growth.png" alt="Placement Rate"></div>'),
    
    (r'<div class="stat-icon"><svg[^>]*>.*?</svg></div>(?=\s*<span class="stat-number"[^>]*>.*?(?:50\+|Hiring Partners))', 
     '<div class="stat-icon"><img src="assets/images/icons/icon-partners.png" alt="Hiring Partners"></div>'),
    
    (r'<div class="stat-icon"><svg[^>]*>.*?</svg></div>(?=\s*<span class="stat-number"[^>]*>.*?(?:5,000\+|Students Trained))', 
     '<div class="stat-icon"><img src="assets/images/icons/icon-students.png" alt="Students Trained"></div>'),
    
    (r'<div class="stat-icon"><svg[^>]*>.*?</svg></div>(?=\s*<span class="stat-number"[^>]*>.*?(?:15\+|Expert Trainers))', 
     '<div class="stat-icon"><img src="assets/images/icons/icon-trainers.png" alt="Expert Trainers"></div>'),

    # Contact Info (stat-icon variant in contact.html)
    (r'<div class="stat-icon" style="[^"]*background: linear-gradient\(135deg, #3B82F6, #60A5FA\);[^"]*"><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>',
     '<div class="stat-icon"><img src="assets/images/icons/icon-location.png" alt="Location"></div>'),
    
    (r'<div class="stat-icon" style="[^"]*background: linear-gradient\(135deg, #10B981, #34D399\);[^"]*"><svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div>',
     '<div class="stat-icon"><img src="assets/images/icons/icon-phone.png" alt="Phone"></div>'),
    
    (r'<div class="stat-icon" style="[^"]*background: linear-gradient\(135deg, #10B981, #34D399\);[^"]*"><svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>',
     '<div class="stat-icon"><img src="assets/images/icons/icon-email.png" alt="Email"></div>'),

    # Feature Cards
    (r'<div class="feature-icon"><svg[^>]*>.*?</svg></div>(?=\s*<h3>Industry-Focused</h3>)', 
     '<div class="feature-icon"><img src="assets/images/icons/icon-growth.png" alt="Industry Focused"></div>'),
    
    (r'<div class="feature-icon"><svg[^>]*>.*?</svg></div>(?=\s*<h3>Expert Trainers</h3>)', 
     '<div class="feature-icon"><img src="assets/images/icons/icon-trainers.png" alt="Expert Trainers"></div>'),
    
    (r'<div class="feature-icon"><svg[^>]*>.*?</svg></div>(?=\s*<h3>Flexible Learning</h3>)', 
     '<div class="feature-icon"><img src="assets/images/icons/icon-laptop.png" alt="Flexible Learning"></div>'),
    
    (r'<div class="feature-icon"><svg[^>]*>.*?</svg></div>(?=\s*<h3>Job Assistance</h3>)', 
     '<div class="feature-icon"><img src="assets/images/icons/icon-rocket.png" alt="Job Assistance"></div>'),

    # Floating Icons (Generic replacements)
    (r'<div class="float-icon[^"]*"><svg[^>]*>.*?</svg></div>', 
     lambda m: '<div class="float-icon ' + (' '.join(m.group(0).split('float-icon')[1].split('>')[0].strip().replace('"', '').split())) + '"><img src="assets/images/icons/icon-rocket.png" alt="Decorative Icon"></div>'),
]

# Quick and dirty approach for float icons since they are decorative
# We'll just replace them with a few chosen 3D icons

float_icons = [
    'icon-rocket.png',
    'icon-growth.png',
    'icon-students.png',
    'icon-laptop.png'
]
float_idx = 0

def process_content(content):
    global float_idx
    # Specific replacements
    for pattern, replacement in replacements:
        if callable(replacement):
             content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        else:
             content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Final sweep for any remaining SVGs in float-icon that weren't caught
    def float_repl(m):
        global float_idx
        icon = float_icons[float_idx % len(float_icons)]
        float_idx += 1
        classes = m.group(1) or ""
        return f'<div class="float-icon {classes}"><img src="assets/images/icons/{icon}" alt="Icon"></div>'

    content = re.sub(r'<div class="float-icon\s+([^"]*)"><svg[^>]*>.*?</svg></div>', float_repl, content, flags=re.DOTALL)
    
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = process_content(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            process_file(os.path.join(root, file))

print("Premium AI Icon integration complete.")
