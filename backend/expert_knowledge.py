"""
Expert Knowledge Base for Oriana Academy
This file contains specific, high-priority facts about the academy to ensure accurate responses.
"""
import os
from sentence_transformers import SentenceTransformer
from vector_store import get_vector_store

def add_expert_knowledge():
    print("🧠 Adding Expert Knowledge Chunks...")
    
    expert_chunks = [
        {
            "text": "Oriana Academy (founded in 2018) is India's leading IT training institute specializing in Data Science, AI, and Digital Marketing. Our mission is to bridge the gap between academic education and industry requirements through practical, hands-on training.",
            "section": "general_info"
        },
        {
            "text": "The leadership team at Oriana Academy includes Rajesh Sharma (Founder & CEO), Priya Mehta (Head of Training), Vikram Kumar (Tech Lead), and Anita Rao (Placement Director). They bring over 50 combined years of industry experience from top MNCs.",
            "section": "leadership"
        },
        {
            "text": "Oriana Academy is located in Bangalore, India, at 123 Tech Park. We offer both online live classes and offline in-person training. Contact us at info@orianaacademy.com or call +91 98765 43210 for inquiries.",
            "section": "contact"
        },
        {
            "text": "Our placement program has a 95% success rate. We have 50+ hiring partners including Google, Amazon, Microsoft, IBM, and TCS. Graduates receive 100% placement support including resume building and mock interviews.",
            "section": "placement"
        },
        {
            "text": "Oriana Academy's unique teaching methodology includes blending theory with real-time projects, pre-class assignments to encourage engagement, and interactive live sessions with industry experts.",
            "section": "methodology"
        },
        {
            "text": "Courses offered at Oriana Academy: Digital Marketing Mastery, Machine Learning Pro, Data Science Bootcamp, Data Analytics Expert, Python Full Stack, Java Enterprise, Generative AI Mastery, and HR Professional training.",
            "section": "courses_list"
        },
        {
            "text": "Data Science Bootcamp covers Python, Statistics, Machine Learning, and Big Data. It includes real-world projects and is ideal for anyone looking to enter the data field. Available in both online and offline formats.",
            "section": "data_science"
        }
    ]

    model = SentenceTransformer('all-MiniLM-L6-v2')
    vector_store = get_vector_store()
    
    documents = []
    embeddings = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(expert_chunks):
        # Prefix for priming
        text = f"Oriana Academy Expert Knowledge: {chunk['text']}"
        embedding = model.encode(text).tolist()
        
        documents.append(text)
        embeddings.append(embedding)
        metadatas.append({
            "page": "official_facts",
            "section": chunk['section'],
            "type": "expert_data",
            "source_file": "expert_knowledge.py"
        })
        ids.append(f"expert_chunk_{i}")

    vector_store.add_documents(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ Successfully added {len(documents)} expert knowledge chunks.")

if __name__ == "__main__":
    add_expert_knowledge()
