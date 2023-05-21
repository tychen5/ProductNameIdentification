import pandas as pd
import numpy as np
import pickle
import datetime as dt
import pymongo
import itertools
import re
import string
import html
import inflect
from pandarallel import pandarallel
import difflib
from rapidfuzz import fuzz

# Load final_product_df
final_product_df = pickle.load(open('/path/to/your/data/combined_product_df_fillpartlevelna.pkl', 'rb'))

# Define filters
first_filtered_out = [',', '®', '*']  # in whole doc
second_filter_out = ['multi grey', 'light grey', 'dark grey']  # in whole doc
third_filter_out = ['pack', 'meter', 'meters', 'wood', 'silver', 'fabric', 'concrete', 'brick', 'black', 'marble',
                    'concrete', 'camo', 'grey', 'white', 'xxxl', 'xxl', 'xl', 's', 'm', 'l', 'gra', 'blu', 'dig',
                    '8m', '5m', '3m', '2m', '1m', '0.3m', '0.5m']  # after cut in whitespaces

# Get all store names
all_sn_li = final_product_df[~final_product_df['store_name'].isna()]['store_name'].tolist()
all_sn_li = list(itertools.chain.from_iterable(all_sn_li))
sorted(set(all_sn_li), reverse=False)

# Preprocess final_product_df
final_product_df['strict_preprocess_doc'] = final_product_df['tag_sku'].apply(lambda x: " ".join(x))


def concate_doc():
    final_product_df['strict_preprocess_doc'] = final_product_df.apply(
        lambda x: concate_doc([x.first_level, x.second_level, x.third_level], x.store_name))


def mongo_to_df(filter_day=7):
    client = pymongo.MongoClient(host='your_host', username='your_username', password='your_password', port=your_port,
                                 authSource='reddit_ui', authMechanism='SCRAM-SHA-1')
    db = client.reddit_ui
    lastweekday = (dt.datetime.today() - dt.timedelta(days=filter_day)).replace(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
    reddit_column = ['subreddit', 'author', 'created_utc', 'full_link', 'link_flair_text', 'title', 'selftext']
    projection = {i: 1 for i in reddit_column}
    projection['_id'] = 0
    prod_collection = db.posts.find({'created_utc': {'$gte': lastweekday}}, projection).sort('created_utc',
                                                                                              pymongo.DESCENDING)
    df = pd.DataFrame(prod_collection)
    return df


reddit_df = mongo_to_df(365)
reddit_df['link_flair_text'].unique()
final_product_df = pickle.load(open('/path/to/your/data/combined_product_df_fillpartlevelna.pkl', 'rb'))


def concate_all_words(col_li):
    final_results = []
    for attr in col_li:
        if type(attr) == str:
            attr = attr.replace('"', '')
            attr = attr.replace('*', '')
            attr_li = re.split(',|/', attr)
            attr_li = set(filter(None, attr_li))
            for at in attr_li:
                at = at.replace('  ', ' ')
                if at[0] == ' ':
                    at = at[1:]
                if at[-1] == ' ':
                    at = at[:-1]
                final_results.append(at)
        elif type(attr) == list:
            for att in attr:
                att = att.replace('"', '')
                att = att.replace('*', '')
                att_li = re.split(',|/', att)
                att_li = set(filter(None, att_li))
                for at in att_li:
                    at = at.replace('  ', ' ')
                    if at[0] == ' ':
                        at = at[1:]
                    if at[-1] == ' ':
                        at = at[:-1]
                    final_results.append(at)
        elif pd.isna(attr):
            pass
        else:
            pass
    fr = final_results.copy()
    for res in final_results:
        if ('camera' in res) or ('uvc' in res):
            text = re.sub('cameras|camera|uvc', '', res)
            text = " ".join(list(filter(None, text.split(' '))))
            fr.append(text)
    return set(fr)


final_product_df['baseline_keywords'] = final_product_df.apply(
    lambda x: concate_all_words([x.second_level, x.third_level, x.tag_sku, x.store_name]), axis=1)


import re
import pandas as pd
import html
from fuzzywuzzy import fuzz
import difflib
from pandarallel import pandarallel

# Dummy variables
need_filtered_puncset = ['dummy_punc1', 'dummy_punc2']
sku_postfix = ['dummy_postfix1', 'dummy_postfix2']
final_product_df = pd.DataFrame()  # Replace with actual DataFrame
reddit_df = pd.DataFrame()  # Replace with actual DataFrame


def clean_tag_sku(ori_text):
    """
    Remove words in (), remove prblm_ start, remove bad words and multiple white spaces for sku/tag.

    Args:
        ori_text (str): Original text to be cleaned.

    Returns:
        set: Cleaned text as a set.
    """
    try:
        text = re.sub(r'\(.*?\)', '', str(ori_text).lower())
    except:
        return ori_text

    for punc in need_filtered_puncset:
        text = text.replace(punc, ' ')

    text_li = re.split(r'_|-|,|/|‑|\n|\.|\&|“|”|’|…| ', text)
    text_li = list(filter(None, text_li))
    text_li = [x for x in text_li if len(x) > 0 and x not in sku_postfix]

    return set(text_li)


def clean_text(text):
    """
    Clean levels name/store name.

    Args:
        text (str): Text to be cleaned.

    Returns:
        set: Cleaned text as a set.
    """
    if pd.isna(text) or str(text) == 'nan':
        return ""

    for punc in need_filtered_puncset:
        text = text.replace(punc, ' ')

    text = text.replace('\n', ' ')
    text_li = re.split(r'_|-|,|\|‑| ', text)
    text_li = list(filter(None, text_li))
    f_text_li = []

    for x in text_li:
        length = len(x)
        if 1 < length < 4:
            f_text_li.append(x.lower())
        elif length >= 4:
            x = x.lower()
            try:
                w = pl_si.singular_noun(x)
            except IndexError:
                f_text_li.append(x)
            if w == False:
                f_text_li.append(x)
            else:
                f_text_li.append(w)

    return set(f_text_li)


def easy_cleansing_doc(doc):
    """
    Clean document by replacing newlines and other characters.

    Args:
        doc (str): Document to be cleaned.

    Returns:
        str: Cleaned document.
    """
    doc = doc.replace('\n', ' ').lower()
    doc = doc.replace('\t', ' ')
    doc = doc.replace('\r', ' ')

    for punc in need_filtered_puncset:
        doc = doc.replace(punc, ' ')

    doc_li = re.split(r'_|-|‑|\\|\/|\,| ', doc)
    doc_li = list(filter(None, doc_li))

    return " ".join(doc_li)


def reddit_cleansing(title, selftext):
    """
    Clean Reddit data using data cleansing functions mentioned above.

    Args:
        title (str): Reddit post title.
        selftext (str): Reddit post selftext.

    Returns:
        tuple: Tuple containing cleaned text as a set and cleaned document.
    """
    title = html.unescape(title)
    selftext = html.unescape(selftext)
    title1 = clean_tag_sku(title)
    title2 = clean_text(title)
    body1 = clean_tag_sku(selftext)
    body2 = clean_text(selftext)
    all_set = set().union(*[title1, title2, body1, body2])
    title_doc = easy_cleansing_doc(title)
    body_doc = easy_cleansing_doc(selftext)

    return all_set, title_doc + ' ' + body_doc


reddit_df[['clean_text_set', 'clean_text_doc']] = reddit_df.apply(
    lambda x: reddit_cleansing(x.title, x.selftext), axis=1, result_type='expand')

import difflib
import re
import inflect
from thefuzz import fuzz


def merge_diff_sn(li_str):
    """
    Use diff score to combine names.

    Args:
        li_str (list): List of strings to be combined.

    Returns:
        list: Combined list of strings.
    """
    if len(li_str) == 1:
        return li_str[0]
    else:
        all_together = []  # list of list of strs
        taken_idx = []
        for i, left in enumerate(li_str):
            if i in taken_idx:
                continue
            put_together = [left]
            taken_idx.append(i)
            for j, right in enumerate(li_str):
                if (j in taken_idx) or (j <= i):
                    continue
                s = difflib.SequenceMatcher(lambda x: x == " ", left, right)
                if s.ratio() >= 0.6:
                    put_together.append(right)
                    taken_idx.append(j)
            all_together.append(put_together)
        taken_li = []
        for ali in all_together:
            taken_li.append(combine_store_names(ali))
        return taken_li


def combine_store_names(ali):
    """
    Dummy function to combine store names.

    Args:
        ali (list): List of store names to be combined.

    Returns:
        str: Combined store name.
    """
    # Replace this with your actual implementation
    return "combined_store_name"


# Example usage
li = ['example1', 'example2']
result = merge_diff_sn(li)
print(result)

# Dummy data for testing
final_product_df = {
    'baseline_keywords': [
        'example1',
        'example2',
    ]
}

# Example usage of find_word function
def find_word(s):
    if 'udm' in s:
        return True
    else:
        return False


filtered_df = [item for item in final_product_df['baseline_keywords'] if find_word(item)]
print(filtered_df)