# Chunking Strategy Comparison — Day 3

Fixed-size chunking split evidence mid-sentence (e.g. cutting "10:52 PM" 
in half), sometimes merging two unrelated events into one chunk. This risks 
the retriever associating the wrong timestamp with the wrong action.

Recursive chunking with overlap preserved each event (call, file creation, 
upload, phone ping, camera footage) as a clean, self-contained chunk. 
For forensic evidence, where each chunk may later be cited as a distinct 
piece of evidence, this atomicity matters more than raw chunk-size efficiency.

Decision: use recursive/semantic chunking for the evidence-aware RAG system, 
not fixed-size chunking.