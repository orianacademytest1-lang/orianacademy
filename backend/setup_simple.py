"""
Simplified setup script to populate vector database
"""
import os
import sys
from vector_store import get_vector_store
import google.generativeai as genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

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
    
    return text[:2000]  # Limit to 2000 chars per file

def generate_embedding(text):
    """Generate embedding using Gemini"""
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"  ⚠️ Embedding error: {e}")
        return None

def setup_simple():
    """Simple setup - just load course files"""
    print("=" * 60)
    print("🔧 SIMPLIFIED DATABASE SETUP")
    print("=" * 60)
    
    # Get courses directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    courses_dir = os.path.join(os.path.dirname(backend_dir), 'courses')
    
    print(f"\n📁 Courses directory: {courses_dir}")
    
    if not os.path.exists(courses_dir):
        print(f"❌ Directory not found!")
        return
    
    # Get HTML files
    html_files = [f for f in os.listdir(courses_dir) if f.endswith('.html')]
    print(f"📚 Found {len(html_files)} course files\n")
    
    # Initialize vector store
    print("💾 Initializing vector store...")
    vector_store = get_vector_store()
    
    # Check existing data
    current_count = vector_store.get_collection_count()
    if current_count > 0:
        print(f"⚠️  Vector store already has {current_count} documents")
        response = input("Reset and reload? (yes/no): ")
        if response.lower() == 'yes':
            vector_store.reset()
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
            
            if not text:
                print(f"  ⚠️ No text extracted, skipping")
                continue
            
            # Generate embedding
            print(f"  Generating embedding...")
            embedding = generate_embedding(text)
            
            if embedding is None:
                print(f"  ⚠️ Embedding failed, skipping")
                continue
            
            # Add to lists
            documents.append(f"{course_name}: {text}")
            embeddings.append(embedding)
            metadatas.append({
                'course': course_name,
                'source_file': filename,
                'section': 'overview'
            })
            ids.append(f"{course_name}_0")
            
            print(f"  ✅ Added successfully")
            
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
            print(f"🚀 Start API: python app.py")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error adding to vector store: {e}")
    else:
        print("\n❌ No documents processed!")

if __name__ == "__main__":
    setup_simple()
