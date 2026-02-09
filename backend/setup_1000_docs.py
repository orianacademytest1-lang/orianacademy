"""
ULTRA-COMPREHENSIVE Website Content Extractor
Creates 1000+ training documents through granular chunking
"""
import os
from bs4 import BeautifulSoup
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import re

class UltraComprehensiveExtractor:
    def __init__(self):
        """Initialize the ultra-comprehensive content extractor"""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = 600  # Increased for better context
        self.overlap = 150  # Increased for smoother transitions
    
    def chunk_text(self, text, max_length=600, overlap=150):
        """Split text into overlapping chunks"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + max_length
            chunk = text[start:end]
            
            # Try to break at sentence/word boundary
            if end < len(text):
                last_period = chunk.rfind('. ')
                last_space = chunk.rfind(' ')
                if last_period > max_length * 0.7:
                    chunk = chunk[:last_period + 1]
                elif last_space > max_length * 0.7:
                    chunk = chunk[:last_space]
            
            chunks.append(chunk.strip())
            start += max_length - overlap
        
        return chunks
    
    def extract_all_content(self, html_path, page_name):
        """Extract ALL content with maximum granularity"""
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Remove noise
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        
        chunks = []
        
        # 1. PAGE METADATA
        title = soup.find('title')
        if title:
            chunks.append({
                'text': f"Page Title: {title.get_text(strip=True)}",
                'section': 'metadata',
                'page': page_name,
                'type': 'title'
            })
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            chunks.append({
                'text': f"Description: {meta_desc.get('content', '')}",
                'section': 'metadata',
                'page': page_name,
                'type': 'meta'
            })
        
        # 2. HERO SECTION (chunked)
        hero = soup.find('section', class_='hero')
        if hero:
            # Extract hero title
            h1 = hero.find('h1')
            if h1:
                chunks.append({
                    'text': f"{page_name}: {h1.get_text(strip=True)}",
                    'section': 'hero',
                    'page': page_name,
                    'type': 'heading'
                })
            
            # Extract hero subtitle
            subtitle = hero.find(['p', 'div'], class_=['hero-subtitle', 'subtitle'])
            if subtitle:
                text = subtitle.get_text(strip=True)
                for chunk_text in self.chunk_text(text):
                    chunks.append({
                        'text': f"{page_name} - {chunk_text}",
                        'section': 'hero',
                        'page': page_name,
                        'type': 'content'
                    })
        
        # 3. ALL HEADINGS (create index)
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for idx, heading in enumerate(headings):
            text = heading.get_text(strip=True)
            if len(text) > 3:
                chunks.append({
                    'text': f"{page_name} section: {text}",
                    'section': f'heading_{idx}',
                    'page': page_name,
                    'type': 'heading'
                })
        
        # 4. ALL PARAGRAPHS (chunked individually)
        paragraphs = soup.find_all('p')
        for idx, p in enumerate(paragraphs):
            text = p.get_text(strip=True)
            if len(text) > 30:  # Skip very short paragraphs
                # Get parent section context
                parent_section = p.find_parent('section')
                section_name = 'content'
                if parent_section:
                    section_class = parent_section.get('class', [''])[0]
                    section_name = section_class or 'content'
                
                # Chunk the paragraph
                for chunk_text in self.chunk_text(text, 250, 50):
                    chunks.append({
                        'text': f"{page_name} - {chunk_text}",
                        'section': section_name,
                        'page': page_name,
                        'type': 'paragraph'
                    })
        
        # 5. ALL LISTS (each item becomes a chunk)
        lists = soup.find_all(['ul', 'ol'])
        for list_elem in lists:
            if list_elem.find_parent(['nav', 'footer']):
                continue
            
            items = list_elem.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if len(text) > 10:
                    chunks.append({
                        'text': f"{page_name}: {text}",
                        'section': 'list_item',
                        'page': page_name,
                        'type': 'list'
                    })
        
        # 6. ALL CARDS/DIVS with substantial content
        cards = soup.find_all('div')
        for idx, card in enumerate(cards):
            # Skip if it's a container with other cards
            if card.find_all('div'):
                continue
            
            text = card.get_text(separator=' ', strip=True)
            text = ' '.join(text.split())
            
            if 20 < len(text) < 500:  # Sweet spot for card content
                card_class = card.get('class', [''])[0] if card.get('class') else 'card'
                for chunk_text in self.chunk_text(text, 200, 30):
                    chunks.append({
                        'text': f"{page_name} - {chunk_text}",
                        'section': str(card_class),
                        'page': page_name,
                        'type': 'card'
                    })
        
        # 7. TABLES (extract row by row)
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_text = ' | '.join([cell.get_text(strip=True) for cell in cells])
                if len(row_text) > 10:
                    chunks.append({
                        'text': f"{page_name} table: {row_text}",
                        'section': 'table',
                        'page': page_name,
                        'type': 'table'
                    })
        
        # 8. LINKS (extract meaningful links)
        links = soup.find_all('a', href=True)
        for link in links:
            link_text = link.get_text(strip=True)
            if len(link_text) > 5 and not link_text.lower() in ['home', 'back', 'next']:
                chunks.append({
                    'text': f"{page_name} link: {link_text}",
                    'section': 'navigation',
                    'page': page_name,
                    'type': 'link'
                })
        
        # 9. STRONG/BOLD TEXT (key information)
        strong_tags = soup.find_all(['strong', 'b'])
        for strong in strong_tags:
            text = strong.get_text(strip=True)
            if len(text) > 5:
                chunks.append({
                    'text': f"{page_name} key point: {text}",
                    'section': 'emphasis',
                    'page': page_name,
                    'type': 'emphasized'
                })
        
        # 10. SECTION-BASED EXTRACTION (with context)
        sections = soup.find_all('section')
        for idx, section in enumerate(sections):
            section_id = section.get('class', [''])[0] or section.get('id', f'section_{idx}')
            
            # Get section title
            section_title = section.find(['h2', 'h3'])
            title_text = section_title.get_text(strip=True) if section_title else f"Section {idx}"
            
            # Get full section content
            content = section.get_text(separator=' ', strip=True)
            content = ' '.join(content.split())
            
            if len(content) > 100:
                # Create multiple overlapping chunks from section
                for chunk_text in self.chunk_text(content, 300, 75):
                    chunks.append({
                        'text': f"{page_name} - {title_text}: {chunk_text}",
                        'section': str(section_id),
                        'page': page_name,
                        'type': 'section'
                    })
        
        return chunks
    
    def process_entire_website(self, root_dir):
        """Process ALL HTML files with maximum granularity"""
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        print(f"📂 Scanning directory: {root_dir}")
        
        # Find all HTML files
        html_files = []
        for root, dirs, files in os.walk(root_dir):
            dir_name = os.path.basename(root)
            skip_dirs = ['backend', 'node_modules', '__pycache__', '.git', '.venv']
            if dir_name in skip_dirs:
                continue
            
            for file in files:
                if file.endswith('.html') and not file.startswith('.'):
                    html_files.append(os.path.join(root, file))
        
        print(f"\n📚 Found {len(html_files)} HTML files")
        print(f"🎯 Target: 1000+ document chunks\n")
        
        chunk_id = 0
        for file_path in html_files:
            rel_path = os.path.relpath(file_path, root_dir)
            page_name = rel_path.replace('\\', '/').replace('.html', '')
            
            print(f"🔄 Processing: {page_name}")
            
            try:
                page_chunks = self.extract_all_content(file_path, page_name)
                
                if not page_chunks:
                    print(f"   ⚠️  No content extracted")
                    continue
                
                print(f"   Found {len(page_chunks)} chunks")
                
                # Generate embeddings
                for chunk in page_chunks:
                    try:
                        # Add global context prefix to improve retrieval
                        text_with_context = f"Oriana Academy Knowledge: {chunk['text']}"
                        embedding = self.embedding_model.encode(text_with_context).tolist()
                        
                        documents.append(text_with_context)
                        embeddings.append(embedding)
                        metadatas.append({
                            'page': chunk['page'],
                            'section': chunk['section'],
                            'type': chunk['type'],
                            'source_file': rel_path
                        })
                        ids.append(f"chunk_{chunk_id}")
                        chunk_id += 1
                    except Exception as e:
                        print(f"   ⚠️  Embedding error: {e}")
                        continue
                
                print(f"   ✅ Total so far: {len(documents)} chunks")
                
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                continue
        
        print(f"\n📊 FINAL: {len(documents)} chunks created!")
        return documents, embeddings, metadatas, ids

def setup_1000_documents():
    """Setup database with 1000+ documents"""
    print("=" * 60)
    print("🔧 ULTRA-COMPREHENSIVE TRAINING: 1000+ DOCUMENTS")
    print("=" * 60)
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(backend_dir)
    
    print(f"\n📁 Website root: {root_dir}")
    
    print("\n🤖 Loading embedding model...")
    extractor = UltraComprehensiveExtractor()
    print("✅ Model loaded!")
    
    # Process website
    documents, embeddings, metadatas, ids = extractor.process_entire_website(root_dir)
    
    print(f"\n📊 Summary:")
    print(f"   Total chunks: {len(documents)}")
    print(f"   Target achieved: {'✅ YES' if len(documents) >= 1000 else '❌ NO'}")
    
    if len(documents) < 1000:
        print(f"   Gap: {1000 - len(documents)} more chunks needed")
    
    # Import vector store
    from vector_store import get_vector_store
    vector_store = get_vector_store()
    
    # Check existing
    current_count = vector_store.get_collection_count()
    if current_count > 0:
        print(f"\n⚠️  Vector store has {current_count} documents. Resetting for fresh index...")
        from vector_store import reset_vector_store
        vector_store.reset()
        reset_vector_store() # Clear singleton
        vector_store = get_vector_store() # Re-initialize
    
    if not documents:
        print("\n❌ ERROR: No documents created!")
        return
    
    print(f"\n💾 Adding {len(documents)} chunks to ChromaDB...")
    vector_store.add_documents(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    final_count = vector_store.get_collection_count()
    print(f"\n" + "=" * 60)
    print(f"✅ ULTRA-COMPREHENSIVE TRAINING COMPLETE!")
    print(f"📊 Database: {final_count} documents")
    print(f"🧠 Chatbot is now an EXPERT on your website!")
    print(f"🚀 Restart: python app_local.py")
    print("=" * 60)

if __name__ == "__main__":
    setup_1000_documents()
