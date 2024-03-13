"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""

from flask import Flask, request, render_template, redirect, url_for
import io
from ner import SpacyDocument
from models import db, Entity, create_database_entries

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# initialize the SQLAlchemy database
db.init_app(app)


# For the website we use the regular Flask functionality and serve up HTML pages.

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        with io.open('input.txt', 'r', encoding='utf-8') as file:
            input_text = file.read()
        return render_template('main.html', input=input_text)
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
        parsed_sent_list, all_dependencies = doc.get_dependencies_by_sentence()
        
        # create and populate the database
        database_entries = create_database_entries(doc.get_entities(), all_dependencies)
        for entry in database_entries:
            db.session.add(entry)
        db.session.commit()
        
        sentences = doc.get_sentences()
        return render_template('result.html', markup=markup_paragraphed, 
                               parsed_sent_list=parsed_sent_list, sentences=sentences)
        
@app.route('/database')
def display_database():
    entities = Entity.query.all()
    return render_template('database.html', entities=entities)

@app.route('/clear_database', methods=['POST'])
def clear_database():
    # delete all entries from the database
    Entity.query.delete()
    db.session.commit()
    
    # redirect back to the main page
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
