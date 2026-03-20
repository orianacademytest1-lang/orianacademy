
import chromadb
from chromadb.config import Settings
import os

try:
    client = chromadb.PersistentClient(path="./test_chroma", settings=Settings(anonymized_telemetry=False, allow_reset=True))
    collection = client.get_or_create_collection(name="test")
    collection.add(
        documents=["test doc"],
        embeddings=[[0.1] * 384],
        metadatas=[{"source": "test"}],
        ids=["id1"]
    )
    print("CHROMA OK")
except Exception as e:
    print(f"CHROMA ERROR: {e}")
