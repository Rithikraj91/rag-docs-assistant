# RAG-Powered Internal Docs Assistant

Production-grade Retrieval-Augmented Generation (RAG) assistant running on Kubernetes with Prometheus/Grafana observability.

## Architecture & Tech Stack
- **App**: FastAPI, sentence-transformers, ChromaDB, Groq/OpenAI
- **Orchestration**: Kubernetes (Minikube), Docker
- **Observability**: Prometheus & Grafana tracking RPS and p95 Latency

## Live Metrics Verified
- Baseline p95 Latency: ~100 ms
- Under 50-Request Burst: Peak p95 latency ~1.0s
- Exported Dashboard: `rag-observability-dashboard.json`

## Documentation
- Architecture choices: [DECISIONS.md](./DECISIONS.md)
