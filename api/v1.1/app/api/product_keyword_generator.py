import pickle
import os
import sys
import pandas as pd
import numpy as np
import re
import itertools
import string
import inflect

data_path = '/path/to/your/data/'

zdhpc_df = pd.read_csv(data_path + 'Ubiquiti_Support_Zendesk_Fields_Historic_Problem_Device_Model.csv')
zdcpd_df = pd.read_csv(data_path + 'Ubiquiti_Support_Zendesk_Fields_Current_Problem_Device_Model_in_ZD.csv')
zdcfu_df = pd.read_csv(data_path + 'Ubiquiti_Support_Zendesk_Fields_Changes_for_UniFi_devices.csv')
psn_df = pd.read_csv(data_path + 'Product_SKU_and_NAME.csv')

sku_postfix = ['us', 'ea', 'beta', 'au', 'uk', 'bk', 'bl', 'blk', 'br', 'ca', 'eu', 'in',
               'jp', 'mx', 'tw', 'usa', 'cn', 'grey', 'au', 'black', 'silver', 'blu', 'gra',
               'camo', 'brick']


def chk_cols(df, colname_li):
    """
    Check if any column is NA/BLANK/null/none/nan, which will be considered an invalid row.
    """
    for col in colname_li:
        col_value = df[col]
        if pd.isnull(col_value) or pd.isna(col_value):
            return 0
        text = str(col_value).lower()
        if text in ['na', 'blank', 'null', 'none', 'nan']:
            return 0
    return 1


def clean_tag_sku(ori_text):
    """
    Clean the original text by removing words in (), removing 'prblm_', and removing bad words and multiple white spaces.
    """
    try:
        text = re.sub('\(.*?\)', '', ori_text.lower())
    except:
        return ori_text
    text = re.sub('prblm_', '', text)
    text_li = re.split('_|-|‑| ', text)
    text_li = [x for x in text_li if len(x) > 0 and x not in sku_postfix]
    return " ".join(text_li)


def clean_na(ori_text):
    """
    Convert na value to np.nan.
    """
    if pd.isnull(ori_text) or pd.isna(ori_text):
        return np.nan
    elif str(ori_text).lower() in ['na', 'blank', 'null', 'none', 'nan']:
        return np.nan
    else:
        return ori_text


def clean_df_rename(oridf, takecols, rename_cols, not_chk_col=[], clean_col=[]):
    """
    Clean the dataframe and rename the columns.
    """
    takedf = oridf[takecols]
    takedf.columns = rename_cols
    chk_col = list(set(rename_cols) - set(not_chk_col))
    takedf['keep'] = takedf.apply(lambda x: chk_cols(x, chk_col), axis=1)
    takedf = takedf[takedf['keep'] == 1].drop('keep', axis=1)
    for col in rename_cols:
        takedf[col] = takedf[col].apply(clean_na)
    for col in clean_col:
        takedf[col] = takedf[col].apply(clean_tag_sku)
    return takedf


zdhpc_df = clean_df_rename(zdhpc_df, ['1st Level Nesting', '2nd Level Nesting', '3rd Level Nesting',
                                      'Model SKU', 'tag'], ['first_level', 'second_level', 'third_level', 'sku', 'tag'],
                           not_chk_col=['third_level'], clean_col=['sku', 'tag'])
zdcpd_df = clean_df_rename(zdcpd_df, ['1st level nest', '2nd level nest',
                                      '3rd level nest', 'tag'], ['first_level', 'second_level', 'third_level', 'tag'],
                           not_chk_col=['third_level'], clean_col=['tag'])
zdcfu_df = clean_df_rename(zdcfu_df, ['1st Level Nesting', '2nd Level Nesting', 'tag'], ['first_level', 'second_level', 'tag'],
                           clean_col=['tag'])
psn_df = clean_df_rename(psn_df, ['Name', 'Sku'], ['store_name', 'sku'], clean_col=['sku'])


import itertools
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def construct_keywords(level_targetcolname_doc, target_col_name):
    """
    Construct unique terms tfidf as keywords of the target_col_name.
    
    Args:
        level_targetcolname_doc (DataFrame): Input DataFrame.
        target_col_name (str): Target column name.
    
    Returns:
        dict: keys=target_col_name(level's name), value=(list of strings)explode_col_name's keywords.
    """
    corpus = level_targetcolname_doc['doc'].tolist()
    vectorizer = TfidfVectorizer(min_df=0.0)
    Z = vectorizer.fit_transform(corpus)
    tfidf_df = pd.DataFrame(Z.toarray(), columns=vectorizer.get_feature_names(),
                            index=level_targetcolname_doc[target_col_name].tolist())
    keyword_dict = {}
    for name in tfidf_df.index:
        keyword_dict[name] = []

    def get_keywords(series, keyword_dict=keyword_dict):
        take = series[series == series.max()]
        not_take = series[series == series.min()]
        if len(take) == 1 and len(not_take) == len(keyword_dict) - 1:
            tmp = keyword_dict[take.index[0]].copy()
            tmp.append(take.name)
            keyword_dict[take.index[0]] = tmp
        return np.array(list(keyword_dict.values()), dtype=object)

    try:
        tmpdf = tfidf_df.apply(lambda x: get_keywords(x), axis=0)
    except:
        return keyword_dict
    tfidf_df['keyword_list'] = tmpdf[tmpdf.columns[-1]]
    return keyword_dict

# Replace 'data_path' with the path to your data
data_path = '/path/to/your/data/'

# Load the data
final_product_df = pd.read_pickle(data_path + 'combined_product_df.pkl')

# Replace the following lines with the appropriate function calls and variable assignments
first_level_tagsku_doc = prepare_data(final_product_df, 'first_level', 'tag_sku')
first_level_storename_doc = prepare_data(final_product_df, 'first_level', 'store_name')

first_level_tagsku_keword_di = construct_keywords(first_level_tagsku_doc, 'first_level')
first_level_storename_keyword_di = construct_keywords(first_level_storename_doc, 'first_level')
