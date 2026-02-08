# OBDPlusCloud

A cloud-hosted, multi-service backend for automotive OBD-II diagnostics.  
The system receives diagnostic trouble codes (DTCs) and freeze-frame data, enriches them with database context, and generates human-readable explanations using an LLM.

This backend is designed to run **locally or on AWS EC2** using **Docker Compose**, with no code changes between environments.

---

## 🧠 Architecture Overview

The backend is split into two microservices:

### 1. API Service
- Public-facing FastAPI service
- Receives requests from the client
- Fetches DTC metadata from Supabase
- Calls the AI service for explanation generation
- Exposes `/explain` endpoint

### 2. AI Service
- Internal FastAPI service
- Generates explanations using the Gemini API
- Receives structured diagnostic context from the API service
- Returns formatted HTML explanations

### External Dependencies
- **Supabase**: PostgreSQL database (accessed via REST API)
- **Gemini API**: Large language model for explanation generation

---

## 📦 Tech Stack

- Python 3.12
- FastAPI
- Docker & Docker Compose
- AWS EC2 (Free Tier)
- Supabase
- Google Gemini API

---

## 📁 Repository Structure

```text
OBDPlusCloud/
├── api-service/
│   ├── main.py
│   ├── supabase_client.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── ai-service/
│   ├── main.py
│   ├── gemini_client.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml
└── README.md
```

---

## Run locally
```bash
docker compose up --build
