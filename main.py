from fastapi import FastAPI, HTTPException
from .schemas import ResearchRequest
from .orchestrator import ResearchOrchestrator
from .data_access import graph_for_disease

app = FastAPI(
    title="BioDiscover AI",
    description="Educational agentic biomedical research prototype",
    version="0.1.0",
)
orchestrator = ResearchOrchestrator()

@app.get("/health")
def health():
    return {"status": "ok", "service": "BioDiscover AI", "mode": "local illustrative prototype"}

@app.post("/api/research")
def create_research(request: ResearchRequest):
    return orchestrator.run(request.disease, request.focus, request.max_records)

@app.get("/api/research/{research_id}")
def get_research(research_id: str):
    result = orchestrator.get(research_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Research run not found in this process")
    return result

@app.get("/api/knowledge-graph/{disease}")
def get_knowledge_graph(disease: str):
    return graph_for_disease(disease)
