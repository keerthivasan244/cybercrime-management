# AI-Powered Investigative Intelligence Platform

## Overview
This platform ingests raw evidence (text, PDFs, CSVs), extracts entities and relationships, resolves duplicate entities using fuzzy matching, builds a Neo4j Knowledge Graph, detects anomalies, and provides an AI Copilot for investigating the graph.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React + Tailwind + Cytoscape
- **Databases**: PostgreSQL (raw documents, extractions), Neo4j (Knowledge Graph)
- **AI/NLP**: SpaCy, scikit-learn, RapidFuzz, Gemini API

## Setup & Running
1. Set `GEMINI_API_KEY` in `docker-compose.yml` or your environment.
2. Run `docker-compose up --build -d` to start all services (Postgres, Neo4j, Backend, Frontend).
3. Access the Dashboard at `http://localhost:5173`.
4. Access the API at `http://localhost:8000/docs`.
5. Run the seed script: `docker-compose exec backend python seed.py`

## End-to-End Demo Walkthrough
1. **Ingest Evidence**: The seed script uploads 3 documents across 2 cases. You can also upload manually via the UI.
2. **Extraction & Resolution**: The backend automatically extracts entities (John Doe, Jane Smith, Blue Warehouse) and resolves aliases (John Doe / Johnathan Doe).
3. **Graph Construction**: The entities are synced to Neo4j.
4. **Network Analytics**: Go to the **Network Graph** tab in the UI to see the connections.
5. **Pattern Detection**: The dashboard shows anomalies, e.g., Jane Smith appearing across multiple documents.
6. **Copilot**: Go to the **Copilot** tab and ask: "Who connects John to the warehouse?" The AI will query the graph and provide an evidence-backed answer.
