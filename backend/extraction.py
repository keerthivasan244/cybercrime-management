import spacy
from typing import List, Dict

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not downloaded, download it (though Dockerfile handles it, local runs might need it)
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# We can also add a transformer for embeddings later in Phase 5
def extract_entities(text: str) -> List[Dict]:
    """
    Extract entities using SpaCy.
    Returns a list of dicts: {"type": str, "value": str, "context": str}
    """
    doc = nlp(text)
    entities = []
    
    # Simple mapping of SpaCy labels to our schema
    label_map = {
        "PERSON": "PERSON",
        "ORG": "ORGANIZATION",
        "GPE": "LOCATION",
        "LOC": "LOCATION",
        "FAC": "LOCATION",
        "DATE": "DATE",
        "MONEY": "MONEY"
    }
    
    for ent in doc.ents:
        if ent.label_ in label_map:
            # Grab context: the sentence containing the entity
            context = ent.sent.text.strip()
            entities.append({
                "type": label_map[ent.label_],
                "value": ent.text.strip(),
                "context": context,
                "confidence": 0.85 # Mock confidence for MVP
            })
            
    # Phone numbers and emails can be matched via regex or custom components.
    # For MVP, we'll stick to basic NER.
    
    return entities

def extract_relationships(text: str, entities: List[Dict]) -> List[Dict]:
    """
    MVP: Extracts relationships based on co-occurrence in sentences.
    Returns: [{"source": ent1, "target": ent2, "type": "CO_OCCURRED_WITH"}]
    """
    doc = nlp(text)
    relationships = []
    
    # A simple approach: if two entities are in the same sentence, they are related.
    # In a real app, use dependency parsing to find verbs (e.g., "called", "paid").
    for sent in doc.sents:
        sent_ents = [ent for ent in sent.ents if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "FAC", "MONEY"]]
        if len(sent_ents) > 1:
            for i in range(len(sent_ents)):
                for j in range(i + 1, len(sent_ents)):
                    e1 = sent_ents[i]
                    e2 = sent_ents[j]
                    relationships.append({
                        "source": e1.text.strip(),
                        "target": e2.text.strip(),
                        "type": "ASSOCIATED_WITH",
                        "context": sent.text.strip()
                    })
    return relationships
