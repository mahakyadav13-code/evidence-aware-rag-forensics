# How LLMs Work

Large Language Models (LLMs), such as GPT and Claude, are built primarily on an architecture known as the **Transformer**. Transformers process text as a sequence of tokens and learn the relationships between these tokens within a given context. Unlike earlier language-processing approaches that handled text more sequentially, transformers can examine relationships between multiple parts of the input simultaneously.

## Attention Mechanism

A fundamental component of the Transformer architecture is the **attention mechanism**. Attention enables the model to assign greater importance to tokens that are more relevant to understanding the meaning of a particular word or sentence.

For example, consider the sentence:

> “The suspect deleted the files after the call.”

When processing the word **“deleted,”** the model needs to determine what was deleted and who performed the action. The attention mechanism helps the model identify the stronger relationships between **“deleted,” “files,”** and **“suspect,”** while words such as **“the”** or **“after”** may have less relevance to that specific relationship.

This ability to identify relationships between different parts of the input allows LLMs to interpret language based on its surrounding context rather than treating each word independently.

## Context Window

The **context window** refers to the amount of information an LLM can process and consider at a given time. This capacity is measured in **tokens**.

For example, if a model has an 8,000-token context window, the total input provided to the model must fit within that limit. If the amount of information exceeds the available context window, some content may need to be truncated or excluded.

This limitation is particularly important for **Retrieval-Augmented Generation (RAG)** systems. A RAG system may retrieve information from multiple sources, but providing all retrieved information to the LLM is not always practical or effective. Instead, the most relevant evidence must be identified, selected, and organized so that it fits within the available context while providing sufficient information for the model to generate a reliable response.

## Tokens

LLMs do not process text directly as complete words. Instead, text is divided into smaller units called **tokens**.

A token may represent a complete word, part of a word, punctuation, or another small unit of text, depending on the tokenizer being used. For example, a less common word such as **“investigation”** may be divided into multiple tokens, while a common word such as **“the”** is typically represented as a single token.

As a general approximation for English text, **1,000 tokens correspond to roughly 750 words**, although the exact relationship varies depending on the content and tokenizer.

## Why This Matters for Our Project

Understanding **tokens, attention, and context windows** is important for developing our **evidence-aware RAG system**.

The system may retrieve evidence from multiple sources, but the LLM has a finite context capacity. Therefore, the system must determine **which pieces of evidence are most relevant and how much information should be provided to the model**.

Providing excessive information can result in important evidence being truncated or becoming less effective for the model to use. Conversely, providing insufficient evidence may prevent the model from generating a complete and well-supported investigator report.

Therefore, **effective evidence selection, context management, and token management** are essential for improving the reliability, relevance, and completeness of an evidence-aware RAG system.
