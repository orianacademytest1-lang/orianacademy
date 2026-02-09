"""
Data Processor - Extract and chunk course content for embeddings
"""
import os
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class DataProcessor:
    def __init__(self):
        """Initialize data processor with local embedding model"""
        from sentence_transformers import SentenceTransformer
        print("📥 Loading local embedding model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def extract_course_content(self, html_path: str) -> Dict[str, str]:
        """Extract structured content from course HTML file"""
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        content = {
            'title': '',
            'description': '',
            'curriculum': [],
            'features': [],
            'duration': '',
            'placement': '',
            'certification': ''
        }
        
        # Extract title
        hero = soup.find('section', class_='hero')
        if hero:
            h1 = hero.find('h1')
            if h1:
                content['title'] = h1.get_text(strip=True)
            
            subtitle = hero.find('p', class_='hero-subtitle')
            if subtitle:
                content['description'] = subtitle.get_text(strip=True)
        
        # Extract curriculum cards
        curriculum_cards = soup.find_all('div', class_='curriculum-card')
        for card in curriculum_cards:
            title_elem = card.find('h3')
            desc_elem = card.find('p')
            if title_elem:
                curriculum_item = {
                    'title': title_elem.get_text(strip=True),
                    'description': desc_elem.get_text(strip=True) if desc_elem else ''
                }
                content['curriculum'].append(curriculum_item)
        
        # Extract info pills (duration, placement, certification)
        info_pills = soup.find_all('div', class_='info-pill')
        for pill in info_pills:
            text = pill.get_text(strip=True)
            if 'month' in text.lower() or 'week' in text.lower():
                content['duration'] = text
            elif 'placement' in text.lower():
                content['placement'] = text
            elif 'certification' in text.lower() or 'certified' in text.lower():
                content['certification'] = text
        
        # Extract features
        feature_cards = soup.find_all('div', class_='feature-card')
        for card in feature_cards:
            h3 = card.find('h3')
            p = card.find('p')
            if h3:
                content['features'].append({
                    'title': h3.get_text(strip=True),
                    'description': p.get_text(strip=True) if p else ''
                })
        
        return content
    
    def chunk_content(self, course_data: Dict[str, str], course_name: str, 
                     source_file: str, chunk_size: int = 500) -> List[Dict]:
        """Create chunks from course content with metadata"""
        chunks = []
        
        # Chunk 1: Course overview
        overview_text = f"""
        Course: {course_data['title']}
        Description: {course_data['description']}
        Duration: {course_data['duration']}
        Placement: {course_data['placement']}
        Certification: {course_data['certification']}
        """.strip()
        
        chunks.append({
            'text': overview_text,
            'metadata': {
                'course': course_name,
                'section': 'overview',
                'source_file': source_file
            }
        })
        
        # Chunk 2-N: Each curriculum item
        for idx, item in enumerate(course_data['curriculum']):
            curriculum_text = f"""
            {course_data['title']} - {item['title']}
            {item['description']}
            """.strip()
            
            chunks.append({
                'text': curriculum_text,
                'metadata': {
                    'course': course_name,
                    'section': 'curriculum',
                    'curriculum_item': item['title'],
                    'source_file': source_file
                }
            })
        
        # Chunk N+1: Features summary
        if course_data['features']:
            features_text = f"{course_data['title']} Features:\n"
            features_text += "\n".join([
                f"- {f['title']}: {f['description']}" 
                for f in course_data['features']
            ])
            
            chunks.append({
                'text': features_text,
                'metadata': {
                    'course': course_name,
                    'section': 'features',
                    'source_file': source_file
                }
            })
        
        return chunks
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using local model"""
        return self.model.encode(text).tolist()
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for search query"""
        return self.model.encode(query).tolist()
    
    def process_all_courses(self, courses_dir: str = None) -> Tuple[List, List, List, List]:
        """Process all HTML course files and return chunks with embeddings"""
        # Use absolute path relative to backend directory
        if courses_dir is None:
            import os
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            courses_dir = os.path.join(os.path.dirname(backend_dir), 'courses')
        
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        # Get all HTML files in courses directory
        if not os.path.exists(courses_dir):
            print(f"❌ Courses directory not found: {courses_dir}")
            return documents, embeddings, metadatas, ids
            
        course_files = [f for f in os.listdir(courses_dir) if f.endswith('.html')]
        
        print(f"📚 Found {len(course_files)} course files in {courses_dir}")
        
        for idx, filename in enumerate(course_files):
            course_name = filename.replace('.html', '')
            file_path = os.path.join(courses_dir, filename)
            
            print(f"\n🔄 Processing: {course_name}")
            
            try:
                # Extract content
                course_data = self.extract_course_content(file_path)
                
                # Create chunks
                chunks = self.chunk_content(course_data, course_name, filename)
                
                print(f"   Created {len(chunks)} chunks")
                
                # Generate embeddings for each chunk
                for chunk_idx, chunk in enumerate(chunks):
                    chunk_id = f"{course_name}_{chunk_idx}"
                    
                    # Generate embedding
                    embedding = self.generate_embedding(chunk['text'])
                    
                    documents.append(chunk['text'])
                    embeddings.append(embedding)
                    metadatas.append(chunk['metadata'])
                    ids.append(chunk_id)
                    
                    print(f"   ✓ Chunk {chunk_idx + 1}/{len(chunks)}: {chunk['metadata']['section']}")
            except Exception as e:
                print(f"   ⚠️  Error processing {filename}: {str(e)}")
                continue
        
        return documents, embeddings, metadatas, ids
