# import packages
import sys
import numpy as np
import pandas as pd

from sqlalchemy import create_engine


def load_data(data_messages, data_categories):
    '''
    load the data, cleans and stores it in a SQL Datapase
    
    Input
        disater messages: dataset with the messages as a csv
        categories of messages: dataset with the caegories as a csv
    
    Returns
        df 
    '''
    # read in file
    messages = pd.read_csv(data_messages)
    categories = pd.read_csv(data_categories)
   
    # clean data
    # merge data
    df = messages.merge(categories, on='id')

    return df
    
def clean_data(df):
    '''
    Function to clean the DataFrames

    Input
        df: clean df

    Retrun
        df
    '''
    # create column for each cat
    categories = df['categories'].str.split(';', expand=True)
    row = categories.loc[0]
    category_colnames = row.apply(lambda x: x.split('-')[0])
    categories.columns = category_colnames
    # remove text in cat columns
    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = categories[column].astype(int)
        
    # replace '2' in the related column
    categories['related'].replace(2, 1, inplace=True)
    
    # drop categories in original df
    df = df.drop(columns='categories')
    # concat
    df = pd.concat([df, categories], axis=1)
    # remove duplicates
    df.drop_duplicates(inplace=True)

    return df
    

def save_data(df, database_filename):
    '''
    Saves the cleaned DataFrame in a sqllite database

    Input
        df: cleand DataFrame
        database_filnaame: name of the database 
    '''

    # load to database
    engine = create_engine(f'sqlite:///{database_filename}')
    df.to_sql(database_filename, engine, index=False, if_exists='replace')


def main():
    '''
    Function to call main and start the script
    
    Expected Input from terminal:
        python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db
    
    '''
    # check the len of the terminal imput
    if len(sys.argv) == 4:
        data_messages = sys.argv[1]
        data_categories = sys.argv[2]
        database_filename = sys.argv[3]      
        
        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(data_messages, data_categories))
        df = load_data(data_messages, data_categories)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filename))
        save_data(df, database_filename)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()