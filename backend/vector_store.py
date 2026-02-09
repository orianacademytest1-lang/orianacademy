"""
Vector Store Management using ChromaDB
"""
import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        """Initialize ChromaDB vector store"""
        self.chroma_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
        
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(
            path=self.chroma_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="oriana_courses",
            metadata={"description": "Oriana Academy course content embeddings"}
        )
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], 
                     metadatas: List[Dict[str, Any]], ids: List[str]):
        """Add documents with embeddings to vector store"""
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Added {len(documents)} documents to vector store")
    
    def search(self, query_embedding: List[float], n_results: int = 3) -> Dict[str, Any]:
        """Search for similar documents using vector similarity"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        return results
    
    def get_collection_count(self) -> int:
        """Get total number of documents in collection"""
        return self.collection.count()
    
    def reset(self):
        """Clear all data from collection (use with caution!)"""
        self.client.reset()
        print("⚠️  Vector store reset complete")
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(name="oriana_courses")
        print("🗑️  Collection deleted")

# Singleton instance
_vector_store = None

def get_vector_store() -> VectorStore:
    """Get or create vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

def reset_vector_store():
    """Reset the singleton instance (used during re-indexing)"""
    global _vector_store
    _vector_store = None
