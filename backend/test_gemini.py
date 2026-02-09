"""
Test Gemini API directly with RAG prompt
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
llm = genai.GenerativeModel('models/gemini-2.5-flash')

# Test prompt
test_context = """
Data Science: Python & Statistics, Machine Learning algorithms, Data Visualization
""".strip()

test_prompt = f"""You are Oriana, a helpful AI assistant for Oriana Academy.

CRITICAL INSTRUCTIONS:
1. Answer questions SIMPLY and DIRECTLY - keep responses concise
2. Use ONLY the information provided in the Context Chunks below
3. If the answer is not in the context, say "I don't have that specific information. Please contact us at info@orianaacademy.com or call +91 98765 43210"
4. Be friendly and professional, but avoid long explanations

Context Chunks (from vector database):
{test_context}

User Question:
What is Data Science?

Simple Answer:"""

print("Testing Gemini API...")
print(f"Prompt length: {len(test_prompt)} characters\n")

try:
    response = llm.generate_content(test_prompt)
    print("✅ SUCCESS!")
    print(f"Answer: {response.text}\n")
except Exception as e:
    print(f"❌ ERROR: {e}\n")
    import traceback
    traceback.print_exc()
