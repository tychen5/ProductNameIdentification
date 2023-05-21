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
        'personal_access_token_name': 'enter_your_token_name',
        'personal_access_token_secret': 'enter_your_token_secret',
        'site_name': 'enter_your_site_name',
        'site_url': 'enter_your_site_url'
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
        file_path (str): Path to the GloVe file.

    Returns:
        list: List of words in the GloVe model.
    """
    en_vocabulary = []
    with open(file_path, 'r') as f:
        for line in f:
            split_line = line.split()
            word = split_line[0]
            en_vocabulary.append(word)
    return en_vocabulary

data_path = '/path/to/your/data/'
en_vocabulary = load_glove_model(data_path + 'glove.6B.50d.txt')

with open(data_path + 'stop_words_english.txt', 'r') as file:
    stop_words = file.read().splitlines()



bad_setli = ori_emfm_df['bad_names'].tolist()
bad_set = set.union(*bad_setli)

def filter_out_bad_set(ori_set, bad_set):
    """
    Filters out bad set from the original set and adds spaces to short tokens.

    Args:
        ori_set (set): The original set of tokens.
        bad_set (set): The set of bad tokens to be removed.

    Returns:
        list: The filtered list of tokens with spaces added to short tokens.
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
    # Add specific words for each product line
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

def process_fl_name(fl_name):
    all_words = [fl_name]
    if fl_name == 'unifi protect':
        all_words.extend([
            'ck gen 2', 'protect products', 'nvr', 'g3 cameras', 'doorbell camera',
            'for protect cam', 'flag protect', 'protects', 'protect deployments',
            'protect deployment', 'with protect', 'protect on', 'the protect',
            'protect is', 'protect instance', 'of protect', 'protect devices',
            'remove protect', 'protect location', 'protect app', 'in protect',
            'protect was', 'new protect', 'ubiquiti protect', 'unifi protect',
            'unvr4 protect', 'protect in cloud', 'protect in', 'protect keep',
            'protect keep', 'protect shows', 'protect amd64', 'protect android',
            'using protect', 'protect application', 'accessing protect',
            'protect without', 'protect should', 'into protect', 'protect claims',
            'protect setup', 'initial protect', 'and protect', 'protect wired',
            'unvr failed', 'protect beta', 'new protect', 'protect questions',
            'live view', 'disable protect', 'uninstalling protect',
            'protect compatibility', 'protect offsite', 'protect analytics',
            'protect that', 'protect not', 'under protect', 'protect config',
            'as protect', 'protect only', 'protect are', 'protect nvr',
            'protect live', 'limiting protect', 'protect access', 'by protect',
            'a protect', 'running protect', 'protect analytic', 'to protect',
            'protect conversion', 'protect being', 'protect clips',
            'protect notifications', 'ubiquiti unvr', 'local protect',
            'protect access', 'protect push', 'protect quality', 'protect no',
            'protect upload', 'of protect', 'protect on', 'laggy streams',
            'protect connection', 'adopted protect', 'my unvr', 'camera streams',
            'unvrs', 'unvr issue', 'unvr seems', 'in nvr', 'a unvr',
            'unvr protect', 'g4 door bell', 'ubiquiti door bell', 'nvrs', 'camera ir',
            'camera privacy zone', 'g5 cams', 'ai 360'
        ])
    elif fl_name == 'unifi talk':
        all_words.extend([
            'port delay', 'port process', 'talk port', 'unifi talk', 'talk phone', 'voicemail', 'talk groups', 'outgoing number',
            'call routing', 'call waiting', 'talk lines', 'incoming phone call', 'phones with talk', 'voicemail to email', 'incoming call group',
            'out going call', 'incoming call', 'transfer call', 'all talk traffic', 'smart attendant', 'talk attendant', 'phone extensions',
            'talk smart', 'talk number', 'attendant talk', 'talk smart', 'talk lines', 'talk attendant'
        ])
    elif fl_name == 'unifi network':
        all_words = [fl_name]
        all_words.extend([
            'usg', 'network', 'switch', 'switchs', 'switches', 'networking', 'networks',
            'vlan', 'vlans', 'routing', 'router', 'routers', 'sfp+', 'usg pro', 'uxg', 'uxg pro'
        ])
        all_words.extend([
            'network', 'vlan', 'vlans', 'networks', 'networking',
            'topology', 'cannot apply setting',
            'unifi switch', 'network app', 'unifi network', 'unifi ac', 'mesh', 'modem',
            'wifi', 'unifi ap',
            'poe switch', 'u6lr', 'uap', '24 poe', '6 pro',
            'ac pro', 'switch lite', '48 poe', 'lite 8',
            'port poe', 'poe switch', 'usg 3p', '24 port', 'usw', 'usw lite', 'gateway',
            'ap lr', 'uac ap', 'nanohd', 'ap lite', 'wall hd', 'ap nano', 'ac pro',
            'ac lite', 'ac longrange', '16 port', 'unifi 8', 'flex mini', 'ap ac',
            'in wall', 'usg pro', 'wifi6', 'mesh router', 'access point',
            'ac mesh', 'wifi 6', 'uap ac m', 'u6 mesh',
            'usg3p', 'aps', 'usg 3', 'usg3', 'usw poe', 'poe 24 switch',
            'u6 pro', 'u6 pro’s', "u6 pro's", 'ac pro', 'u6 enterprise',
            'nano hd', 'wifi',
            'flex', 'flex ap', 'ap settings',
            'unifi6', 'unifi6 extender', 'unify 6',
            'poes', 'u6 lr', 'nano hds', 'u6 pros', 'unify 6 enterprise ap', 'u6 ac', 'u6 iw',
            'nanobeam', 'wireless', 'unifi6 lite', 'usg3p', 'usg ikev2', 'unifi6 in wall',
            'unifi security gateway', 'security gateway', 'nano',
            'install nano', 'installing nano', 'u6 mesh', 'u6 mesh running', 'my usg',
            'smart queues', 'usg pro', 'u6 lr', 'usw 16 poe', 'uap6',
            'long range wifi6', 'my ap', 'usw', 'us 16 150', 'switches', 'usw pro 48 poe',
            'udw', 'switch', 'router', 'uap', 'u6 pro', 'aps', 'mesh', 'u6 lr operating',
            'confirming u6 lr', 'on flex switch', 'switch flex', 'unifi6 pro', 'unifi6 long range',
            'ac m', 'a unifi6 lite', 'unifi6 enterprise', 'flexxg',
            'the switches',
            'wifi experience', 'wifi experience graph', 'iptv on usg', 'uap ac pro',
            'ac pros', 'u6 lite', 'the u6 lite', 'u6 lite reset'
        ])
    elif fl_name == 'amplifi':
        all_words.extend(['amplifi', 'amplify'])
    elif fl_name == 'unifi led':
        all_words.extend(['lamps'])
    return all_words

data_path = '/path/to/your/data'
final_product_df = pd.DataFrame()

rows = []
for fl_name in fl_names:
    all_words = process_fl_name(fl_name)
    row = [fl_name, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, list(all_words)]
    rows.append(row)

final_product_df = final_product_df.append(pd.DataFrame(rows, columns=final_product_df.columns), ignore_index=True)
final_product_df.to_pickle(data_path + 'fm_em123_detect_finalproductdf.pkl')

new_em_df = pl_merge_df[['productline', 'detect_names']]  # EM2
new_em_df = new_em_df.dropna(subset='detect_names')
new_em_df = new_em_df.groupby('productline', as_index=False).agg(list)

import itertools

def construct_detect_set(nested_list):
    """
    Constructs a list of unique sets from a nested list of lists.
    
    Args:
        nested_list (list): A nested list of lists.
        
    Returns:
        list: A list of unique sets.
    """
    processed_set = []
    flattened_list = list(itertools.chain.from_iterable(nested_list))
    
    for single_list in flattened_list:
        single_set = set(single_list)
        if single_set not in processed_set:
            processed_set.append(single_set)
    
    return processed_set

# Assuming new_em_df is a DataFrame with a 'detect_names' column
new_em_df['detect_names'] = new_em_df['detect_names'].apply(construct_detect_set)

# Replace the path with your desired path
new_em_df.to_pickle('/path/to/your/notebooks/em2_detect_df.pkl')
