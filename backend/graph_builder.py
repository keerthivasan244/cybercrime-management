from sqlalchemy.orm import Session
from neo4j_db import get_neo4j_session
import models

def sync_to_neo4j(db: Session):
    """
    Reads ResolvedEntities and writes them to Neo4j.
    In a real system, we'd also sync relationships.
    """
    resolved_entities = db.query(models.ResolvedEntity).all()
    
    with get_neo4j_session() as session:
        for ent in resolved_entities:
            # Cypher query to merge (create or update) the node
            label = ent.entity_type
            # Neo4j labels must be valid identifiers, we assume label is like 'PERSON'
            
            # Use MERGE to avoid duplicates
            query = f"""
            MERGE (n:{label} {{id: $id}})
            SET n.name = $name, n.aliases = $aliases
            """
            session.run(
                query, 
                id=str(ent.id), 
                name=ent.canonical_name, 
                aliases=ent.attributes.get("aliases", [])
            )
            
        # For relationships, we would iterate through documents, 
        # extract relationships between ResolvedEntities, and MERGE paths.
        # This is a simplified MVP sync.
        
    return len(resolved_entities)

def get_graph_data():
    """Fetches graph data for the frontend visualization."""
    nodes = []
    edges = []
    with get_neo4j_session() as session:
        # Get all nodes
        result = session.run("MATCH (n) RETURN id(n) as internal_id, labels(n)[0] as label, n")
        for record in result:
            n = record["n"]
            nodes.append({
                "data": {
                    "id": str(n.get("id")),
                    "label": n.get("name"),
                    "type": record["label"]
                }
            })
            
        # Get all relationships
        result = session.run("MATCH (a)-[r]->(b) RETURN a.id as source, b.id as target, type(r) as rel_type")
        for record in result:
            edges.append({
                "data": {
                    "source": str(record["source"]),
                    "target": str(record["target"]),
                    "label": record["rel_type"]
                }
            })
            
    return {"nodes": nodes, "edges": edges}
