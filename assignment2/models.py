# thie module contains the SQLAlchemy model used in the application and a helper function 
# to create database entries from the NER and dependency parsing results.
from flask_sqlalchemy import SQLAlchemy
from typing import List, Tuple

db = SQLAlchemy()

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    ner_label = db.Column(db.String(50), nullable=False)
    head = db.Column(db.String(100), nullable=True)
    dependency_label = db.Column(db.String(50), nullable=True)
    child = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Entity('{self.text}', '{self.ner_label}', '{self.head}', '{self.dependency_label}', '{self.child}')"
    
    
def create_database_entries(entities: List[Tuple[int, int, str, str]], 
                          dependencies: List[Tuple[str, str, str]]) -> List[Entity]:
    """ 
    Helper method to create database entries from NER and dependency parsing
    """
    
    # get existing entities from the database
    existing_entities = Entity.query.all()
    existing_entities_set = {(entity.text, entity.ner_label, entity.head, entity.dependency_label, entity.child) 
                              for entity in existing_entities}
    all_entries = []
    for entity in entities:
        entity_text, entity_label = entity[3], entity[2]
        for dep in dependencies:
            entity_text_list = entity_text.split()
            if dep[2] in entity_text_list:
                head, dependency_label, child = dep[0], dep[1], dep[2]
                entry = (entity_text, entity_label, head, dependency_label, child)
                if entry not in existing_entities_set: # make sure to not add duplicates
                    entry_entity = Entity(
                        text=entity_text,
                        ner_label=entity_label, 
                        head=head,
                        dependency_label=dependency_label,
                        child=child
                    )
                    all_entries.append(entry_entity)
                    existing_entities_set.add(entry)
    return all_entries
