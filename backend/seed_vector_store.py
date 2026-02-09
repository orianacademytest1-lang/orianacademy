"""
Seed Vector Store - Process all course HTML files and add to ChromaDB
"""
import os
import sys

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_store import get_vector_store
from data_processor import DataProcessor

def seed_data():
    print("🚀 Starting vector store seeding...")
    
    # Initialize components
    vs = get_vector_store()
    dp = DataProcessor()
    
    # Process all courses
    documents, embeddings, metadatas, ids = dp.process_all_courses()
    
    if not documents:
        print("❌ No documents found to index.")
        return
    
    print(f"📊 Adding {len(documents)} document chunks to vector store...")
    
    # Add to vector store
    vs.add_documents(documents, embeddings, metadatas, ids)
    
    print("\n✨ Seeding complete!")
    print(f"📈 Total documents in collection: {vs.get_collection_count()}")

if __name__ == "__main__":
    seed_data()
