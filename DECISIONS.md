# Architecture & Design Decisions (ADR)

## 1. Vector Database: ChromaDB vs. Pinecone / Qdrant
- **Decision:** ChromaDB running locally/embedded within the cluster.
- **Reasoning:** ChromaDB requires zero external cloud API dependencies, eliminates vendor egress costs, and keeps latency sub-millisecond for local retrieval. For enterprise scale (Project 5), it can transition to Qdrant/Milvus without rewriting core retrieval logic.

## 2. Chunking Strategy & Token Window
- **Decision:** Recursive character splitting with `chunk_size = 500` characters and `chunk_overlap = 50`.
- **Reasoning:** Runbooks and technical documents contain dense context (service endpoints, timeout configs, runbook IDs). Smaller chunks (400–600 tokens) yield higher retrieval precision, preventing extraneous noise from polluting the prompt context and reducing token usage.

## 3. LLM Selection: gpt-4o-mini / Groq vs. Full Frontier Models
- **Decision:** Cost-efficient small reasoning models (`gpt-4o-mini` / Llama via Groq).
- **Reasoning:** In an internal documentation assistant, the heavy lifting is retrieval precision, not creative writing. Using smaller, high-throughput models cuts inference cost by ~90% and delivers p95 latency under 1 second while maintaining zero-shot citation accuracy.

## 4. Hallucination Mitigation
- **Decision:** Strict system prompting with mandatory citations and explicit out-of-context fallback.
- **Reasoning:** If the top-k cosine similarity threshold is not met or context does not contain the answer, the assistant explicitly declines to answer rather than hallucinating plausible false runbook steps.
