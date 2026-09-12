# Evidence-Aware Retriever — Pseudocode Design (Week 6 Day 4)

## Hybrid ranking formula

final_score = (a × dense_similarity) + (b × evidence_score) + (c × graph_proximity_score)

Default weights (tuned later in Week 9): a = 0.4, b = 0.35, c = 0.25

## Component signals

- **dense_similarity**: semantic closeness between the query and the 
  evidence chunk's embedding (from the vector DB, Week 2 Day 4).
- **evidence_score**: the recency + reliability + corroboration score 
  defined in Week 6 Day 2.
- **graph_proximity_score**: how close (in graph hops) the evidence's 
  linked entities are to the entities mentioned in the query, using the 
  knowledge graph schema from Week 6 Day 3.

## Pseudocode
def hybrid_retrieve(query, all_evidence, knowledge_graph, top_k=5):
# Step 1: extract entities mentioned in the query
query_entities = extract_entities(query)

# Step 2: dense similarity search (from vector DB)
dense_results = vector_db.search(query, top_n=20)

candidates = []
for item in dense_results:
    dense_sim = item.similarity_score

    # Step 3: evidence score (recency + reliability + corroboration)
    ev_score = evidence_score(
        item,
        query_time=extract_time(query),
        all_evidence=all_evidence
    )

    # Step 4: graph proximity — shortest path (in hops) from query
    # entities to this evidence item's linked entities in the KG
    graph_dist = knowledge_graph.shortest_path(query_entities, item.entity_refs)
    graph_score = 1 / (1 + graph_dist)  # closer = higher score

    # Step 5: combine into final rank
    final_score = 0.4 * dense_sim + 0.35 * ev_score + 0.25 * graph_score
    candidates.append((item, final_score))

# Step 6: sort and return top_k
candidates.sort(key=lambda x: x[1], reverse=True)
return candidates[:top_k]


## Why hybrid, not dense-only

Pure dense retrieval (Week 2) misses corroboration/reliability signals 
and can't reason about entity relationships. Graph proximity lets the 
retriever pull in evidence that's *relevant by connection* even if it 
doesn't share query keywords or close embedding similarity — e.g. 
retrieving Mike's location ping when the query is about John, because 
they're linked via COMMUNICATED_WITH in the knowledge graph.

## Relationship to earlier design decisions

This retriever design directly builds on:
- The evidence schema (Week 5 Day 4) — provides `confidence`, 
  `entity_refs`, and `timestamp` fields used in scoring
- The evidence scoring spec (Week 6 Day 2) — defines `evidence_score()`
- The knowledge graph schema (Week 6 Day 3) — defines the node/edge 
  types traversed for `graph_proximity_score`

It will be implemented as real code in Week 9 (`retriever/hybrid_rank.py`), 
using this document as the specification.