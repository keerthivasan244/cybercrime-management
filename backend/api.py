from fastapi import APIRouter, UploadFile, File, Depends, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
import json

from database import get_db
import models
from ingestion import parse_pdf, parse_csv, parse_text
from extraction import extract_entities, extract_relationships

router = APIRouter()

def process_document_background(document_id: int, text: str, db: Session):
    # 1. Extraction
    entities = extract_entities(text)
    
    extracted_db_ents = []
    for e in entities:
        db_ent = models.ExtractedEntity(
            document_id=document_id,
            entity_type=e["type"],
            entity_value=e["value"],
            context=e["context"],
            confidence=e["confidence"]
        )
        db.add(db_ent)
        extracted_db_ents.append(db_ent)
    
    db.commit()
    # In a full app, we would also persist the relationships extracted here.
    # For now, we will wait until Phase 5 (Entity Resolution) and Phase 6 (Graph)
    # to persist relationships properly based on ResolvedEntities.

@router.post("/upload")
async def upload_evidence(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    case_id: str = Form(...),
    source_type: str = Form(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    extracted_text = ""
    metadata_json = {"original_filename": file.filename}

    if source_type == "pdf" or file.filename.endswith(".pdf"):
        extracted_text = parse_pdf(contents)
    elif source_type == "csv" or file.filename.endswith(".csv"):
        csv_data = parse_csv(contents)
        metadata_json["rows"] = len(csv_data)
        extracted_text = json.dumps(csv_data)
    else:
        extracted_text = parse_text(contents)

    doc = models.Document(
        filename=file.filename,
        source_type=source_type,
        case_id=case_id,
        content=extracted_text,
        metadata_json=metadata_json
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Kick off extraction in background
    background_tasks.add_task(process_document_background, doc.id, extracted_text, db)
    
    return {"message": "Evidence uploaded successfully", "document_id": doc.id, "extracted_length": len(extracted_text)}

from resolution import resolve_entities
from graph_builder import sync_to_neo4j, get_graph_data
from analytics import get_centrality_metrics
from anomalies import detect_anomalies
from copilot import ask_copilot
from pydantic import BaseModel

class CopilotQuery(BaseModel):
    question: str

@router.post("/resolve")
def run_resolution(db: Session = Depends(get_db)):
    count = resolve_entities(db)
    return {"message": f"Resolved {count} entities"}

@router.post("/sync_graph")
def run_graph_sync(db: Session = Depends(get_db)):
    count = sync_to_neo4j(db)
    return {"message": f"Synced {count} entities to graph"}

@router.get("/graph")
def fetch_graph():
    return get_graph_data()

@router.get("/analytics/centrality")
def fetch_centrality():
    return get_centrality_metrics()

@router.post("/anomalies/detect")
def run_anomaly_detection(db: Session = Depends(get_db)):
    results = detect_anomalies(db)
    return {"anomalies": results}

@router.post("/copilot/ask")
def copilot_ask(query: CopilotQuery):
    return ask_copilot(query.question)

@router.get("/documents")
def list_documents(case_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Document)
    if case_id:
        query = query.filter(models.Document.case_id == case_id)
    return query.all()
