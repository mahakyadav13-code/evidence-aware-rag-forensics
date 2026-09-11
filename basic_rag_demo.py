import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()
client_llm = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Evidence "documents" (stand-in for real case files)
documents = [
    "John called Mike at 10:30 PM on the night of the incident.",
    "The IP address 192.168.1.5 accessed the server at midnight.",
    "A file named 'transfer.zip' was created on the suspect's laptop.",
    "Mike sent a message saying 'meet me at the warehouse'.",
    "The suspect's phone location pinged near the warehouse at 11 PM.",
]

# Step 1: Store in vector DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("basic_rag_demo")
collection.add(documents=documents, ids=[f"doc{i}" for i in range(len(documents))])

# Step 2: Retrieve relevant chunks for a query
query = "What did the suspect do around 11 PM?"
results = collection.query(query_texts=[query], n_results=3)
retrieved_chunks = results["documents"][0]

# Step 3: Build prompt with retrieved context
context = "\n".join(retrieved_chunks)
prompt = f"""Using ONLY the evidence below, answer the question. Cite which evidence line supports your answer.

Evidence:
{context}

Question: {query}
"""

# Step 4: Generate grounded answer
response = client_llm.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("=== RETRIEVED EVIDENCE ===")
for c in retrieved_chunks:
    print("-", c)

print("\n=== GENERATED ANSWER ===")
print(response.text)