import json
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "biomedical_records.json"

def load_records() -> list[dict[str, Any]]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def search_local_records(disease: str, focus: str | None = None, limit: int = 10):
    terms = [disease.lower()]
    if focus:
        terms.append(focus.lower())
    records = load_records()
    scored = []
    for record in records:
        haystack = " ".join([
            record.get("title", ""),
            record.get("disease", ""),
            record.get("summary", ""),
            " ".join(record.get("entities", [])),
        ]).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            scored.append((score, record))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:limit]]

def graph_for_disease(disease: str):
    records = load_records()
    nodes, edges = {}, []
    target = disease.lower()
    for record in records:
        if target not in record.get("disease", "").lower():
            continue
        disease_name = record["disease"]
        nodes[disease_name] = {"id": disease_name, "type": "Disease"}
        for entity in record.get("entities", []):
            entity_type = record.get("entity_types", {}).get(entity, "BiomedicalEntity")
            nodes[entity] = {"id": entity, "type": entity_type}
            edges.append({"source": disease_name, "target": entity, "relation": "associated_with",
                          "source_record": record["id"]})
    return {"nodes": list(nodes.values()), "edges": edges}
