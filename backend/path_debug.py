import os
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
index_path = os.path.join(project_root, "index.html")

print(f"DEBUG: backend_dir = {backend_dir}")
print(f"DEBUG: project_root = {project_root}")
print(f"DEBUG: index_path = {index_path}")
print(f"DEBUG: index_exists = {os.path.exists(index_path)}")
print(f"DEBUG: current_files = {os.listdir(project_root)}")
