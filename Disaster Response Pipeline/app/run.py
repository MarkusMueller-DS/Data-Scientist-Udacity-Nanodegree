import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Histogram
from sklearn.externals import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

def tokenize(text):
    '''
    tokenize message

    Input
        text: disaster message 

    Return
        clean_tokens: tokenized and lammatized wwords
    '''



    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterMessages', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    # get columns names and count for each catagory
    category_names = df.loc[:, 'related':'direct_report'].columns
    category_count = df.loc[:, 'related':'direct_report'].sum().values

    # get the lenggth of each diaster message 
    len_messages = df['message'].apply(len)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
            # GRAPH 1 - genre
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
            # GRAPH 2 - counts of catagories
        {
            'data': [
                Bar(
                    x=category_names,
                    y=category_count
                )
            ],

            'layout': {
                'title': 'Count of Categories',
                'yaxis': {
                    'title': 'Count'
                },
                'xaxis': {
                    'title': 'categories'
                }
            }
        },
            # GRAPH 3 - Histogram with len of message
        {
            'data': [
                Histogram(
                    x=len_messages,
                    nbinsx=500
                    )
                ],

            'layout': {
                'title': 'length of messages',
                'yaxis': {
                    'title': 'count'
                },
                'xaxis': {
                    'title': 'lenghth of messages' 
                }                   
            }
        }  
   ]

    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()