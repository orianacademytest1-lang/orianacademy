"""
Script to standardize remaining course pages with modern design
"""

# Footer replacement content (same for all pages)
HOMEPAGE_FOOTER = '''    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="../index.html" class="footer-logo">
                        <img src="../assets/images/oriana-logo-cropped.png" alt="Oriana Academy" class="logo-img filter-invert">
                    </a>
                    <p>Oriana Academy is India's leading IT training institute offering cutting-edge courses in Data Science,
                        Machine Learning, Digital Marketing, and more. Join us to unlock your potential.</p>
                    <div class="footer-social">
                        <a href="#" class="social-icon">f</a>
                        <a href="#" class="social-icon">in</a>
                        <a href="#" class="social-icon">X</a>
                        <a href="#" class="social-icon">▶</a>
                    </div>
                </div>

                <div class="footer-section">
                    <h4>Programs</h4>
                    <ul>
                        <li><a href="digital-marketing.html">Digital Marketing</a></li>
                        <li><a href="data-science.html">Data Science</a></li>
                        <li><a href="machine-learning.html">Machine Learning</a></li>
                        <li><a href="python.html">Python Programming</a></li>
                        <li><a href="generative-ai.html">Generative AI</a></li>
                    </ul>
                </div>

                <div class="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="../about.html">About Us</a></li>
                        <li><a href="../career-guidance.html">Career Guidance</a></li>
                        <li><a href="#">Partnerships</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Careers</a></li>
                    </ul>
                </div>

                <div class="footer-section">
                    <h4>Contact Us</h4>
                    <ul class="footer-contact">
                        <li>📍 123 Tech Park, Bangalore, India</li>
                        <li>📞 +91 98765 43210</li>
                        <li>📧 info@orianaacademy.com</li>
                    </ul>
                    <div class="footer-newsletter">
                        <h4>Newsletter</h4>
                        <form class="newsletter-form">
                            <input type="email" placeholder="Your email address">
                            <button type="submit">→</button>
                        </form>
                    </div>
                </div>
            </div>

            <div class="footer-bottom">
                <p>© 2026 Oriana Academy. All rights reserved. | <a href="#">Privacy Policy</a>
                    | <a href="#">Terms of Service</a></p>
            </div>
        </div>
    </footer>'''

import re
import os

def update_course_page_footer(filepath):
    """Update footer in course page to match homepage"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find footer section and replace
    footer_pattern = r'<!-- FOOTER -->.*?</footer>'
    if re.search(footer_pattern, content, re.DOTALL):
        content = re.sub(footer_pattern, HOMEPAGE_FOOTER, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Update all course pages
course_dir = r'c:\Users\karth\.gemini\antigravity\scratch\oriana-academy\courses'
courses = ['machine-learning.html', 'python.html', 'generative-ai.html', 'java.html', 'data-analytics.html', 'hr-training.html']

for course in courses:
    filepath = os.path.join(course_dir, course)
    if os.path.exists(filepath):
        success = update_course_page_footer(filepath)
        print(f"{'✓' if success else '✗'} Updated {course}")
    else:
        print(f"✗ File not found: {course}")

print("\nFooter updates complete!")
