# Portfolio AI Backend

A complete production-ready AI agent backend system built with **FastAPI**, **LangGraph**, and **HuggingFace**, designed specifically for portfolio websites.

## 🌟 Features
* **Conversational AI Agent**: Uses `gemma-3-27b-it` via HuggingFace for intelligent responses.
* **Short-Term Memory**: Strict 20-message sliding window persisted in MongoDB (no long-term tracking).
* **Local RAG Pipeline**: Ingests portfolio documents and GitHub repos into a local **ChromaDB** using `sentence-transformers` for free vector search.
* **Tool Calling**:
  * `send_email`: Sends real emails to the owner using Gmail SMTP.
  * `download_resume`: Provides links to the owner's resume.
  * `navigate_page`: Returns structured routing information for the frontend.
* **Human-in-the-Loop Escalation**: Automatically detects ambiguous queries or requests to talk to a human and flags them.
* **LangSmith Tracing**: Integrated observability for agent actions.

## 🛠 Tech Stack (100% Free Tier Compatible)
* **Backend Framework**: FastAPI
* **Agent Orchestration**: LangGraph / LangChain
* **LLM**: Google Gemma 3 (via HuggingFace Serverless API)
* **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (Local/CPU)
* **Vector DB**: ChromaDB (Local Persistent)
* **Chat Memory DB**: MongoDB Atlas (Free Tier M0)

## 📁 Project Structure
```text
backend/
├── agents/          # LangGraph agent setup, prompts, and escalation logic
├── config/          # Pydantic settings, DB connections, LLM clients
├── controllers/     # API request handlers
├── memory/          # MongoDB short-term memory logic
├── rag/             # Local chunking, embedding, and ChromaDB retrieval
├── routes/          # FastAPI route definitions
├── scripts/         # Data ingestion scripts (Docs + GitHub)
├── services/        # Auxiliary services (like tool execution logging)
├── tools/           # LangChain @tool definitions
└── main.py          # FastAPI application entry point
```

## 🚀 Setup & Installation

### 1. Prerequisites
* Python 3.10+
* MongoDB URI (Atlas or Local)
* HuggingFace API Key
* LangSmith API Key (Optional but recommended)

### 2. Install Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the template and fill in your keys:
```bash
cp .env.example .env
```

### 4. Data Ingestion (RAG)
Put your data in the `data/` folder (e.g., `resume.txt`, `projects.md`), then run:
```bash
python scripts/ingest_documents.py
```
*(Optional) To ingest from your GitHub repos:*
```bash
python scripts/ingest_github.py
```

### 5. Run the Server
```bash
uvicorn main:app --reload
```
The server will run at `http://localhost:8000`.

## ⚡ API Endpoints

### `POST /api/chat`
Main endpoint to talk to the agent.
**Request**:
```json
{
  "userId": "user-1234",
  "message": "Can you show me Tushar's latest projects?"
}
```
**Response**:
```json
{
  "reply": "Here are some of Tushar's latest projects...",
  "toolCalled": null,
  "toolResult": null,
  "escalated": false,
  "metadata": {
    "ragChunks": 3,
    "memoryLength": 2,
    "model": "gemma-3-27b-it"
  }
}
```

### `GET /api/health`
Checks if the server and MongoDB are online.
