from collections import Counter

import streamlit as st
import pandas as pd
import altair as alt

from ner import SpacyDocument

example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")

st.markdown('## Spacy NLP Services')

# sitebar menu
with st.sidebar:
    st.header("Settings")
    st.write("Select view")
    settings_option = st.radio(
        "",
        ("Word Frequencies", "Named Entities", "Dependencies"),
        label_visibility="collapsed"
    )

st.markdown('### Text to process')
text = st.text_area('', value=example, height=150, label_visibility="collapsed")

doc = SpacyDocument(text)

if settings_option == "Word Frequencies":
    st.markdown('### Word Frequencies')
    
    tokens = doc.get_tokens()
    counter = Counter(tokens)
    words = list(sorted(counter.most_common(30)))
    
    # display word frequency statistics
    chart = pd.DataFrame({
        'frequency': [w[1] for w in words],
        'word': [w[0] for w in words]})
    bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')
    st.markdown(f'Total number of tokens: {len(tokens)}<br/>'
                f'Total number of types: {len(counter)}', unsafe_allow_html=True)
    
    # display word frequency bar chart
    st.altair_chart(bar_chart)
elif settings_option == "Named Entities":
    st.markdown('### Named Entities')
    
    # visualize named entities within the text
    entities = doc.get_entities()
    doc.visualize_ner()
    
    # display named entities in a table
    entities = pd.DataFrame(entities, columns=['Start Index', 'End Index', 'Entity Type', 'Entity Text'])
    st.table(entities)
elif settings_option == "Dependencies":
    st.markdown('### Dependencies')
    
    graph, table = st.tabs(["Graph", "Table"])

    with graph:
        # visualize dependencies as a graph
        doc.visualize_dependencies()
    with table:
        # visualize dependencies as a table
        dependencies = doc.get_dependencies_by_sentence()
        sentences = doc.get_sentences()
        for parsed_sent, sent in zip(dependencies, sentences):
            dependencies_df = pd.DataFrame(parsed_sent, columns=['Parent', 'Label', 'Child'])
            st.markdown(sent)
            st.table(dependencies_df)
    