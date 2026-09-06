from sqlalchemy.orm import Session
import models
from sklearn.ensemble import IsolationForest
import numpy as np

def detect_anomalies(db: Session):
    """
    Detect anomalies in extracted entities.
    MVP: If we had structured transaction amounts, we'd run IsolationForest.
    Since we have text entities, we'll flag any entity that appears in many documents
    but wasn't expected, or rule-based flag 'bursts'.
    """
    # 1. Rule-based: Find entities that appear in > 3 different documents
    # (Mocking a 'high cross-case activity' flag)
    query = """
    SELECT entity_value, count(distinct document_id) as doc_count 
    FROM extracted_entities 
    GROUP BY entity_value 
    HAVING count(distinct document_id) > 2
    """
    
    # We will use SQLAlchemy core or ORM.
    # Let's do it via ORM grouping for simplicity.
    from sqlalchemy import func
    
    anomalies = []
    
    results = db.query(
        models.ExtractedEntity.entity_value, 
        func.count(func.distinct(models.ExtractedEntity.document_id)).label('doc_count')
    ).group_by(models.ExtractedEntity.entity_value).having(
        func.count(func.distinct(models.ExtractedEntity.document_id)) > 2
    ).all()
    
    for r in results:
        flag = models.AnomalyFlag(
            pattern_type="high_frequency_cross_document",
            description=f"Entity '{r.entity_value}' appears in {r.doc_count} distinct documents.",
            severity="Medium",
            evidence_ids=[] # In real app, query back for the exact entity IDs
        )
        db.add(flag)
        anomalies.append(flag)

    db.commit()
    
    return [
        {
            "id": a.id,
            "pattern_type": a.pattern_type,
            "description": a.description,
            "severity": a.severity
        } for a in anomalies
    ]
