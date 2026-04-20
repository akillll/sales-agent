# 🚀 AI Sales Agent API

An AI-powered autonomous sales agent built using **FastAPI, LangGraph, and OpenAI**, capable of enriching leads, generating personalized cold emails, and handling objections with context-aware responses.

---

## 🧠 Overview

This project simulates a real-world AI sales system where:

* A prospect is enriched using LLM-based inference
* A personalized cold email is generated
* Replies are classified and handled intelligently
* The system maintains memory and traces all LLM interactions

---

## ⚙️ Tech Stack

* **FastAPI** — API layer (async, high-performance)
* **LangGraph** — Agent orchestration & state management
* **OpenAI API** — LLM for reasoning, generation, classification
* **Langfuse** — Observability & tracing
* **SQLAlchemy + SQLite** — Persistence & memory
* **Pydantic** — Request validation

---

## 🏗️ Architecture

```
Client → FastAPI → LangGraph Agent
                     ↓
        [Enrichment Node] (LLM JSON)
                     ↓
        [Email Generation Node]
                     ↓
        [Reply Classifier Node]
                     ↓
        ┌────────────┬────────────┬────────────┐
        ↓            ↓            ↓
   Objection     Positive     Neutral
     Node          Node         Node
```

---

## ✨ Features

### ✅ Core Features

* AI-based **prospect enrichment** (structured JSON)
* **Personalized cold email generation**
* **Reply classification** (positive / objection / neutral)
* Context-aware **objection handling**
* Stateful **agent workflow using LangGraph**

---

### 🔥 Advanced Features

* **Streaming responses** (real-time email generation)
* **Conversation memory** (DB-backed history)
* **Retry + timeout handling** for LLM reliability
* **Structured outputs** using OpenAI JSON mode
* **Langfuse tracing** for observability

---

## 📁 Project Structure

```
sales-agent/
├── main.py
├── agent/
│   ├── graph.py
│   ├── nodes.py
│   ├── state.py
│   ├── tools.py
│   ├── prompts.py
├── services/
│   ├── llm.py
│   └── observability.py
├── db/
│   ├── models.py
│   └── init_db.py
├── schemas.py
├── config.py
├── requirements.txt
└── .env
```

---

## 🚀 Setup Instructions

### 1. Clone & Setup

```bash
git clone <repo-url>
cd sales-agent
python -m venv venv
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_key
MODEL=gpt-4.1-mini

LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

### 4. Run Server

```bash
uvicorn main:app --reload
```

Open:
👉 http://127.0.0.1:8000/docs

---

## 🧪 API Usage

---

### 🔹 Generate Email

**POST /prospect**

```json
{
  "name": "John",
  "company": "Stripe"
}
```

**Response:**

```json
{
  "email": "...",
  "enrichment": {
    "role": "...",
    "industry": "...",
    "pain_points": ["..."]
  }
}
```

---

### 🔹 Handle Reply

**POST /reply**

```json
{
  "name": "John",
  "company": "Stripe",
  "reply": "Not interested right now"
}
```

**Response:**

```json
{
  "response": "...",
  "classification": {
    "type": "objection",
    "reason": "timing"
  }
}
```

---

### 🔹 Streaming Email

**POST /prospect/stream**

Returns real-time generated email.

---

## 📊 Observability (Langfuse)

* Automatic tracing of all LLM calls
* Node-level observability (`@observe`)
* Token usage + latency tracking
* Full request lifecycle visibility

---

## 🧠 Key Concepts

### 🔹 Structured Output

Uses OpenAI JSON mode to ensure reliable responses:

```python
response_format={"type": "json_object"}
```

---

### 🔹 Agent State

Shared memory across nodes:

```python
AgentState = {
  name,
  company,
  enrichment,
  email,
  reply,
  response,
  history
}
```

---

### 🔹 Conditional Routing

LangGraph routes based on reply classification:

* objection → objection_node
* positive → positive_node
* neutral → neutral_node

---

## ⚠️ Production Considerations

* Add caching for enrichment
* Implement rate limiting
* Add queue system (Celery / SQS)
* Store token usage for cost tracking
* Add prompt versioning + evaluation

---

## 🎯 What This Project Demonstrates

* AI agent orchestration using LangGraph
* Real-world LLM pipeline design
* Structured output handling
* Observability & tracing
* Backend system design for AI applications

---

## 📌 Future Improvements

* Prompt evaluation & scoring system
* A/B testing for prompts
* RAG (company knowledge enrichment)
* AWS deployment (ECS / Lambda)
* Multi-agent workflows

---

