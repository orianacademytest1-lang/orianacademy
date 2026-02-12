"""
FastAPI Backend for RAG Chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from vector_store import get_vector_store
from data_processor import DataProcessor

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Oriana Academy RAG API", version="1.0.0")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
llm = genai.GenerativeModel('gemini-2.0-flash-exp')

# Initialize components
vector_store = get_vector_store()
data_processor = DataProcessor()

# RAG System Prompt Template
RAG_PROMPT_TEMPLATE = """You are Oriana, a helpful AI assistant for Oriana Academy.

CRITICAL INSTRUCTIONS:
1. Answer questions SIMPLY and DIRECTLY - keep responses concise
2. Use ONLY the information provided in the Context Chunks below
3. If the answer is not in the context, say "I don't have that specific information. Please contact us at info@orianaacademy.com or call +91 98765 43210"
4. Be friendly and professional, but avoid long explanations

Context Chunks (from vector database):
{context}

User Question:
{question}

Simple Answer:"""

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list = []

@app.get("/api/info")
async def api_info():
    """API info endpoint"""
    return {
        "message": "Oriana Academy RAG API",
        "version": "1.0.0",
        "endpoints": {
            "/api/chat": "POST - Chat with RAG",
            "/api/health": "GET - Health check",
            "/api/stats": "GET - Vector store statistics"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    doc_count = vector_store.get_collection_count()
    return {
        "status": "healthy",
        "vector_store": "connected",
        "documents_count": doc_count
    }

@app.get("/api/stats")
async def get_stats():
    """Get vector store statistics"""
    doc_count = vector_store.get_collection_count()
    return {
        "total_documents": doc_count,
        "collection_name": "oriana_courses"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG-powered chat endpoint
    1. Generate query embedding
    2. Search vector database
    3. Construct prompt with retrieved chunks
    4. Generate response using Gemini
    """
    try:
        # Step 1: Generate query embedding
        query_embedding = data_processor.generate_query_embedding(request.question)
        
        # Step 2: Search vector database for top 3 relevant chunks
        search_results = vector_store.search(query_embedding, n_results=3)
        
        # Step 3: Extract documents and metadata
        retrieved_docs = search_results['documents'][0] if search_results['documents'] else []
        retrieved_metadata = search_results['metadatas'][0] if search_results['metadatas'] else []
        
        # Build context from retrieved chunks
        context = "\n\n---\n\n".join(retrieved_docs) if retrieved_docs else "No relevant information found."
        
        # Step 4: Construct RAG prompt
        prompt = RAG_PROMPT_TEMPLATE.format(
            context=context,
            question=request.question
        )
        
        # Step 5: Generate response using Gemini
        response = llm.generate_content(prompt)
        answer = response.text
        
        # Extract sources for citation
        sources = [
            {
                "course": meta.get('course', 'unknown'),
                "section": meta.get('section', 'unknown')
            }
            for meta in retrieved_metadata
        ]
        
        return ChatResponse(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Mount static files (Frontend)
    from fastapi.staticfiles import StaticFiles
    
    # Mount root directory to serve index.html and other static assets
    # Check if ../index.html exists to confirm we are in the right place
    if os.path.exists("../index.html"):
        app.mount("/", StaticFiles(directory="../", html=True), name="static")
        print("🌍 Serving frontend from ../")
    else:
        print("⚠️  Frontend files not found in ../")

    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Starting RAG API on http://localhost:{port}")
    print(f"📊 Vector store has {vector_store.get_collection_count()} documents")
    uvicorn.run(app, host="0.0.0.0", port=port)
