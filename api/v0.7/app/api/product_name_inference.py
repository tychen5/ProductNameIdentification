import pickle
import re
import html
import difflib
from rapidfuzz import fuzz
import os

# Define the path to the pickle file containing the sensitive information
current_directory = os.path.dirname(__file__)
pkl_path = os.path.join(current_directory, 'api_tuples_data.pkl')

# Load the necessary data from the pickle file
final_product_df, stop_words, en_vocabulary, need_filtered_puncset = pickle.load(open(pkl_path, 'rb'))

def easy_cleansing_doc(doc):
    '''
    Perform basic text cleansing on the input document.
    '''
    # Unescape HTML characters
    doc = html.unescape(doc)
    # Replace newlines with spaces and convert to lowercase
    doc = doc.replace('\n', ' ').lower()
    # Replace tabs and carriage returns with spaces
    doc = doc.replace('\t', ' ').replace('\r', ' ')
    # Replace certain punctuation characters with spaces
    for punc in need_filtered_puncset:
        doc = doc.replace(punc, ' ')
    # Split the document into a list of words
    doc_li = re.split('_|-|‑|\\|\/|\,| ', doc)
    # Remove any empty strings from the list and join the remaining words with spaces
    doc_li = list(filter(None, doc_li))
    return " ".join(doc_li)

def calc_doc_score(sent_kw, reddit_text):
    '''
    Calculate the score of a given set of keywords against a Reddit post.
    '''
    score = 0
    for kw in sent_kw:
        # Calculate the token set ratio between the Reddit post and the keyword
        s = max(fuzz.token_set_ratio(reddit_text, kw), fuzz.token_set_ratio(kw, reddit_text)) / 100
        if s >= 0.8:
            if ' ' in kw:
                # If the keyword contains a space, it is considered a strong match
                score = score + 1 / 1.8 * (s)
            else:
                if (kw not in stop_words) and (kw not in en_vocabulary):
                    # If the keyword is not a stop word or in the English vocabulary, it is considered a strong match
                    score = score + 1 / 3 * (s)
                elif kw not in stop_words:
                    # If the keyword is not a stop word, it is considered a moderate match
                    score = score + 1 / 3.5 * (s)
                else:
                    # If the keyword is a stop word, it is considered a weak match
                    score = score + 1 / 4 * (s)
    return score

def clean_productline(pl_set):
    '''
    Clean a set of product line names by removing the 'others' category and sorting the names alphabetically.
    '''
    if (len(pl_set) > 1) and ('others' in pl_set):
        pl_set.remove('others')
    return sorted(pl_set)

def merge(l, r):
    '''
    Merge two lists of strings using the difflib library.
    '''
    m = difflib.SequenceMatcher(None, l, r)
    for o, i1, i2, j1, j2 in m.get_opcodes():
        if o == 'equal':
            yield l[i1:i2]
        elif o == 'delete':
            yield l[i1:i2]
        elif o == 'insert':
            yield r[j1:j2]
        elif o == 'replace':
            yield l[i1:i2]
            yield r[j1:j2]

def combine_store_names(sn_li):
    '''
    Combine a list of store names using the merge() function and the difflib library.
    '''
    if len(sn_li) == 1:
        return sn_li[0]
    else:
        sn_li.sort(key=lambda s: len(s), reverse=True) # Sort the list of store names by length, from longest to shortest
        for i, name in enumerate(sn_li):
            if i == 0:
                l = name.lower().split()
                r = sn_li[i + 1].lower().split()
                merged = merge(l, r)
                merged_txt = ' '.join(' '.join(x) for x in merged)
            else:
                l = merged_txt.split()
                r = sn_li[i + 1].lower().split()
                merged = merge(l, r)
                merged_txt = ' '.join(' '.join(x) for x in merged)
            if i + 2 == len(sn_li):
                return merged_txt
                break

def merge_diff_sn(li_str):
    '''
    Merge a list of store names using the difflib library and a similarity threshold.
    '''
    if len(li_str) == 1:
        return li_str[0]
    else:
        all_together = [] # List of lists of strings
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
                    if s.ratio() > 0.8:
                        put_together.append(right)
                        taken_idx.append(j)
                    else:
                        continue
            all_together.append(put_together)
        taken_li = []
        for ali in all_together:
            taken_li.append(combine_store_names(ali))
        return taken_li

def chk_li_empty(li):
    '''
    Check if a list is empty and return a list containing the string 'others' if it is.
    '''
    if isinstance(li, str):
        return [li]
    if len(li) < 1:
        return ['others']
    else:
        return li

def get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.75):
    '''
    Extract the product name, first level, second level, and third level categories from a Reddit post.
    '''
    # Calculate the score for each product in the product dataframe against the Reddit post
    product_df['score'] = product_df['baseline_keywords'].apply(calc_doc_score, args=(reddit_doc,))
    # Filter the product dataframe to only include products with a score above the threshold
    take_df = product_df[product_df['score'] > thr]
    # Replace any NaN values with the string 'others'
    take_df = take_df.fillna('others')
    # Clean the first level, second level, and third level categories
    fl_li = clean_productline(set(take_df['first_level'].tolist()))
    sl_li = clean_productline(set(take_df['second_level'].tolist()))
    tl_li = clean_productline(set(take_df['third_level'].tolist()))
    # Combine the store names for each product
    take_df = take_df[take_df['store_name'].apply(lambda x: type(x) == list)]
    try:
        take_df['merged_sn'] = take_df['store_name'].apply(combine_store_names)
        merged_sn_li = list(set(take_df['merged_sn'].tolist()))
        merged_sn_li.sort(key=lambda s: len(s), reverse=True) # Sort the list of store names by length, from longest to shortest
        sn_li = merge_diff_sn(merged_sn_li)
    except KeyError:
        sn_li = []
    # Create a dictionary containing the product name, first level, second level, and third level categories
    final_di = {}
    final_di['first_level'] = chk_li_empty(fl_li)
    final_di['second_level'] = chk_li_empty(sl_li)
    final_di['third_level'] = chk_li_empty(tl_li)
    final_di['product_name'] = chk_li_empty(sn_li)
    return final_di

def product_name_inference_inhouse(input_post):
    '''
    Perform product name inference on a Reddit post.
    '''
    clean_text = easy_cleansing_doc(input_post)
    return_text = get_product_name_doc(clean_text, final_product_df)
    return return_text

if __name__ == '__main__':
    # Demo TEXT:
    # User Inputs: 需自行先組合標題與內文（input_post = post_title + " " + post_body）
    # input_post = "what should I replace my USG with, UDM, UDMpro or UDR?My USG took a crap today so need a replacement and with the USG basically end of life I am looking at the UDM, the UDMpro or UDR.. I have a basic home network with 1 switch and single AP the network is not complex with a couple of VLANs and some routing rules for an Unraid Box running plex, nextcloud etx. I am leaning towards the UDR but would like to hear some pro's /con's of each"
    input_post = "Protect 2.1.2 crashing"
    # input_post = "I don't know how to buy Camera and what to pick in Camera G3-Instant"
    # input_post = "What's required for port isolation? I've read docs and even opened a support case, but I'm still not