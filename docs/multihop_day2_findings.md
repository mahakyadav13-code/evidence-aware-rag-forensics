# Multi-Hop Day 2 Findings

Decomposition works well (LLM correctly breaks complex temporal 
questions into sequential sub-queries). However, retrieval for 
sub-queries 1-3 still returned "the call" as top result even 
though the sub-queries asked about events AFTER the call — pure 
semantic similarity cannot distinguish "the call" from "after the 
call" since both mention "call" prominently.

This confirms: query decomposition alone is not sufficient. The 
retriever needs explicit timestamp filtering (e.g. timestamp > 
call_end_time) combined with semantic search, not semantic search 
alone. This will be addressed in Day 4 (Timeline Builder).