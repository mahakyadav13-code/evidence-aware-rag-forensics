# Tech Stack Decision

## LLM API
Anthropic Claude — tested and working in Week 1 Day 6 API setup.

## Vector Database
ChromaDB — used in Week 2 Day 2 for local vector storage and similarity search.

## Embedding Model
sentence-transformers (all-MiniLM-L6-v2) — tested in Week 1 Day 4, showed strong 
semantic similarity results on evidence-style text.

## Graph Library
networkx — used in Week 3 Day 3 for KG construction. Sufficient for our project 
scale (synthetic case with limited entities); Neo4j not needed unless the graph 
grows significantly larger.

## Backend
FastAPI — lightweight, Python-native, good fit for wrapping our pipeline modules 
behind an API layer for the UI (Week 12).

## Evaluation
RAGAS — planned for Week 13 evaluation phase (faithfulness, context precision/recall).