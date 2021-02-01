# Disaster Response Pipeline Project

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/


###Motivation
This is a repository for my Udacity Data Scientist Nanodegree Project 2: Disaster Response Pipeline.

###Necessary Libraries
Sys
Pandas
Numpy
SQLAlchemy
JSON
Plotly
NLTK
Flask
Sklearn
SQLite3
RE
Pickle

###Files in the Repository w/ Summary
#####README.md: documentation file

#####App Folder
  run.py: contains the code to create the visualizations for the Flask app website
  templates folder
    go.html: code for message classification graphics
    master.html: code to create a page to insert training set message classification visualizations

#####Data Folder
  process_data.py: Python script to clean and load data into a SQLite3 database
  disaster_messages.csv: initial messages data
  disaster_categories.csv: initial categories data

#####Models Folder
  train_classifier.py: Python script to train a model on clean data taken from a SQLite3 database

#####Prep Folder
  pickle_disasterresponse_model.pkl: saved model
  ML Pipeline Preparation.ipynb: Jupyter notebook to work out machine learning pipeline
  messages.csv: initial messages data
  ETL Pipeline Preparation.ipynb: Jupyter notebook to work out a pipeline to clean and tidy the data
  categorized_disaster_response_messages.db: database of cleaned and tidied message and category data
  categories.csv: initial categories data

###Analysis Summary
This was a useful exercise to get used to creating ETL and ML pipelines. Also getting my feet wet with a multi-output classifier.

###Acknowledgements
Mihajlo Pavloski of Stack Abuse for the pickle help! (https://stackabuse.com/scikit-learn-save-and-restore-models/)
Udacity for the start code
