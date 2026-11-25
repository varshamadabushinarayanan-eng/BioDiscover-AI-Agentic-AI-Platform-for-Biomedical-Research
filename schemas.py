from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ResearchRequest(BaseModel):
    disease: str = Field(..., min_length=2, description="Disease or biomedical condition")
    focus: Optional[str] = Field(default=None, description="Optional biological focus, e.g. neuroinflammation")
    max_records: int = Field(default=10, ge=1, le=50)

class EvidenceItem(BaseModel):
    record_id: str
    title: str
    source: str
    summary: str
    relevance_score: float
    evidence_label: str

class ResearchResponse(BaseModel):
    research_id: str
    disease: str
    focus: Optional[str]
    literature: List[Dict[str, Any]]
    graph: Dict[str, Any]
    evidence: List[Dict[str, Any]]
    hypothesis: Dict[str, Any]
    limitations: List[str]
