import chromadb

client = chromadb.Client()
collection = client.create_collection("evidence_demo")

documents = [
    "John called Mike at 10:30 PM on the night of the incident.",
    "The IP address 192.168.1.5 accessed the server at midnight.",
    "A file named 'transfer.zip' was created on the suspect's laptop.",
    "Mike sent a message saying 'meet me at the warehouse'.",
    "The suspect's phone location pinged near the warehouse at 11 PM."
]
ids = [f"doc{i}" for i in range(len(documents))]

collection.add(documents=documents, ids=ids)

results = collection.query(
    query_texts=["Who did the suspect contact around the time of the incident?"],
    n_results=3
)

for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"Score: {dist:.4f} | {doc}")