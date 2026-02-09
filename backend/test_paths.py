"""
Simple test script to debug path issues
"""
import os

# Get current directory
print(f"Current directory: {os.getcwd()}")

# Check backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Backend dir: {backend_dir}")

# Check parent directory
parent_dir = os.path.dirname(backend_dir)
print(f"Parent dir: {parent_dir}")

# Check courses directory
courses_dir = os.path.join(parent_dir, 'courses')
print(f"Courses dir: {courses_dir}")
print(f"Courses dir exists: {os.path.exists(courses_dir)}")

# List files if exists
if os.path.exists(courses_dir):
    files = os.listdir(courses_dir)
    html_files = [f for f in files if f.endswith('.html')]
    print(f"\nFound {len(html_files)} HTML files:")
    for f in html_files:
        print(f"  - {f}")
else:
    print("\n❌ Courses directory not found!")
    
    # Try to find it
    print("\nSearching for courses directory...")
    for root, dirs, files in os.walk(parent_dir):
        if 'courses' in dirs:
            found_courses = os.path.join(root, 'courses')
            print(f"Found courses at: {found_courses}")
            html_count = len([f for f in os.listdir(found_courses) if f.endswith('.html')])
            print(f"  Contains {html_count} HTML files")
