# import packages
import sys
import re
import numpy as np
import pandas as pd

from sqlalchemy import create_engine

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger', 'stopwords'])

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

import pickle


def load_data(database_filepath):
    '''
    load the data from the sql database
    
    Input 
        database_filepath: path to database
    
    Returns
        X: predictors
        y: categories
        category_names: names of the categories
    '''
    #create sql engine
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql('SELECT * FROM DisasterMessages', engine)
    
    # create X and Y
    X = df['message']
    y = df.loc[:, 'related':'direct_report']
    # carete category names
    category_names = y.columns
    
    return X, y, category_names


def tokenize(text):
    '''
    process text to make it usable for ML
    
    Input
        text: column with the messages
    
    Returns
        clean_tokens: tokenized words extracted from each message
    '''
    # normalize
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    # tokenize and remove stopwords
    words = word_tokenize(text)
    tokens = [w for w in words if w not in stopwords.words('english')]
    # lemmatize and strip tokens
    lemmatizer = WordNetLemmatizer()
    
    clean_tokens = []
    for tok in tokens:
        c_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(c_tok)
    
    return clean_tokens


def build_model():
    '''
    creates the model 
    
    Input
        None
    
    Returns
        model: Pipeline using the best Hyperparameters from the GridSearch
    '''
    
    # model pipeline
    # pipeline_log = Pipeline([
    #    ('vect', CountVectorizer(tokenizer=tokenize)),
    #    ('tfidf', TfidfTransformer()),
    #    ('clf', MultiOutputClassifier(LogisticRegression()))
    # ])

    # check paramaters
    # pipeline_log.get_params().keys()
    
    # define parameters for GridSearchCV
    # parameters = {'clf__estimator__C': [0.01, 0.1, 1, 10, 100],
    #              'clf__estimator__solver': ['saga', 'lbfgs']
    #             }
        
    # create gridsearch object and return as final model pipeline
    # cv = GridSearchCV(pipeline_log, param_grid=parameters, n_jobs=-1, verbose=10)
    
    # since I allready did the GridSerach I can directly define a LogisticRegression with the best hyperparameters
    classifier = LogisticRegression(C=10, solver='saga', n_jobs=-2)
    
    # use the classifier in the pipeline
    model = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(classifier))
    ])
    
    return model


def evaluate_model(model, X_test, y_test, category_names):
    '''
    Input
        model: ML model
        X_test: massages to make predictions
        y_test: true categories for y
        category_names: name of the categories
    '''


    # use the model to make predictions from the test set
    y_pred = model.predict(X_test)

    # build DataFrame with predictions for each catehory
    y_pred_df = pd.DataFrame(data=y_pred, index=y_test.index, columns=category_names)

    # print output of classification report for each category
    print(classification_report(y_test, y_pred_df, target_names=category_names))


def save_model(model, model_filepath):
    '''
    saves the model as a pickle file to use it later, without training it again
    
    Input
        model: trained model
        model_filepath: where the model will be saved
    
    Returns
        None
    '''
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    '''
    Function to call main and start the script
    Expected Input from terminal:
        python train_classifier.py path_to_database pickle.pkl


    '''
    # check the len of the terminal imput
    if len(sys.argv) == 3:
        database_filepath = sys.argv[1]  
        model_filepath = sys.argv[2]

        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

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