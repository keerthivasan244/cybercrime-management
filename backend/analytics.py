from neo4j_db import get_neo4j_session

def get_centrality_metrics():
    """
    Returns nodes with highest degree centrality.
    In a full Neo4j setup, we'd use Graph Data Science (GDS) library.
    For MVP, we can calculate simple degree centrality via standard Cypher.
    """
    results = []
    query = """
    MATCH (n)-[r]-()
    RETURN id(n) as node_id, n.name as name, labels(n)[0] as type, count(r) as degree
    ORDER BY degree DESC
    LIMIT 10
    """
    with get_neo4j_session() as session:
        result = session.run(query)
        for record in result:
            results.append({
                "node_id": str(record["node_id"]),
                "name": record["name"],
                "type": record["type"],
                "degree": record["degree"]
            })
    return results
