import os
import google.generativeai as genai
from neo4j_db import get_neo4j_session

# Check if GEMINI_API_KEY is available
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-pro') if gemini_api_key else None

def ask_copilot(question: str):
    """
    RAG over Knowledge Graph using Gemini.
    """
    if not model:
        return {"answer": "Error: GEMINI_API_KEY is not set. Cannot run copilot.", "citations": []}
    
    # 1. Translate question to Cypher
    prompt_1 = f"""
    You are an AI assistant for a criminal investigation platform.
    The Neo4j database has nodes like PERSON, ORGANIZATION, LOCATION, PHONE.
    Given the following user question, output ONLY a valid Cypher query to retrieve the relevant information.
    Do not output markdown, just the raw query.
    Question: {question}
    """
    
    try:
        cypher_response = model.generate_content(prompt_1)
        cypher_query = cypher_response.text.strip().replace('```cypher', '').replace('```', '').strip()
        
        # 2. Execute Cypher
        results = []
        with get_neo4j_session() as session:
            db_result = session.run(cypher_query)
            for record in db_result:
                results.append(str(record.data()))
                
        # 3. Generate Answer
        evidence_text = "\n".join(results)
        
        prompt_2 = f"""
        You are an AI investigation copilot.
        Answer the following question based ONLY on the retrieved database records below.
        If the records do not contain the answer, say "Insufficient evidence to answer this."
        Do NOT fabricate connections.
        
        Question: {question}
        
        Retrieved Database Records:
        {evidence_text}
        """
        
        final_response = model.generate_content(prompt_2)
        
        return {
            "answer": final_response.text,
            "citations": results,
            "cypher_used": cypher_query
        }

    except Exception as e:
        return {"answer": f"Error running copilot: {str(e)}", "citations": []}
