# Assignment 1

## Requirements

The code assumes Python version 3.8 or higher. I used Python version 3.10.13.

The `requirements.txt` file contains all modules needed to run this code. To install them, run `pip install -r requirements.txt` in your terminal.


## FastAPI

### To run:

```bash
$ uvicorn app_fastapi:app --reload
```

### Accessing the API:

#### Getting information about the service:
```bash
$ curl http://127.0.0.1:8000
```

Using the pretty parameter:
```bash
$ curl http://127.0.0.1:8000?pretty=true
```

#### Perform named entity recognition on the text in `input.json`:

```bash
$ curl http://127.0.0.1:8000/ner -H "Content-Type: application/json" -d@input.json
```

Using the pretty parameter:
```bash
$ curl http://127.0.0.1:8000/ner?pretty=true -H "Content-Type: application/json" -d@input.json
```

#### Perform dependency parsing on the text in `input.json`:

```bash
$ curl http://127.0.0.1:8000/dep -H "Content-Type: application/json" -d@input.json
```

Using the pretty parameter:
```bash
$ curl http://127.0.0.1:8000/dep?pretty=true -H "Content-Type: application/json" -d@input.json
```


## Flask server

To run:

```bash
$ python --app app_flask.py
```

To access the website, point your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Streamlit

To run:

```bash
$ streamlit run app_streamlit.py
```

To access the website, point your browser at [http://localhost:8501](http://localhost:8501).