"""
Setup Database - One-time script to populate vector store with course embeddings
"""
import sys
from vector_store import get_vector_store
from data_processor import DataProcessor

def setup_database():
    """Load all course data into vector database"""
    print("=" * 60)
    print("🔧 ORIANA ACADEMY - VECTOR DATABASE SETUP")
    print("=" * 60)
    
    # Initialize components
    print("\n📦 Initializing vector store and data processor...")
    vector_store = get_vector_store()
    data_processor = DataProcessor()
    
    # Check if database already has data
    current_count = vector_store.get_collection_count()
    if current_count > 0:
        print(f"\n⚠️  Vector store already has {current_count} documents")
        response = "yes" # input("Do you want to reset and reload? (yes/no): ")
        if response.lower() == 'yes':
            print("🗑️  Resetting vector store...")
            vector_store.reset()
            vector_store = get_vector_store()  # Reinitialize
        else:
            print("✅ Keeping existing data. Exiting.")
            return
    
    # Process all course files
    print("\n📚 Processing all course HTML files...")
    print("   (This may take a few minutes...)\n")
    
    try:
        documents, embeddings, metadatas, ids = data_processor.process_all_courses()
        
        print(f"\n✅ Processed {len(documents)} total chunks")
        print(f"\n💾 Adding to vector database...")
        
        # Add to vector store
        vector_store.add_documents(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        # Verify
        final_count = vector_store.get_collection_count()
        print(f"\n" + "=" * 60)
        print(f"✅ DATABASE SETUP COMPLETE!")
        print(f"📊 Total documents in vector store: {final_count}")
        print(f"🚀 You can now start the API server with: python app.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
