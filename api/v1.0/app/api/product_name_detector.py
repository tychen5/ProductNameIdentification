
import pandas as pd
import numpy as np
import pickle
import datetime as dt
import itertools
import re
import string
import inflect
from collections import Counter
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import querying, flatten_dict_column

data_path = '/path/to/your/data/'
tableau_server_config = {
    'my_env': {
        'server': 'https://your-tableau-server-url',
        'api_version': '3.10',
        'personal_access_token_name': 'your_personal_access_token_name',
        'personal_access_token_secret': 'your_personal_access_token_secret',
        'site_name': 'your_site_name',
        'site_url': 'your_site_url'
    }
}

conn = TableauServerConnection(tableau_server_config, env='my_env')
conn.sign_in()

site_views_df = querying.get_views_dataframe(conn)
site_views_detailed_df = flatten_dict_column(site_views_df, keys=['name', 'id'], col_name='workbook')
relevant_views_df = site_views_detailed_df[site_views_detailed_df['workbook_name'] == 'Product Name List']
table_id = relevant_views_df[relevant_views_df['name'] == 'Product SKU and NAME']['id'].to_list()[0]
store_raw_data = querying.get_view_data_dataframe(conn, view_id=table_id)
store_productname_save_path = data_path + 'productline_keywords_df.pkl'
shopify_export_data_us = data_path + 'products_export_us.csv'


import itertools
import pickle
import re
import pandas as pd

def load_glove_model(file_path):
    """
    Load GloVe model from a file.

    Args:
        file_path (str): Path to the GloVe model file.

    Returns:
        list: List of words in the GloVe model.
    """
    vocabulary = []
    with open(file_path, 'r') as f:
        for line in f:
            split_line = line.split()
            word = split_line[0]
            vocabulary.append(word)
    return vocabulary

# Replace the following path with the path to your GloVe model file
glove_model_path = '/path/to/your/glove_model_file'
en_vocabulary = load_glove_model(glove_model_path)

# Replace the following path with the path to your stop words file
stop_words_path = '/path/to/your/stop_words_file'
with open(stop_words_path, 'r') as file:
    stop_words = file.read().splitlines()


# Replace the following paths with the paths to your data files
data_path = '/path/to/your/data_path'
store_productname_save_path = '/path/to/your/store_productname_save_path'


def filter_out_bad_set(ori_set, bad_set):
    """
    Filters out bad set from the original set and appends space if the token length is less than or equal to 5.

    Args:
        ori_set (set): The original set of tokens.
        bad_set (set): The set of bad tokens to be removed.

    Returns:
        list: The filtered list of tokens.
    """
    taken = []
    li = sorted(ori_set - bad_set)
    for token in li:
        token = token.replace('-', ' ')
        if len(token) > 5:
            taken.append(token)
        else:
            taken.append(token + ' ')
            taken.append(' ' + token)
    return taken


ori_emfm_df['detect_names2'] = ori_emfm_df['detect_names2'].apply(filter_out_bad_set)
ori_emfm_df = ori_emfm_df[['productline', 'detect_names2']]
emfm_di = ori_emfm_df.set_index('productline')['detect_names2'].to_dict()
dont_take_names = ["unifi", 'cameras', 'connect']
fl_names = final_product_df['first_level'].value_counts().index.tolist()
fl_names.extend(list(emfm_di.keys()))
fl_names = sorted(set(fl_names))
pl_nouns = ['consoles', 'accessories']
pl_si = inflect.engine()
rows = []

for fl_name in fl_names:
    all_words = [fl_name]
    # Add more words based on the first level name
    # ...

    try:
        all_words.extend(emfm_di[fl_name])
    except KeyError:
        pass

    try:
        convertli = fl_convert_dict[fl_name]
    except KeyError:
        pass

    if len(console_li) > 0:
        for productline in convertli:
            try:
                bad_set = bad_em1_di[productline]
            except KeyError:
                pass
            all_words = set(all_words) - set(bad_set)

    row = [fl_name, np.nan, np.nan, np.nan, np.nan, np.nan, list(all_words), np.nan]
    rows.append(row)

final_product_df = final_product_df.append(pd.DataFrame(rows, columns=final_product_df.columns), ignore_index=True)
dont_take_names = ["unifi", 'connect']
rows = []

for fl_name in fl_names:
    all_words = [fl_name]
    pl_words = fl_name.split(" ")
    pl_words = [w for w in pl_words if w not in dont_take_names]
    all_words.extend(pl_words)
    # Add more words based on the first level name

import itertools


def construct_detect_di(lilili):
    """
    This function takes a list of lists of lists and returns a list of unique sets
    created from the innermost lists.

    Args:
        lilili (list): A list of lists of lists.

    Returns:
        list: A list of unique sets created from the innermost lists.
    """
    processed_set = []
    twod_li = list(itertools.chain.from_iterable(lilili))
    for oned_li in twod_li:
        oned_set = set(oned_li)
        if oned_set not in processed_set:
            processed_set.append(oned_set)
    return processed_set


# Replace the following line with the actual path to your DataFrame
data_path = "/path/to/your/data/"

# Assuming new_em_df is a DataFrame with a 'detect_names' column
new_em_df["detect_names"] = new_em_df["detect_names"].apply(construct_detect_di)

# Save the modified DataFrame to a pickle file
new_em_df.to_pickle(data_path + "em2_detect_df.pkl")