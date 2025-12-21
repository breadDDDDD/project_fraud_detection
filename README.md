# Fraud Assistant — RAG + SQL Analytics Chatbot

An AI-powered analytics and knowledge assistant that supports **conversational Q&A**, **Retrieval-Augmented Generation (RAG)**, and **SQL Intelligence**.  
Built with **Streamlit**, powered by **Gemini**, **Pinecone**, **Ollama embeddings**, and **SQL Server**, and fully containerized via **Docker Compose**.

---

## 🚀 What This App Does

This app allows you to:

- Chat conversationally with Gemini
- Ask questions over your documents using RAG
- Ask analytical questions backed by SQL Server
    - LLM generates SQL
    - Query executes
    - LLM explains results

All through a clean Streamlit interface.

---

## ✨ Features

- 🖥️ **Streamlit UI**
- 🤖 **Gemini LLM Responses**
- 📚 **RAG Pipeline with Pinecone**
- 🗄️ **SQL Execution + Result Summaries**
- 🧠 **Ollama Embedding Engine**
- 🐳 Fully Dockerized

---

## 🏗️ Architecture Overview

```
User
 │
 ▼
 Streamlit UI
 │
 ├── Normal Chat (Gemini)
 ├── RAG Mode (Gemini + Pinecone + Ollama embeddings)
 └── SQL Mode (Gemini → SQL → DB Query → Summary)
```

**Docker Compose Includes**
- App Container
- Ollama Embedding Server

**External Services**
- SQL Server
- Pinecone
- Gemini API

---

## ⚙️ Environment Setup

Create a **.env** file in the project root.

> 🔥 This is required or the app will NOT run.

### Required Variables

### 🔹 SQL Server
```
DB_URL=mssql+pyodbc://USERNAME:PASSWORD@host.docker.internal/DB_NAME?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=no
```

**Notes**
- Must use **SQL Authentication**
- Uses ODBC Driver 17
- `host.docker.internal` lets Docker access your host DB

---

### 🔹 Pinecone
```
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=fraud-docs
```

**Important**
- Index dimension must match embedding model  
  (for qwen embeddings → **1024**)

---

### 🔹 Gemini
```
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=your_preferred_gemini_model
```

---

### 🔹 Ollama Embeddings
```
OLLAMA_HOST=http://ollama:11434
OLLAMA_EMBED_MODEL=qwen3-embedding:0.6b
```

---

## 🐳 Run with Docker

### Prerequisites
- Docker Desktop installed
- SQL Server running
- .env properly configured

---

### 1️⃣ Build & Start
```
docker compose up --build
```

### 2️⃣ Start (next time)
```
docker compose up
```

### 3️⃣ Stop
```
docker compose down
```

---

## 🌍 Access the App
Visit:
```
http://localhost:8501
```

---

## 🤖 Verify Ollama Embeddings

Check installed models:
```
docker exec -it ollama curl http://localhost:11434/api/tags
```

You should see:
```
qwen3-embedding:0.6b
```

If missing, install manually:
```
docker exec -it ollama ollama pull qwen3-embedding:0.6b
```

---

## 🛠️ Local Development (No Docker)

If you prefer running locally:

### Install uv
```
pip install uv
```

### Create Virtual Environment
```
uv venv
```

Windows:
```
.venv/Scripts/activate
```

Mac/Linux:
```
source .venv/bin/activate
```

### Install Dependencies
```
uv pip install -r requirements.txt
```

### Run Streamlit
```
streamlit run streamlit_app.py
```

Update `.env`:
```
OLLAMA_HOST=http://localhost:11434
```

Open:
```
http://localhost:8501
```

---

## 🛡️ Security Notes

- `.env` is ignored via `.dockerignore`
- Secrets are **NOT baked** into the image
- Safe to push repo

---

## 🎉 What You Can Do

Once running, you can:
- 💬 Chat normally
- 📚 Switch to RAG mode for document Q&A
- 🧠 Use SQL mode for analytics insights
- 📄 Upload PDFs / Docs to build knowledgebase

Enjoy!
