# OBD++

A multi-service OBD diagnostic backend built with FastAPI and Docker.

## Architecture
- api-service: handles client requests and data access
- ai-service: generates explanations using Gemini
- Supabase: stores diagnostic codes (REST API)

## Run locally
```bash
docker compose up --build
