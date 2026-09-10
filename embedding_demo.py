from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "The suspect deleted the files at midnight.",
    "Evidence was erased around 12 AM.",
    "The victim went to the market to buy vegetables.",
    "He purchased groceries from the store.",
    "The weather was sunny yesterday."
]

embeddings = model.encode(sentences)

print("Embedding shape:", embeddings.shape)

sim_matrix = cosine_similarity(embeddings)
print("\nSimilarity matrix:")
for i, row in enumerate(sim_matrix):
    print(f"Sentence {i}: {[round(x, 2) for x in row]}")