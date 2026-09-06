from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    source_type = Column(String) # pdf, docx, csv
    case_id = Column(String, index=True)
    content = Column(Text) # Extracted text
    metadata_json = Column(JSON, default={})
    ingestion_timestamp = Column(DateTime, default=datetime.utcnow)
    
    extracted_entities = relationship("ExtractedEntity", back_populates="document")

class ExtractedEntity(Base):
    __tablename__ = "extracted_entities"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    entity_type = Column(String, index=True) # PERSON, PHONE, VEHICLE, LOCATION, ORGANIZATION
    entity_value = Column(String, index=True)
    confidence = Column(Float, default=1.0)
    context = Column(Text) # The surrounding text where it was found
    
    resolved_entity_id = Column(Integer, ForeignKey("resolved_entities.id"), nullable=True)
    
    document = relationship("Document", back_populates="extracted_entities")
    resolved_entity = relationship("ResolvedEntity", back_populates="mentions")

class ResolvedEntity(Base):
    """Canonical entities after deduplication"""
    __tablename__ = "resolved_entities"
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, index=True)
    canonical_name = Column(String, index=True)
    attributes = Column(JSON, default={}) # Aliases, combined metadata
    
    mentions = relationship("ExtractedEntity", back_populates="resolved_entity")

class AnomalyFlag(Base):
    __tablename__ = "anomalies"
    id = Column(Integer, primary_key=True, index=True)
    pattern_type = Column(String, index=True) # e.g., 'burst_calls', 'structuring'
    description = Column(Text)
    severity = Column(String)
    evidence_ids = Column(JSON) # List of extracted entity or document IDs
    created_at = Column(DateTime, default=datetime.utcnow)
