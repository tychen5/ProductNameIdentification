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

# Load data
final_product_df = pickle.load(open('/path/to/your/data/combined_product_df_fillpartlevelna.pkl', 'rb'))

# Preprocessing
first_filtered_out = [',', '®', '*']
second_filter_out = ['multi grey', 'light grey', 'dark grey']
third_filter_out = ['pack', 'meter', 'meters', 'wood', 'silver', 'fabric', 'concrete', 'brick', 'black', 'marble',
                    'concrete', 'camo', 'grey', 'white', 'xxxl', 'xxl', 'xl', 's', 'm', 'l', 'gra', 'blu', 'dig',
                    '8m', '5m', '3m', '2m', '1m', '0.3m', '0.5m']

all_sn_li = final_product_df[~final_product_df['store_name'].isna()]['store_name'].tolist()
all_sn_li = list(itertools.chain.from_iterable(all_sn_li))
sorted(set(all_sn_li), reverse=False)

final_product_df['strict_preprocess_doc'] = final_product_df['tag_sku'].apply(lambda x: " ".join(x))


def concate_doc():
    final_product_df['strict_preprocess_doc'] = final_product_df.apply(
        lambda x: concate_doc([x.first_level, x.second_level, x.third_level], x.store_name))


def mongo_to_df(filter_day=7):
    client = pymongo.MongoClient(host='your_host', username='your_username', password='your_password', port=your_port,
                                 authSource='your_authSource', authMechanism='your_authMechanism')
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

# Additional preprocessing
fl_names = final_product_df['first_level'].value_counts().index.tolist()
pl_nouns = ['cameras', 'consoles', 'accessories']
pl_si = inflect.engine()
rows = []

import re
import html
from fuzzywuzzy import fuzz
import difflib
from pandarallel import pandarallel


def easy_cleansing_doc(doc):
    """
    Cleanses the input document by removing unnecessary characters and splitting it into words.

    Args:
        doc (str): The input document to be cleansed.

    Returns:
        str: The cleansed document.
    """
    doc = doc.replace('\n', ' ').lower()
    doc = doc.replace('\t', ' ')
    doc = doc.replace('\r', ' ')
    for punc in need_filtered_puncset:
        doc = doc.replace(punc, ' ')
    doc_li = re.split('_|-|‑|\\|\/|\,| ', doc)
    doc_li = list(filter(None, doc_li))
    return " ".join(doc_li)


def reddit_cleansing(title, selftext):
    """
    Cleanses Reddit data using the data cleansing function mentioned above and combines the title and selftext.

    Args:
        title (str): The title of the Reddit post.
        selftext (str): The selftext of the Reddit post.

    Returns:
        tuple: A tuple containing the cleansed data as a set and a combined string of the title and selftext.
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


# Apply the reddit_cleansing function to the Reddit DataFrame
reddit_df[['clean_text_set', 'clean_text_doc']] = reddit_df.apply(
    lambda x: reddit_cleansing(x.title, x.selftext), axis=1, result_type='expand')

# Example Reddit text
reddit_text = """
Researching what router to get for Starlink set up Greetings everyone. So I've gotten my (square) dishy in and initial tests have been going well, but I an keen on getting a 3rd party router in part to start cutting my networking chops and have a better overall performing connection. I have seen glowing remarks for a Ubiquiti set up but I also don't have a need, for now, for a whole mesh set up and what have you. That said my folks talk about adding a tiny house/granny unit so future expansion isn't off the table. For the moment though I'm basically looking for a solid router to connect to Starlink while the Starlink router is in bypass mode.
Initial research pointed towards a AmpliFi Instant Router perhaps, good price, but its looking like its either sold out or potentially even discontinued. Would the next step up then be either a Dream Router (no current plans for using anything that needs that OS/storage to my knowledge) or the AmpliFi Alien Router (bit pricey for me currently) or is there something more reasonably priced that I'm over looking?
The house is about 1700 Square Feet and is spread out rectangular. Our previous provider (haven't cancelled yet) is AT&amp;T with their DSL U-Verse. They replaced the old router/modem within the last few months with a BGW210 though both seemed to reach throughout the house alright. That said being on DSL I can't really say how good the speeds farther out actually were. Believe me I'd love to set up a proper switch and have ethernet strung throughout but this is an older and my folks don't want to be tearing out the walls to be putting ethernet in.
"""

# Example keywords
words = ['g4', "g4 pro’s", "g4 pro's", 'g4 instant', 'protect', 'ptz', 'smart detection',
         'doorbell', 'zoom', 'instant', 'instants', 'flex', 'flexes', 'face recognition',
         'motion detect', 'motion zone', 'zone', 'g4 pro', 'bullet', 'ai bullet', 'detect',
         'detection', 'smart detect', 'motion detection', 'motion', 'person detect', 'package detect',
         'vehicle detect', 'facial recognition', 'object detection', 'protect app', 'motion event',
         'unifi protect', 'g3', 'facial', 'detection', 'g5', 'smart', 'cams', 'person', 'vehicle', 'animal']

# Replace the following variables with your actual data
need_filtered_puncset = set()  # Set of punctuation characters to be filtered
stop_words = set()  # Set of stop words
en_vocabulary = set()  # Set of English vocabulary words

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
            put_together = []
            put_together.append(left)
            taken_idx.append(i)
            for j, right in enumerate(li_str):
                if (j in taken_idx) or (j <= i):
                    continue
                else:
                    s = difflib.SequenceMatcher(lambda x: x == " ", left, right)
                    if s.ratio() >= 0.6:
                        put_together.append(right)
                        taken_idx.append(j)
            all_together.append(put_together)
        taken_li = []
        for ali in all_together:
            taken_li.append(combine_store_names(ali))
        return taken_li


def find_word(s):
    """
    Check if the given word is present in the string.

    Args:
        s (str): String to search for the word.

    Returns:
        bool: True if the word is found, False otherwise.
    """
    if 'udm' in s:
        return True
    else:
        return False


# Example usage
li = ['example1', 'example2']
merged_list = merge_diff_sn(li)
print(merged_list)

# Dummy data for final_product_df
final_product_df = {
    'baseline_keywords': [
        'example1',
        'example2',
        'example3'
    ]
}

# Filter final_product_df based on the find_word function
filtered_final_product_df = [
    item for item in final_product_df['baseline_keywords'] if find_word(item)
]
print(filtered_final_product_df)