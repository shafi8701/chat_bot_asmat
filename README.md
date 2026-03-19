# 🚀 Enterprise RAG System (Config-Driven + ETL)

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)

## 📖 Overview
Enterprise-grade Retrieval-Augmented Generation (RAG) system with ETL, evaluation, and logging.

## 🏗️ Architecture
Data → ETL → Chunking → Embeddings → Vector DB → RAG → LLM → Evaluation

## 🚀 Quick Start
```bash
docker compose down -v
docker compose up -d
docker compose run --rm chat_bot
docker compose run --rm etl_worker
```
