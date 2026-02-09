import os
import re

COURSES_DIR = r'c:\Users\karth\.gemini\antigravity\scratch\Oriana_Mark2\courses'
NEW_FOOTER = '''    <!-- FOOTER -->
    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="../index.html" class="logo">
                        <img src="../assets/images/oriana-logo-cropped.png" alt="Oriana Academy" class="logo-img">
                    </a>
                    <p>Oriana Academy is India's leading IT training institute offering cutting-edge courses in Data
                        Science,
                        Generative AI, Digital Marketing, and more. Join us to unlock your potential.</p>
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
                        <li><a href="machine-learning.html">Machine Learning Pro</a></li>
                        <li><a href="data-science.html">Data Science</a></li>
                        <li><a href="generative-ai.html">Generative AI</a></li>
                        <li><a href="data-analytics.html">Data Analyst</a></li>
                        <li><a href="java.html">Full Stack Java Development</a></li>
                        <li><a href="python.html">Full Stack Python Development</a></li>
                        <li><a href="software-testing.html">Software Testing</a></li>
                        <li><a href="digital-marketing.html">Digital Marketing</a></li>
                    </ul>
                </div>

                <div class="footer-section">
                    <h4>Company</h4>
                    <ul>
                        <li><a href="../about.html">About Us</a></li>
                        <li><a href="../pet-program.html">PET Program</a></li>
                        <li><a href="../career-guidance.html">Career Guidance</a></li>
                        <li><a href="#">Partnerships</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="../careers.html">Careers</a></li>
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

def update_footer(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find footer and replace it
    # We look for <footer class="footer"> ... </footer>
    updated_content = re.sub(r'<footer class="footer">.*?</footer>', NEW_FOOTER, content, flags=re.DOTALL)
    
    # Also clean up duplicate <!-- FOOTER --> comments if any
    updated_content = re.sub(r'<!-- FOOTER -->\s*<!-- FOOTER -->', '<!-- FOOTER -->', updated_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Updated {os.path.basename(file_path)}")

if __name__ == "__main__":
    for filename in os.listdir(COURSES_DIR):
        if filename.endswith('.html'):
            update_footer(os.path.join(COURSES_DIR, filename))
