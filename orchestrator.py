from uuid import uuid4
from .agents import LiteratureAgent, KnowledgeGraphAgent, EvidenceAgent, HypothesisAgent

class ResearchOrchestrator:
    def __init__(self):
        self.literature = LiteratureAgent()
        self.graph = KnowledgeGraphAgent()
        self.evidence = EvidenceAgent()
        self.hypothesis = HypothesisAgent()
        self.results = {}

    def run(self, disease: str, focus: str | None = None, max_records: int = 10):
        records = self.literature.run(disease, focus, max_records)
        graph = self.graph.run(disease)
        evidence = self.evidence.run(records)
        hypothesis = self.hypothesis.run(disease, focus, evidence, graph)
        research_id = str(uuid4())
        result = {
            "research_id": research_id,
            "disease": disease,
            "focus": focus,
            "literature": records,
            "graph": graph,
            "evidence": evidence,
            "hypothesis": hypothesis,
            "limitations": [
                "The included records are illustrative portfolio data, not live literature search results.",
                "Evidence scoring is a simple demonstration heuristic and is not validated.",
                "Generated hypotheses are exploratory and do not establish causality or therapeutic efficacy.",
                "Human biomedical expert review and experimental validation are required.",
            ],
        }
        self.results[research_id] = result
        return result

    def get(self, research_id: str):
        return self.results.get(research_id)
