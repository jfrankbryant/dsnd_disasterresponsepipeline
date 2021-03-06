#import libraries
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlite3
import re
import pickle
import nltk
nltk.download(['punkt', 'wordnet'])
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score, f1_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def load_data(database_filepath):
    """ Takes a database filepath.
    Returns dataframe from a table in the database and a lemmatizer.
    """
    engine = create_engine('sqlite:///' + database_filepath)
    conn = sqlite3.connect(database_filepath)
    df = pd.read_sql('SELECT * FROM categorized_messages', conn)
    X = df.message
    Y = df[['related', 'request', 'offer', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue',
       'security', 'military', 'child_alone', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people',
       'refugees', 'death', 'other_aid', 'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools',
       'hospitals', 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 'fire',
       'earthquake', 'cold', 'other_weather', 'direct_report']]

    return X, Y, list(Y.columns)



def tokenize(text):
    """ Takes text and returns tokens of single words."""
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens


def build_model():
    """Returns a GridSearchCV pipeline."""
    pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenize)),
            ('tfidf', TfidfTransformer(norm='l1')),
            ('clf', MultiOutputClassifier(AdaBoostClassifier(random_state=42)))
            ])

    parameters = {'vect__analyzer': ['word', 'char'],
                  'tfidf__norm': ['l1', 'l2'],
                  'clf__estimator': [AdaBoostClassifier(), KNeighborsClassifier()],
                  'clf__n_jobs': [1, 3]
}

    cv = GridSearchCV(pipeline, param_grid=parameters, verbose=3)

    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    """Prints out the classification report for the predicted Y values
    from the X test values.
    """
    y_pred = model.predict(X_test)

    print(classification_report(Y_test, y_pred, target_names=category_names))


def save_model(model, model_filepath):
    """Saves the fitted model above to use elsewhere."""
    #pickle export info from https://stackabuse.com/scikit-learn-save-and-restore-models/
    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)

def main():
    """This function was provided by Udacity.
    It utilizes the functions above to loads the clean data,
    builds the model, and make predictions.
    """
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
