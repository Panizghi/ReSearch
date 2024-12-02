from datetime import datetime
from ast import literal_eval
import numpy as np
import pandas as pd

def get_user_input():
    user_input = input("Enter key words: ")
    return user_input

def format_user_input(user_input):
    lower_user_input = user_input.lower()
    search_query = lower_user_input.replace(" ", "%20")
    return search_query
    
def convert_to_datetime(string):
    if string == 'no data':
        return 'no data'
    return datetime.strptime(string, "%Y-%m-%d")

def load_from_csv(data_path):
    df = pd.read_csv(data_path)
    df["key_words"] = df["key_words"].apply(literal_eval)
    return df

def flatten_list(list_to_flatten):
    return [item for sublist in list_to_flatten for item in sublist]

def clean_google_authors(df):
    authors_list = []
    for element in df.authors:
        authors_ = element.strip('et al.').split(',')
        authors = [authors_[1] + ' ' + authors_[0]]
        authors.extend(authors_[2:])
        authors_list.append(authors)
    return authors_list 