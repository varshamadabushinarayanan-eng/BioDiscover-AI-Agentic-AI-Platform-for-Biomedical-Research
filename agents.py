from .data_access import search_local_records, graph_for_disease

class LiteratureAgent:
    name = "literature_retrieval"
    def run(self, disease: str, focus: str | None, limit: int):
        return search_local_records(disease, focus, limit)

class KnowledgeGraphAgent:
    name = "knowledge_graph_exploration"
    def run(self, disease: str):
        return graph_for_disease(disease)

class EvidenceAgent:
    name = "evidence_analysis"
    def run(self, records: list[dict]):
        results = []
        for record in records:
            # Transparent demo heuristic only; not scientific evidence grading.
            score = 0.35
            if record.get("study_type") == "review":
                score += 0.10
            if record.get("source") in {"Europe PMC (illustrative record)", "PubMed (illustrative record)"}:
                score += 0.05
            score = min(score, 0.50)
            results.append({
                "record_id": record["id"],
                "title": record["title"],
                "source": record["source"],
                "summary": record["summary"],
                "relevance_score": round(score, 2),
                "evidence_label": "illustrative supporting context",
                "study_type": record.get("study_type", "not specified"),
            })
        return results

class HypothesisAgent:
    name = "hypothesis_generation"
    def run(self, disease: str, focus: str | None, evidence: list[dict], graph: dict):
        entities = sorted({
            node["id"] for node in graph.get("nodes", [])
            if node.get("type") not in {"Disease"}
        })
        focus_text = focus or "the biological mechanisms represented in the retrieved records"
        if evidence and entities:
            statement = (
                f"Research hypothesis for investigation: in {disease}, modulation of {focus_text} "
                f"may influence disease-relevant biology through one or more of these candidate entities: "
                f"{', '.join(entities[:5])}. This is a hypothesis for experimental testing, not an established mechanism."
            )
        else:
            statement = (
                f"Insufficient local evidence to generate a specific hypothesis for {disease}. "
                "Broaden the search terms or connect a live biomedical literature source."
            )
        return {
            "statement": statement,
            "supporting_record_ids": [item["record_id"] for item in evidence],
            "candidate_entities": entities[:10],
            "confidence": "low — illustrative local corpus; not clinically validated",
            "recommended_validation": [
                "Run a systematic literature search and review primary studies.",
                "Check for contradictory evidence and independent replication.",
                "Validate candidate relationships in appropriate experimental models.",
            ],
        }
