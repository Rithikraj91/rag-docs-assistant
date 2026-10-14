# 📚 RAG Docs Assistant — Enterprise Knowledge Retrieval on Kubernetes

[![CI/CD Pipeline](https://github.com/Rithikraj91/rag-docs-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Rithikraj91/rag-docs-assistant/actions)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes%20(Minikube)-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Grafana](https://img.shields.io/badge/Observability-Prometheus%20%2B%20Grafana-F46800?logo=grafana&logoColor=white)](https://grafana.com/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![VectorDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-blue)](https://www.trychroma.com/)

> Production-ready Retrieval-Augmented Generation (RAG) microservice running on Kubernetes. Ingests internal runbooks, performs low-latency vector similarity retrieval, enforces source citations, and exports real-time telemetry to Prometheus and Grafana.

---

## 🎯 Problem & Solution
Internal documentation, troubleshooting playbooks, and architecture specs are usually scattered across repositories, leading to developer context-switching and delayed incident resolution. 

This assistant provides an enterprise search interface that:
- Answers queries using **exact internal runbook context** with source attribution.
- Implements strict fallback guardrails: if retrieved context does not match, it explicitly refuses to answer rather than hallucinating false commands[cite: 38].
- Operates under end-to-end telemetry (RPS, latency percentiles, error rates).

---

## 🏗️ Architecture & Data Flow

- **App Layer**: FastAPI serving `/query` and `/metrics` endpoints.
- **Vector Store**: ChromaDB indexing chunked internal documentation.
- **CI/CD Pipeline**: GitHub Actions workflow executing unit tests, building Docker images, and publishing to GHCR[cite: 37].
- **Kubernetes Orchestration**: Deployed on Minikube with `ClusterIP` services, container health probes, and Ingress routing[cite: 37].
- **Observability**: Prometheus scraping application metrics paired with a custom Grafana dashboard tracking real-time RPS and p95 latency percentiles[cite: 37].

---

## 📊 Live Observability & Load Benchmarks
Metrics instrumented via custom Prometheus middleware and graphed in Grafana[cite: 37]:

| Metric | Idle Baseline | Under Load (50 concurrent requests) |
| :--- | :--- | :--- |
| **p95 Latency** | **~95 ms – 100 ms**[cite: 20, 22] | **~1.00 s**[cite: 22] |
| **Throughput (RPS)** | ~0.06 req/s[cite: 20, 22] | Spikes cleanly to handle bursts[cite: 22] |
| **HTTP Error Rate** | 0.0% | 0.0% (Zero 5xx/4xx during load bursts) |

Exported dashboard definition: `k8s/rag-observability-dashboard.json`[cite: 51]

---

## 🧪 Verified API Response Sample

Request:
```bash
curl -X POST "http://localhost:8080/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does vector search work?"}'