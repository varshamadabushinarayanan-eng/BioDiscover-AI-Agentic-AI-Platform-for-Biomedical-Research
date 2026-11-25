# BioDiscover AI — Agentic Biomedical Research Prototype

BioDiscover AI is a portfolio prototype for evidence-guided biomedical research and therapeutic-hypothesis exploration. It demonstrates a modular workflow:

1. **Literature agent** — retrieves relevant records from a small local example corpus.
2. **Knowledge-graph agent** — explores disease, gene, pathway and compound relationships.
3. **Evidence agent** — scores and labels supporting evidence, while preserving source identifiers.
4. **Hypothesis agent** — drafts a research hypothesis from the retrieved evidence.
5. **FastAPI service** — exposes the workflow through a REST endpoint.

## Important scope note

This downloadable version is a runnable **local prototype**. It uses a small, illustrative dataset and deterministic Python orchestration so it can run without API keys or external services. It does **not** make clinical recommendations, establish causality, or validate a therapeutic target. The Neo4j, ChromaDB, live literature APIs, LLM provider, LangGraph orchestration and React UI are documented as planned extension points, not falsely represented as active integrations.

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/api/research" \
  -H "Content-Type: application/json" \
  -d '{"disease":"Alzheimer disease","focus":"neuroinflammation"}'
```

## Project layout

```text
BioDiscover_AI/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI routes
│   ├── schemas.py           # Request/response models
│   ├── orchestrator.py      # Multi-step agent workflow
│   ├── agents.py            # Literature, graph, evidence, hypothesis agents
│   └── data_access.py       # Local corpus and graph access
├── data/
│   └── biomedical_records.json
├── tests/
│   └── test_workflow.py
├── .env.example
├── requirements.txt
└── README.md
```

## API endpoints

- `GET /health` — service health.
- `POST /api/research` — run the research workflow.
- `GET /api/research/{research_id}` — retrieve a saved in-memory result.
- `GET /api/knowledge-graph/{disease}` — return related graph nodes and edges.

## How the workflow works

The orchestrator passes a research request through each agent in sequence. The literature agent finds matching local records. The graph agent finds connected biomedical entities. The evidence agent summarizes the records and assigns a simple transparent evidence label. The hypothesis agent generates a cautious, testable research hypothesis and lists the evidence IDs that motivated it.

The current score is a **demo heuristic**, not a validated evidence-grading framework. A real system should assess study design, replication, species, sample size, bias, effect size, contradictory findings and publication quality.

## Next engineering steps

- Replace the local corpus with Europe PMC / PubMed retrieval and persist query metadata.
- Add embedding generation, chunking, ChromaDB indexing and retrieval evaluation (Recall@k, MRR, citation precision).
- Add Neo4j constraints, typed relationships and provenance-aware graph queries.
- Move orchestration to LangGraph with explicit state, retries, timeouts and human approval nodes.
- Connect an LLM through a secured provider adapter; require structured output and source-grounded claims.
- Add PostgreSQL persistence, authentication, audit logs, rate limits and observability.
- Build a React front end for research requests, evidence review and graph exploration.
- Add safety tests for prompt injection, unsupported claims, stale sources and missing evidence.

## Responsible-use statement

This is an educational research-support prototype. It is not a medical device and must not be used for diagnosis, treatment selection, patient management, clinical decisions or regulatory submissions. All hypotheses require independent expert review and experimental validation.
