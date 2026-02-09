import os
import re

base_dir = r"C:\Users\karth\.gemini\antigravity\scratch\oriana-academy"

# Mapping of course filename to its 3D illustration
course_illustrations = {
    # Courses (inside courses/)
    "digital-marketing.html": "digital-marketing-3d.png",
    "data-science.html": "data-science-3d.png",
    "data-analytics.html": "data-science-3d.png",
    "machine-learning.html": "machine-learning-3d.png",
    "generative-ai.html": "generative-ai-3d.png",
    "java.html": "coding-training-3d.png",
    "python.html": "coding-training-3d.png",
    "hr-training.html": "hr-training-3d.png",
    # Root pages
    "about.html": "icon-partners.png",
    "contact.html": "icon-location.png",
    "career-guidance.html": "icon-rocket.png"
}

def redesign_page(filepath):
    filename = os.path.basename(filepath)
    is_in_courses = "courses" in filepath
    assets_prefix = "../assets" if is_in_courses else "assets"
    link_prefix = "../" if is_in_courses else ""
    
    illustration = course_illustrations.get(filename, "icon-rocket.png")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Header Logo (Ensure it uses the right class and no inline height)
    logo_pattern = r'<a href="[^"]*" class="logo">.*?</a>'
    new_logo = f'''<a href="{link_prefix}index.html" class="logo">
                <img src="{assets_prefix}/images/oriana-logo-cropped.png" alt="Oriana Academy" class="logo-img">
            </a>'''
    # We use a more careful replacement here to find the logo inside header
    content = re.sub(r'<header class="header".*?<a href="[^"]*" class="logo">.*?</a>', 
                     f'<header class="header" id="header"><div class="container">{new_logo}', 
                     content, flags=re.DOTALL)
    # Note: The above is a bit aggressive, let's just target the logo img directly if it has style
    content = re.sub(r'<a href="[^"]*" class="logo">\s*<img[^>]*style="[^"]*"[^>]*>', 
                     new_logo, content)

    # 2. Update Hero Section (Robust version)
    # Matches any section with class hero, page-hero, or section-green-dark
    # Regardless of whether there's a comment before it.
    hero_pattern = r'(<!-- (?:COURSE|PAGE|PREMIUM) HERO -->\s*)?<section class="(?:hero|page-hero|section-green-dark)"[^>]*>.*?</section>'
    
    # Extract title and p from the *content we have left*
    title_match = re.search(r'<h1>(.*?)</h1>', content)
    p_match = re.search(r'</h1>\s*<p>(.*?)</p>', content)
    
    title = title_match.group(1) if title_match else "Oriana Academy"
    p_text = p_match.group(1) if p_match else "Launch your dream career with India's #1 IT training institute."
    # Remove any tags from p_text if any
    p_text = re.sub('<[^<]+?>', '', p_text)

    new_hero = f'''
  <!-- PREMIUM HERO -->
  <section class="section-green-dark" style="padding: 10rem 0 6rem; min-height: 80vh; display: flex; align-items: center;">
    <div class="container" style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 4rem; align-items: center;">
      <!-- Floating elements -->
      <div class="float-circle blue size-lg float-top-right delay-1"></div>
      <div class="float-circle green size-sm float-bottom-left delay-2"></div>
      <div class="float-icon float-top-left delay-3"><img src="{assets_prefix}/images/icons/icon-rocket.png" alt="Icon"></div>
      
      <div class="hero-content reveal">
        <span class="hero-badge" style="background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2);">
          <img src="{assets_prefix}/images/icons/icon-growth.png" style="width: 20px; height: 20px; margin-right: 8px;"> Professional Excellence
        </span>
        <h1 style="color: #fff; font-size: clamp(2.5rem, 5vw, 3.5rem); margin-bottom: 1.5rem;">{title}</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.25rem; margin-bottom: 2.5rem; max-width: 600px;">{p_text}</p>
        <div class="hero-buttons">
          <a href="{link_prefix}contact.html" class="cta-btn" style="padding: 1rem 2.5rem; font-size: 1.1rem; background: #fff; color: var(--primary);">Get Started</a>
          <a href="{link_prefix}index.html#courses" class="btn btn-outline" style="border-color: #fff; color: #fff; margin-left: 1rem; padding: 1rem 2.5rem;">Explore Programs</a>
        </div>
      </div>
      
      <div class="hero-image reveal" style="position: relative;">
        <div style="background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%); position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 120%; height: 120%; z-index: -1;"></div>
        <img src="{assets_prefix}/images/{illustration}" alt="{title}" style="width: 100%; filter: drop-shadow(0 20px 50px rgba(0,0,0,0.3)); animation: floatShape 8s ease-in-out infinite;">
      </div>
    </div>
  </section>
'''
    content = re.sub(hero_pattern, new_hero, content, count=1, flags=re.DOTALL)

    # 3. Fix Sections
    # Only replace plain section if it looks like the first one
    if '<section class="section section-mesh">' not in content:
        content = content.replace('<section class="section">', '<section class="section section-mesh">', 1)
    
    # 4. Enhance Curriculum/Features lists on course pages
    if is_in_courses:
        # Avoid double wrapping
        if 'style="background: rgba(255,255,255,0.7)' not in content:
            content = re.sub(r'<div class="reveal">\s*<h3>(.*?)</h3>\s*<ul class="curriculum-list">', 
                             r'<div class="card reveal" style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); padding: 2.5rem; border-radius: 2rem; box-shadow: var(--shadow-xl); height: 100%;">\n<h3 style="color: var(--primary); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 10px;">\1</h3>\n<ul class="curriculum-list">', 
                             content)

    # 5. Add Course Features section if it doesn't exist
    if is_in_courses and "<!-- COURSE FEATURES -->" not in content:
        features_section = f'''
  <!-- COURSE FEATURES -->
  <section class="section section-green-light">
    <div class="container">
      <div class="section-header reveal">
        <h2 class="text-gradient">Why Choose This Program?</h2>
        <p>Experience a learning journey designed for excellence</p>
      </div>
      
      <div class="grid-4">
        <div class="feature-card reveal stagger-1">
          <div class="feature-icon"><img src="{assets_prefix}/images/icons/icon-growth.png" alt="Growth"></div>
          <h3>Industry Curriculum</h3>
          <p>Learn tools and strategies that are actually used by top tech companies today.</p>
        </div>
        <div class="feature-card reveal stagger-2">
          <div class="feature-icon"><img src="{assets_prefix}/images/icons/icon-trainers.png" alt="Mentorship"></div>
          <h3>Expert Mentors</h3>
          <p>Get guided by professionals who have worked at Google, Amazon, and Microsoft.</p>
        </div>
        <div class="feature-card reveal stagger-3">
          <div class="feature-icon"><img src="{assets_prefix}/images/icons/icon-laptop.png" alt="Projects"></div>
          <h3>Real-world Projects</h3>
          <p>Build a portfolio of live projects that demonstrate your skills to employers.</p>
        </div>
        <div class="feature-card reveal stagger-4">
          <div class="feature-icon"><img src="{assets_prefix}/images/icons/icon-rocket.png" alt="Placement"></div>
          <h3>Job Assistance</h3>
          <p>Comprehensive placement support including mock interviews and resume building.</p>
        </div>
      </div>
    </div>
  </section>
'''
        if '<!-- FAQ SECTION -->' in content:
            content = content.replace('<!-- FAQ SECTION -->', features_section + '\n  <!-- FAQ SECTION -->')
        elif '<!-- FOOTER -->' in content:
             content = content.replace('<!-- FOOTER -->', features_section + '\n  <!-- FOOTER -->')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Process course files
courses_dir = os.path.join(base_dir, "courses")
for file in os.listdir(courses_dir):
    if file.endswith(".html"):
        redesign_page(os.path.join(courses_dir, file))

# Process root pages
for page in ["about.html", "contact.html", "career-guidance.html"]:
    filepath = os.path.join(base_dir, page)
    if os.path.exists(filepath):
        redesign_page(filepath)

print("Global redesign complete.")
