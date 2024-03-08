"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""

from flask import Flask, request, render_template
import io
from ner import SpacyDocument

app = Flask(__name__)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        with io.open('input.txt', 'r', encoding='utf-8') as file:
            input_text = file.read()
        return render_template('form.html', input=input_text)
    else:
        text = request.form['text']
        doc = SpacyDocument(text)
        
        # NER part
        markup = doc.get_entities_with_markup()
        markup_paragraphed = ''
        for line in markup.split('\n'):
            if line.strip() == '':
                markup_paragraphed += '<p/>\n'
            else:
                markup_paragraphed += line
        
        # dependencies part
        parsed_sent_list = doc.get_dependencies_by_sentence()
        sentences = doc.get_sentences()
        return render_template('result.html', markup=markup_paragraphed, 
                               parsed_sent_list=parsed_sent_list, sentences=sentences)

# alternative where we use two resources

@app.route('/', methods=['GET'])
def index_get():
    with io.open('input.txt', 'r', encoding='utf-8') as file:
        input_text = file.read()
    return render_template('form.html', input=input_text)

@app.route('/', methods=['POST'])
def index_post():
    text = request.form['text']
    doc = SpacyDocument(text)
    
    # NER part
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line
    
    # dependencies part
    parsed_sent_list = doc.get_dependencies_by_sentence()
    sentences = doc.get_sentences()
    return render_template('result.html', markup=markup_paragraphed, 
                            parsed_sent_list=parsed_sent_list, sentences=sentences)

if __name__ == '__main__':

    app.run(debug=True)
