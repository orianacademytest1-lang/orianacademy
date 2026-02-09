# Oriana Academy RAG Backend

Python backend for vector-based Retrieval-Augmented Generation (RAG) chatbot.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` file with your API key (already configured):
```
GEMINI_API_KEY=your_key_here
```

### 3. Initialize Vector Database
Run once to load course data:
```bash
cd backend
python setup_database.py
```

This will:
- Extract content from all course HTML files
- Generate embeddings using Gemini API
- Store in ChromaDB vector database
- Takes ~2-5 minutes depending on course count

### 4. Start API Server
```bash
python app.py
```

Server runs on: `http://localhost:5000`

## API Endpoints

### `POST /api/chat`
Main RAG endpoint for chatbot queries.

**Request:**
```json
{
  "question": "What courses do you offer?"
}
```

**Response:**
```json
{
  "answer": "We offer 8 courses including...",
  "sources": [
    {"course": "data-science", "section": "overview"},
    {"course": "machine-learning", "section": "curriculum"}
  ]
}
```

### `GET /api/health`
Health check and database status.

### `GET /api/stats`
Vector store statistics.

## Architecture

1. **User asks question** → Frontend sends to `/api/chat`
2. **Generate embedding** → Question converted to vector
3. **Semantic search** → Find top 3 relevant course chunks
4. **Build context** → Combine retrieved chunks
5. **LLM generation** → Gemini creates answer from context
6. **Return response** → Send answer + sources to frontend

## Files

- `app.py` - FastAPI server with RAG endpoints
- `vector_store.py` - ChromaDB wrapper
- `data_processor.py` - Content extraction & embeddings
- `setup_database.py` - One-time database initialization
- `requirements.txt` - Python dependencies
- `.env` - Environment variables
