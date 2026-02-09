"""
Comprehensive Website Content Extractor
Extracts and chunks content from ALL pages of Oriana Academy website
"""
import os
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer

class ComprehensiveExtractor:
    def __init__(self):
        """Initialize the comprehensive content extractor"""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.processed_pages = []
    
    def extract_section(self, soup, section_class_or_id, section_name):
        """Extract content from a specific section"""
        # Try by class
        section = soup.find('section', class_=section_class_or_id)
        if not section:
            # Try by ID
            section = soup.find(id=section_class_or_id)
        
        if not section:
            return None
        
        # Get all text
        text = section.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return {
            'text': text,
            'section_name': section_name
        }
    
    def extract_all_content(self, html_path, page_name):
        """Extract ALL content from an HTML page"""
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Remove script, style, nav, footer noise
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        
        chunks = []
        
        # 1. Extract page title and meta description
        title = soup.find('title')
        if title:
            chunks.append({
                'text': f"Page: {title.get_text(strip=True)}",
                'section': 'title',
                'page': page_name
            })
        
        # 2. Extract hero section
        hero = soup.find('section', class_='hero')
        if hero:
            hero_text = hero.get_text(separator=' ', strip=True)
            hero_text = ' '.join(hero_text.split())
            if len(hero_text) > 50:
                chunks.append({
                    'text': f"{page_name} - Hero: {hero_text}",
                    'section': 'hero',
                    'page': page_name
                })
        
        # 3. Extract all sections
        sections = soup.find_all('section')
        for idx, section in enumerate(sections):
            # Get section class or ID for identification
            section_id = section.get('class', [''])[0] or section.get('id', f'section_{idx}')
            
            # Get section title (h2, h3)
            section_title = section.find(['h2', 'h3'])
            title_text = section_title.get_text(strip=True) if section_title else f"Section {idx}"
            
            # Get section content
            content = section.get_text(separator=' ', strip=True)
            content = ' '.join(content.split())
            
            if len(content) > 100:  # Only add substantial sections
                chunks.append({
                    'text': f"{page_name} - {title_text}: {content}",
                    'section': str(section_id),
                    'page': page_name
                })
        
        # 4. Extract curriculum/feature cards
        cards = soup.find_all('div', class_=['curriculum-card', 'feature-card', 'card'])
        for idx, card in enumerate(cards):
            card_text = card.get_text(separator=' ', strip=True)
            card_text = ' '.join(card_text.split())
            if len(card_text) > 30:
                chunks.append({
                    'text': f"{page_name} - Card: {card_text}",
                    'section': 'cards',
                    'page': page_name
                })
        
        # 5. Extract info pills (duration, certification, etc.)
        info_pills = soup.find_all('div', class_='info-pill')
        if info_pills:
            info_text = ' | '.join([pill.get_text(strip=True) for pill in info_pills])
            chunks.append({
                'text': f"{page_name} - Info: {info_text}",
                'section': 'info',
                'page': page_name
            })
        
        # 6. Extract lists (ul, ol)
        lists = soup.find_all(['ul', 'ol'])
        for idx, list_elem in enumerate(lists):
            # Skip navigation lists
            if list_elem.find_parent('nav') or list_elem.find_parent('footer'):
                continue
            
            list_text = list_elem.get_text(separator=' | ', strip=True)
            if len(list_text) > 30:
                chunks.append({
                    'text': f"{page_name} - List: {list_text}",
                    'section': 'list',
                    'page': page_name
                })
        
        return chunks
    
    def process_entire_website(self, root_dir):
        """Process ALL HTML files in the website"""
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        print(f"📂 Scanning directory: {root_dir}")
        
        # Find all HTML files recursively
        html_files = []
        for root, dirs, files in os.walk(root_dir):
            # Get directory name (not full path)
            dir_name = os.path.basename(root)
            
            # Skip certain directory NAMES
            skip_dirs = ['backend', 'node_modules', '__pycache__', '.git', '.venv']
            if dir_name in skip_dirs:
                continue
            
            for file in files:
                if file.endswith('.html') and not file.startswith('.'):
                    full_path = os.path.join(root, file)
                    html_files.append(full_path)
        
        print(f"\n📚 Found {len(html_files)} HTML files to process")
        if not html_files:
            print("⚠️  No HTML files found! Check the directory path.")
            return documents, embeddings, metadatas, ids
        
        # Show first few files
        print("\nFiles to process:")
        for f in html_files[:5]:
            print(f"  - {os.path.relpath(f, root_dir)}")
        if len(html_files) > 5:
            print(f"  ... and {len(html_files) - 5} more")
        print()
        
        chunk_id = 0
        for file_path in html_files:
            # Get relative path for page name
            rel_path = os.path.relpath(file_path, root_dir)
            page_name = rel_path.replace('\\', '/').replace('.html', '')
            
            print(f"🔄 Processing: {page_name}")
            
            try:
                # Extract all chunks from this page
                page_chunks = self.extract_all_content(file_path, page_name)
                
                if not page_chunks:
                    print(f"   ⚠️  No content extracted")
                    continue
                
                print(f"   Found {len(page_chunks)} chunks")
                
                # Generate embeddings for each chunk
                for chunk in page_chunks:
                    try:
                        # Generate embedding
                        embedding = self.embedding_model.encode(chunk['text']).tolist()
                        
                        # Add to lists
                        documents.append(chunk['text'])
                        embeddings.append(embedding)
                        metadatas.append({
                            'page': chunk['page'],
                            'section': chunk['section'],
                            'source_file': rel_path
                        })
                        ids.append(f"chunk_{chunk_id}")
                        chunk_id += 1
                    except Exception as embed_error:
                        print(f"   ⚠️  Embedding error: {embed_error}")
                        continue
                
                print(f"   ✅ Embedded {len(page_chunks)} chunks")
                
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\n📊 Total processed: {len(documents)} chunks")
        return documents, embeddings, metadatas, ids

def setup_comprehensive_database():
    """Setup database with comprehensive website content"""
    print("=" * 60)
    print("🔧 COMPREHENSIVE WEBSITE TRAINING")
    print("=" * 60)
    
    # Get root directory (parent of backend)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir)
    
    print(f"\n📁 Backend directory: {backend_dir}")
    print(f"📁 Website root: {root_dir}")
    print(f"📁 Root dir exists: {os.path.exists(root_dir)}")
    print(f"📁 Files in root: {os.listdir(root_dir)[:10]}")
    
    # Initialize extractor
    print("\n🤖 Loading embedding model...")
    extractor = ComprehensiveExtractor()
    print("✅ Model loaded!")
    
    # Process entire website
    documents, embeddings, metadatas, ids = extractor.process_entire_website(root_dir)
    
    print(f"\n📊 Summary:")
    print(f"   Total chunks: {len(documents)}")
    print(f"   Total characters: {sum(len(doc) for doc in documents)}")
    
    # Import vector store
    from vector_store import get_vector_store
    
    # Initialize vector store
    vector_store = get_vector_store()
    
    # Check existing data
    current_count = vector_store.get_collection_count()
    if current_count > 0:
        print(f"\n⚠️  Vector store already has {current_count} documents")
        response = input("Delete and reload with comprehensive data? (yes/no): ")
        if response.lower() != 'yes':
            print("Keeping existing data. Exiting.")
            return
        vector_store.reset()
        vector_store = get_vector_store()
    
    # Add to vector store
    if not documents:
        print("\n❌ ERROR: No documents were processed!")
        print("   Possible issues:")
        print("   1. No HTML files found in directory")
        print("   2. All HTML files failed to process")
        print("   3. Content extraction failed for all files")
        return
    
    print(f"\n💾 Adding {len(documents)} chunks to vector database...")
    vector_store.add_documents(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    final_count = vector_store.get_collection_count()
    print(f"\n" + "=" * 60)
    print(f"✅ COMPREHENSIVE TRAINING COMPLETE!")
    print(f"📊 Total documents in database: {final_count}")
    print(f"🧠 The chatbot now knows EVERYTHING about your website!")
    print(f"🚀 Restart API: python app_local.py")
    print("=" * 60)

if __name__ == "__main__":
    setup_comprehensive_database()
