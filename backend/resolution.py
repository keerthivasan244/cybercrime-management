from sqlalchemy.orm import Session
from rapidfuzz import fuzz
import models

FUZZY_THRESHOLD = 85.0

def resolve_entities(db: Session):
    """
    Finds all unresolved ExtractedEntities and attempts to map them
    to existing ResolvedEntities or creates new ones.
    """
    unresolved = db.query(models.ExtractedEntity).filter(models.ExtractedEntity.resolved_entity_id == None).all()
    
    for extracted in unresolved:
        # We only compare with the same entity type
        existing_resolved = db.query(models.ResolvedEntity).filter(models.ResolvedEntity.entity_type == extracted.entity_type).all()
        
        best_match = None
        best_score = 0
        
        for resolved in existing_resolved:
            # Fuzzy match the names
            score = fuzz.ratio(extracted.entity_value.lower(), resolved.canonical_name.lower())
            
            # For MVP, we can also check aliases if stored in attributes
            # aliases = resolved.attributes.get("aliases", [])
            # for alias in aliases:
            #     alias_score = fuzz.ratio(extracted.entity_value.lower(), alias.lower())
            #     if alias_score > score: score = alias_score

            if score > best_score:
                best_score = score
                best_match = resolved
                
        if best_match and best_score >= FUZZY_THRESHOLD:
            # Link to existing
            extracted.resolved_entity_id = best_match.id
            
            # Optionally add to aliases if not exact
            if extracted.entity_value.lower() != best_match.canonical_name.lower():
                aliases = best_match.attributes.get("aliases", [])
                if extracted.entity_value not in aliases:
                    aliases.append(extracted.entity_value)
                    best_match.attributes["aliases"] = aliases
                    # force update
                    db.add(best_match)
        else:
            # Create new canonical entity
            new_resolved = models.ResolvedEntity(
                entity_type=extracted.entity_type,
                canonical_name=extracted.entity_value,
                attributes={"aliases": [extracted.entity_value], "first_seen_context": extracted.context}
            )
            db.add(new_resolved)
            db.commit() # Commit to get ID
            db.refresh(new_resolved)
            extracted.resolved_entity_id = new_resolved.id
            
        db.add(extracted)
    
    db.commit()
    return len(unresolved)
