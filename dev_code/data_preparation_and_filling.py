import itertools
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def prepare_data(final_product_df, target_col_name, explode_col_name, tcn_str=True):
    """
    Prepare data for further processing.

    Args:
        final_product_df (DataFrame): The input DataFrame.
        target_col_name (str): The column name to fill missing values.
        explode_col_name (str): The column name to find keywords.
        tcn_str (bool, optional): If target column name's values is string. Defaults to True.

    Returns:
        DataFrame: The processed DataFrame.
    """
    if tcn_str:
        level_df = final_product_df[~final_product_df[target_col_name].isna()]
        level_targetcol_name = level_df[~level_df[explode_col_name].isna()]
        level_targetcol_name = level_targetcol_name[[target_col_name, explode_col_name]]
        level_targetcolname_doc = level_targetcol_name.explode(explode_col_name)
        level_targetcolname_doc = level_targetcolname_doc.groupby([target_col_name], as_index=False).agg(list)
        level_targetcolname_doc['doc'] = level_targetcolname_doc[explode_col_name].apply(lambda x: " ".join(x))
        return level_targetcolname_doc


def construct_keywords(level_targetcolname_doc, target_col_name):
    """
    Construct unique terms tfidf as keywords of the target_col_name.

    Args:
        level_targetcolname_doc (DataFrame): The input DataFrame.
        target_col_name (str): The target column name.

    Returns:
        dict: A dictionary with keys as target_col_name(level's name) and values as list of strings (explode_col_name's keywords).
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


def fill_firstlevel(first_level, tag_sku, store_name, keyword_dict, keyword_dict_store):
    # Your implementation here
    pass


def clean_sl(li, tag_sku_li):
    # Your implementation here
    pass


def fill_secondlevel(first_level, second_level, tag_sku, store_name, keyword_dict, keyword_dict_store, flsl_corr_di=None):
    # Your implementation here
    pass


def fill_secondlevel(first_level, second_level, third_level, tag_sku, store_name, keyword_dict, keyword_dict_store,
                     flsl_corr_di=None, sltl_corr_di=None):
    # Your implementation here
    pass


# Example usage
final_product_df = pd.read_pickle('../data/combined_product_df_fillpartlevelna.pkl')

first_level_tagsku_doc = prepare_data(final_product_df, 'first_level', 'tag_sku')
first_level_storename_doc = prepare_data(final_product_df, 'first_level', 'store_name')

first_level_tagsku_keword_di = construct_keywords(first_level_tagsku_doc, 'first_level')
first_level_storename_keyword_di = construct_keywords(first_level_storename_doc, 'first_level')
