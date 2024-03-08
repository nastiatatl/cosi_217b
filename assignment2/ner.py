"""ner.py

Run spaCy NER over an input string and insert XML tags for each entity.

"""

import io
import spacy
from spacy_streamlit import visualize_parser, visualize_ner
from typing import Callable, List, Tuple

nlp = spacy.load("en_core_web_sm")

class SpacyDocument:

    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)

    def get_tokens(self) -> List[str]:
        return [token.lemma_ for token in self.doc]
    
    def get_sentences(self) -> List[str]:
        return [sent.text for sent in self.doc.sents]

    def get_entities(self) -> List[Tuple[int, int, str, str]]:
        entities = []
        for e in self.doc.ents:
            entities.append((e.start_char, e.end_char, e.label_, e.text))
        return entities
    
    def get_dependencies(self, doc: str) -> List[Tuple[str, str, str]]:
        # helper method to get dependencies for a single sentence
        dependencies = []
        doc = nlp(doc)
        for token in doc:
            parent = token.head.text
            child = token.text
            label = token.dep_
            dependencies.append((parent, label, child))
        return dependencies
    
    def get_dependencies_by_sentence(self) -> List[List[Tuple[str, str, str]]]:
        sentences = []
        for sent in self.doc.sents:
            sentences.append(self.get_dependencies(sent.text))
        return sentences
    
    def visualize_dependencies(self) -> Callable[..., None]:
        return visualize_parser(self.doc, title=None)    
    
    def visualize_ner(self) -> Callable[..., None]:
        return visualize_ner(self.doc, title=None, show_table=False)       

    def get_entities_with_markup(self) -> str:
        entities = self.doc.ents
        starts = {e.start_char: e.label_ for e in entities}
        ends = {e.end_char: True for e in entities}
        buffer = io.StringIO()
        for p, char in enumerate(self.text):
            if p in ends:
                buffer.write('</entity>')
            if p in starts:
                buffer.write('<entity class="%s">' % starts[p])
            buffer.write(char)
        markup = buffer.getvalue()
        return '<markup>%s</markup>' % markup

if __name__ == '__main__':

    example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn't "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")

    doc = SpacyDocument("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously.")
    print(doc.get_tokens())
    for entity in doc.get_entities():
        print(entity)
    
