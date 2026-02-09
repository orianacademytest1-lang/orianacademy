import os

# Get paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(backend_dir)

print(f"Backend: {backend_dir}")
print(f"Root: {root_dir}")
print(f"\nAll files in root:")
for f in os.listdir(root_dir):
    full_path = os.path.join(root_dir, f)
    if os.path.isfile(full_path) and f.endswith('.html'):
        print(f"  ✅ {f}")

print(f"\nFiles found by os.walk:")
for root, dirs, files in os.walk(root_dir):
    print(f"\nDirectory: {root}")
    print(f"  Dirs: {dirs}")
    print(f"  HTML files: {[f for f in files if f.endswith('.html')]}")
    
    # Check skip logic
    skip_dirs = ['backend', '.gemini', 'node_modules', '__pycache__', '.git']
    if any(skip_dir in root for skip_dir in skip_dirs):
        print(f"  ⚠️  SKIPPED due to: {[s for s in skip_dirs if s in root]}")
