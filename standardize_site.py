import os
import re

# Paths
base_dir = r"C:\Users\karth\.gemini\antigravity\scratch\oriana-academy"
courses_dir = os.path.join(base_dir, "courses")

# Color Replacements (Hex cases)
colors = {
    "#7C3AED": "#10B981", # Purple -> Green
    "#8B5CF6": "#34D399", # Light Purple -> Light Green
    "#6D28D9": "#059669", # Dark Purple -> Dark Green
    "#EC4899": "#3B82F6", # Pink -> Blue (Accent)
    "#F472B6": "#60A5FA", # Light Pink -> Light Blue
}

def standardize_header(html_content, is_course=False):
    # Regex to find the <header> block
    header_pattern = re.compile(r'<header.*?</header>', re.DOTALL)
    
    logo_path = "../assets/images/oriana-logo-cropped.png" if is_course else "assets/images/oriana-logo-cropped.png"
    index_link = "../index.html" if is_course else "index.html"
    about_link = "../about.html" if is_course else "about.html"
    career_link = "../career-guidance.html" if is_course else "career-guidance.html"
    contact_link = "../contact.html" if is_course else "contact.html"
    
    # We need to preserve the active class logic if it exists, but for now we'll just make them consistent
    # and maybe keep the current file as active if we can detect it.
    
    new_header = f"""<header class="header" id="header">
        <div class="container">
            <a href="{index_link}" class="logo">
                <img src="{logo_path}" alt="Oriana Academy" class="logo-img">
            </a>

            <nav>
                <ul class="nav-menu" id="navMenu">
                    <li><a href="{index_link}">Home</a></li>
                    <li><a href="{about_link}">About Us</a></li>
                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle">Courses</a>
                        <ul class="dropdown-menu">
                            <li><a href="{'courses/' if not is_course else ''}digital-marketing.html">Digital Marketing</a></li>
                            <li><a href="{'courses/' if not is_course else ''}machine-learning.html">Machine Learning</a></li>
                            <li><a href="{'courses/' if not is_course else ''}data-science.html">Data Science</a></li>
                            <li><a href="{'courses/' if not is_course else ''}data-analytics.html">Data Analytics</a></li>
                            <li><a href="{'courses/' if not is_course else ''}java.html">Java Training</a></li>
                            <li><a href="{'courses/' if not is_course else ''}python.html">Python Programming</a></li>
                            <li><a href="{'courses/' if not is_course else ''}generative-ai.html">Generative AI</a></li>
                            <li><a href="{'courses/' if not is_course else ''}hr-training.html">HR Training</a></li>
                        </ul>
                    </li>
                    <li><a href="{career_link}">Career Guidance</a></li>
                    <li><a href="{contact_link}">Contact</a></li>
                </ul>
            </nav>

            <a href="{contact_link}" class="cta-btn">Enroll Now</a>

            <button class="mobile-toggle" id="mobileToggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>"""
    
    return header_pattern.sub(new_header, html_content)

def process_file(filepath, is_course=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Standardize Header
    content = standardize_header(content, is_course)
    
    # 2. Update CSS version for cache busting
    content = content.replace('css/main.css', 'css/main.css?v=1.3')
    
    # 3. Color replacements
    for old, new in colors.items():
        content = re.sub(re.escape(old), new, content, flags=re.IGNORECASE)
    
    # 4. Special case for pink-purple gradients that might be hardcoded as names or variables
    # (Though we mostly targeted hex)
    
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

print("Standardization and Theme update complete.")
