"""
Setup with local embeddings (no API quota limits)
Uses sentence-transformers for local embedding generation
"""
import os
from vector_store import get_vector_store
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer

def extract_text_from_html(file_path):
    """Extract main text content from HTML"""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text[:2000]  # Limit to 2000 chars

def setup_with_local_embeddings():
    """Setup using local sentence-transformers model"""
    print("=" * 60)
    print("🔧 DATABASE SETUP - LOCAL EMBEDDINGS")
    print("=" * 60)
    
    # Get courses directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    courses_dir = os.path.join(os.path.dirname(backend_dir), 'courses')
    
    print(f"\n📁 Courses directory: {courses_dir}")
    
    html_files = [f for f in os.listdir(courses_dir) if f.endswith('.html')]
    print(f"📚 Found {len(html_files)} course files\n")
    
    # Load local embedding model
    print("🤖 Loading local embedding model (this may take a minute)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, lightweight model
    print("✅ Model loaded!\n")
    
    # Initialize vector store
    vector_store = get_vector_store()
    
    # Check existing data
    current_count = vector_store.get_collection_count()
    if current_count > 0:
        print(f"⚠️  Vector store already has {current_count} documents")
        response = input("Reset and reload? (yes/no): ")
        if response.lower() != 'yes':
            print("Keeping existing data. Exiting.")
            return
        vector_store.reset()
        from vector_store import reset_vector_store
        reset_vector_store()
        vector_store = get_vector_store()

    
    # Process files
    documents = []
    embeddings = []
    metadatas = []
    ids = []
    
    for idx, filename in enumerate(html_files):
        course_name = filename.replace('.html', '')
        file_path = os.path.join(courses_dir, filename)
        
        print(f"{idx+1}/{len(html_files)} Processing: {course_name}")
        
        try:
            # Extract text
            text = extract_text_from_html(file_path)
            
            if not text or len(text) < 50:
                print(f"  ⚠️ Insufficient text, skipping")
                continue
            
            # Generate embedding locally (no API call!)
            embedding = model.encode(text).tolist()
            
            # Add to lists
            doc_text = f"{course_name.replace('-', ' ').title()}: {text}"
            documents.append(doc_text)
            embeddings.append(embedding)
            metadatas.append({
                'course': course_name,
                'source_file': filename,
                'section': 'overview'
            })
            ids.append(f"{course_name}_0")
            
            print(f"  ✅ Embedded: {len(text)} chars")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue
    
    # Add to vector store
    if documents:
        print(f"\n💾 Adding {len(documents)} documents to vector store...")
        try:
            vector_store.add_documents(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            final_count = vector_store.get_collection_count()
            print(f"\n" + "=" * 60)
            print(f"✅ SETUP COMPLETE!")
            print(f"📊 Total documents: {final_count}")
            print(f"\n🚀 Next steps:")
            print(f"   1. Start API: python app_local.py")
            print(f"   2. Test: http://localhost:5000/api/health")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error adding to vector store: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ No documents processed!")

if __name__ == "__main__":
    setup_with_local_embeddings()
