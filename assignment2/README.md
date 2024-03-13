# Assignment 2

## Requirements

The code assumes Python version 3.8 or higher. I used Python version 3.10.13.

The `requirements.txt` file contains all modules needed to run this code. To install them, run `pip install -r requirements.txt` in your terminal.

## Flask server

To run:

```bash
$ python app_flask.py
```

To access the website, point your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Database Functionality

In addition to the assignment requirements, I added an option to clear the database. This option is available when displaying the database via the "Clear database" button. If clicked, the user will be automatically redirected to the main page. If the user selects to see the database after clearing it, it will be displayed as empty.

Complete duplicates are not allowed in the database; however, the same entity can appear in the database more than once if other fields are different. 