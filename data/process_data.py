# import libraries
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """Returns two dataframes: one for messages and the other with the categories."""
    messages = pd.read_csv(messages_filepath)
    category_column_names = pd.read_csv(categories_filepath, nrows=1)
    category_column_names = category_column_names.categories.str.split(";",expand=True)
    category_column_names = category_column_names.iloc[0].str.rstrip('-01').tolist()
    categories = pd.read_csv(categories_filepath, sep=';', names= category_column_names)

    return messages, categories

def clean_data(messages_df, categories_df):
    """Returns a merged, cleaned dataframe."""
    categories_df[['id','related']] = categories_df.related.str.split(",",expand=True)
    categories_df.drop(0, inplace=True)
    categories_df = categories_df.reset_index(drop=True)
    for column in categories_df:
    # set each value to be the last character of the string
        categories_df[column] = categories_df[column].str.lstrip("abcdefghijklmnopqrstuvwxyz_-") #can [-1] be used instead of lstrip? yes but it's less exact and causes other issues

    # convert column from string to interger
        categories_df[column] = categories_df[column].astype(int)
    df = messages_df.merge(categories_df, how="outer", on='id')
    drop_indices = list(df.loc[df['related'] == 2].index)
    df.drop(drop_indices, inplace=True)
    df = df.reset_index(drop=True)
    df = df.drop_duplicates()

    return df


def save_data(df, database_filename):
    """Create a SQLite database and save the cleaned dataframe as a table."""
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('categorized_messages', engine, index=False)

    return engine


def main():
    """This function was provided by Udacity.
    It utilizes the functions above to load, clean, and save the data.
    It was modified based on how the data gets cleaned.
    """
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        messages, categories = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(messages, categories)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

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
