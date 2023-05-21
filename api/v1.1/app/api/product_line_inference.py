import pickle
import pandas as pd
import html
import string
import re
import inflect
from rapidfuzz import fuzz
import gc, torch, os
import warnings
import transformers
from transformers import pipeline
from torch.utils.data import Dataset
from tqdm.auto import tqdm

transformers.logging.set_verbosity_error()
warnings.simplefilter("ignore")

current_directory = os.path.dirname(__file__)
data_path = './data/'
data_path = os.path.join(current_directory, data_path)

# Replace the following file paths with your own file paths
final_product_df = pd.read_pickle(data_path + 'enter_your_final_product_df_file_path')
fl_convert_dict = pickle.load(open(data_path + 'enter_your_fl_convert_dict_file_path', 'rb'))
new_em_df = pd.read_pickle(data_path + 'enter_your_new_em_df_file_path')
en_vocabulary, stop_words = pickle.load(open(data_path + 'enter_your_en_vocabulary_and_stop_words_file_path', 'rb'))
detect_di_title = pickle.load(open(data_path + 'enter_your_detect_di_title_file_path', 'rb'))
all_names_title = list(detect_di_title.keys())
detect_di_selftext = pickle.load(open(data_path + 'enter_your_detect_di_selftext_file_path', 'rb'))
all_names_selftext = list(detect_di_selftext.keys())
classifier = pickle.load(open(data_path + 'enter_your_classifier_file_path', 'rb'))

# Define constants
bad_puncli = set('\|\\|#|x200b|\*|>|<|\%|\\\\-|\*|*|%|®|tl;dr|x200B|X200b|X200B|& ;|&nbsp;|@UI-'.split('|'))
need_filtered_puncset = set(string.punctuation).union(bad_puncli)
need_filtered_puncset_model = need_filtered_puncset - { '+', '&', '.', "'", "-" }
title_model_lossethr = 0.9688
title_model_strictthr = (0.9936 + 0.9884 + 0.9893) / 3
selftext_model_lossethr = 0.9901
selftext_model_strictthr = (0.9975 + 0.9982) / 2
default_order = ['unifi access', 'unifi talk', 'unifi protect', 'unifi network', 'unifi consoles', 'uisp', 'amplifi', 'unifi connect', 'unifi led']
bad_protect_name_di = {}
bad_protect_name_di['unifi protect'] = ['Netamo', 'Dahua', 'GVM', 'Light2']
need_filtered_puncset = set(string.punctuation) - { '+', '&', '.' }
sku_postfix = ['us', 'ea', 'beta', 'au', 'uk', 'bk', 'bl', 'blk', 'br', 'ca', 'eu', 'in',
               'jp', 'mx', 'tw', 'usa', 'cn', 'grey', 'au', 'black', 'silver', 'blu', 'gra',
               'camo', 'brick']
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"  # dingbats
                           u"\u3030"
                           u"\u2122"
                           u"\u00ae"
                           u"\u2022"
                           "]+", flags=re.UNICODE)
pl_si = inflect.engine()
fmthr_di = {'accessories': 3.0,
            'amplifi': 3.0,
            'uisp': 1.9967,
            'unifi access': 3.0,
            'unifi connect': 3.0,
            'unifi consoles': 1.84,
            'unifi led': 3.0,
            'unifi network': 0.84,
            'unifi protect': 2.0667,
            'unifi talk': 2.13335}
fmthr_dict = {}  # Replace with your own dictionary
for k, v in fmthr_di.items():
    if v < 2.9999:
        fmthr_dict[k] = v

# Define functions

def get_model_res(title_res, thr, detect_di):
    """
    Get model results based on threshold.

    Args:
        title_res: DataFrame containing results.
        thr: Threshold for filtering results.
        detect_di: Dictionary for label conversion.

    Returns:
        model_title_loose_res: List of filtered and converted labels.
    """
    model_title_loose_res = []
    seq = ""

    if len(title_res) > 0:
        seq = title_res.loc[0, 'sequence']
        title_model_loose = title_res[title_res['scores'] >= thr]
        title_model_loose = title_model_loose['labels'].tolist()

        for label in title_model_loose:
            try:
                convert = detect_di[label]
            except KeyError:
                continue

            if convert not in model_title_loose_res:
                model_title_loose_res.append(convert)

    for pl, bad_li in bad_protect_name_di.items():
        for name in bad_li:
            if name.lower() in seq.lower():
                try:
                    model_title_loose_res.remove(pl)
                except ValueError:
                    continue

    return model_title_loose_res


def check_emtitle(li1, li2):
    """
    Check if there exists an intersection between two lists.

    Args:
        li1: First list.
        li2: Second list.

    Returns:
        int: Length of the intersection.
    """
    return len(set(li1).intersection(set(li2)))


def get_intersection(li1, li2, default_order=False):
    """
    Get the intersection of two lists while maintaining the order of the first list.

    Args:
        li1: First list.
        li2: Second list.
        default_order: If True, use the default order.

    Returns:
        list: Intersection of the two lists.
    """
    return sorted(set(li1) & set(li2), key=li1.index)


def intersect_loop(li):
    """
    Get the intersection of a list of lists.

    Args:
        li: List of lists.

    Returns:
        list: Intersection of the lists.
    """
    key = li[0]

    for l in li[1:]:
        intersect_li = get_intersection(key, l)

        if len(intersect_li) > 0:
            return intersect_li
        else:
            continue

    return []

