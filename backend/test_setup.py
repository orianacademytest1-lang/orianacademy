
import os
import sys
# Add parent dir to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_store import get_vector_store
from data_processor import DataProcessor

def test():
    print("Testing setup...")
    dp = DataProcessor()
    vs = get_vector_store()
    
    # Check if courses dir exists
    courses_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "courses")
    if not os.path.exists(courses_dir):
        print(f"Error: {courses_dir} not found")
        return

    # Use first html file
    html_files = [f for f in os.listdir(courses_dir) if f.endswith(".html")]
    if not html_files:
        print("No html files found")
        return
    
    filename = html_files[0]
    html_path = os.path.join(courses_dir, filename)
    print(f"Processing {filename}...")
    
    data = dp.extract_course_content(html_path)
    chunks = dp.chunk_content(data, filename.replace(".html", ""), filename)
    print(f"Created {len(chunks)} chunks")
    
    docs = [c["text"] for c in chunks]
    print("Generating embeddings...")
    embeds = [dp.generate_embedding(c["text"]) for c in chunks]
    metas = [c["metadata"] for c in chunks]
    ids = [f"test_{filename}_{i}" for i in range(len(chunks))]
    
    print("Adding to vector store...")
    vs.add_documents(
        documents=docs,
        embeddings=embeds,
        metadatas=metas,
        ids=ids
    )
    
    count = vs.get_collection_count()
    print(f"DONE! Count is now: {count}")

if __name__ == "__main__":
    test()
