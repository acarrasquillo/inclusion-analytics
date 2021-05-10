# inclusion-analytics
Coding Assessment

# Requirements
- Python 3
- Python virtualenv
- Linux commandline

# DEV ENV SETUP
Set python environment to run the app
```
inclusion-analytics $ virtualenv -p PYTHON_EXE venv
inclusion-analytics $ source venv/bin/activate
(venv) inclusion-analytics $ cd analytics_app/
(venv) analytics_app $ pip install -r requirements.txt
```

Set Flask app environment variables
```
(venv) $ export FLASK_APP=analytics_app
(venv) $ export FLASK_ENV=development
```

# Initialize the app db
```
(venv) $ cd ..
(venv) inclusion-analytics $ flask init-db
...
...
Initialized the database
```

# Run the app
```
(venv) inclusion-analytics $ flask run
```

# Open the app on your webrowser
```
http://127.0.0.1:5000/
```