# 🚀 Enterprise RAG System (Config-Driven + ETL)

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Status](https://img.shields.io/badge/status-production--ready-success)

---

## 📖 Overview
Enterprise-grade **Retrieval-Augmented Generation (RAG)** system with:
- ETL pipeline
- Config-driven architecture
- Multi-LLM support
- Evaluation & logging

---

## 🏗️ Architecture

![Architecture](architecture_premium.png)

---

## ⚙️ Features
- 🔄 ETL pipeline for ingestion
- 🧠 Multi-LLM (OpenAI, Ollama)
- 📊 Evaluation framework
- 🧾 Logging & observability
- ⚙️ Config-driven behavior

---

## 🚀 Quick Start

```bash
docker compose down -v
docker compose up -d
docker compose run --rm chat_bot
docker compose run --rm etl_worker
```

---

## 📊 Evaluation
Logs stored in:
```
logs/rag_logs.json
```

---

## 📄 License
MIT License
