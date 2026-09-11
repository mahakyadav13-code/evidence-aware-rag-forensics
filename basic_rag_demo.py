import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()
client_llm = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def check_faithfulness(answer, retrieved_context):
    """
    Very basic faithfulness heuristic:
    counts how many key words from the answer also appear in the
    retrieved context. Low overlap = possible hallucination.
    """
    answer_words = set(answer.lower().split())
    context_words = set(retrieved_context.lower().split())

    overlap = answer_words.intersection(context_words)
    score = len(overlap) / max(len(answer_words), 1)

    return {
        "faithfulness_score": round(score, 2),
        "unsupported_words": list(answer_words - context_words)
    }


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

queries = [
    "What did the suspect do around 11 PM?",
    "Who did John talk to on the night of the incident?",
    "What evidence links the suspect to the warehouse?",
]

results_log = []

for query in queries:
    results = collection.query(query_texts=[query], n_results=3)
    retrieved_chunks = results["documents"][0]
    context = "\n".join(retrieved_chunks)

    prompt = f"""Using ONLY the evidence below, answer the question. Cite which evidence line supports your answer.

Evidence:
{context}

Question: {query}
"""

    response = client_llm.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    answer = response.text

    faithfulness = check_faithfulness(answer, context)

    print("\n=== QUERY ===")
    print(query)
    print("--- RETRIEVED EVIDENCE ---")
    for c in retrieved_chunks:
        print("-", c)
    print("--- GENERATED ANSWER ---")
    print(answer)
    print("--- FAITHFULNESS ---")
    print(faithfulness)

    results_log.append({
        "query": query,
        "answer": answer,
        "faithfulness_score": faithfulness["faithfulness_score"]
    })

print("\n=== SUMMARY ===")
for r in results_log:
    print(r["query"], "->", r["faithfulness_score"])