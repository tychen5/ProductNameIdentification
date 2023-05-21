import pickle
import re
import html
import difflib
import os

# Load data from pickle file
current_directory = os.path.dirname(__file__)
pkl_path = os.path.join(current_directory, 'api_tuples_data.pkl')
final_product_df, stop_words, en_vocabulary, need_filtered_puncset = pickle.load(open(pkl_path, 'rb'))

def easy_cleansing_doc(doc):
    '''
    Clean the document by replacing newlines with spaces, converting to lowercase, and removing punctuation.
    '''
    doc = html.unescape(doc)
    doc = doc.replace('\n', ' ').lower()
    for punc in need_filtered_puncset:
        doc = doc.replace(punc, ' ')
    doc_li = re.split('_|-|‑|\\|\/|\,| ', doc)
    doc_li = list(filter(None, doc_li))
    return " ".join(doc_li)

def calc_doc_score(sent_kw, reddit_text):
    '''
    Calculate the score of a document based on the presence of certain keywords.
    '''
    score = 0
    for kw in sent_kw:
        if kw in reddit_text:
            if ' ' in kw:
                score = score + 1/2
            else:
                if (kw not in stop_words) and (kw not in en_vocabulary):
                    score = score + 1/3
                elif kw not in stop_words:
                    score = score + 1/4
                else:
                    score = score + 1/5
    return score

def clean_productline(pl_set):
    '''
    Clean the product line by removing 'others' and sorting the set.
    '''
    if (len(pl_set) > 1) and ('others' in pl_set):
        pl_set.remove('others')
    return sorted(pl_set)

def merge(l, r):
    '''
    Merge two strings using SequenceMatcher.
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
    Combine store names using SequenceMatcher and merge.
    '''
    if len(sn_li) == 1:
        return sn_li[0]
    else:
        sn_li.sort(key=lambda s: len(s), reverse=True)
        for i, name in enumerate(sn_li):
            if i == 0:
                l = name.lower().split()
                r = sn_li[i+1].lower().split()
                merged = merge(l, r)
                merged_txt = ' '.join(' '.join(x) for x in merged)
            else:
                l = merged_txt.split()
                r = sn_li[i+1].lower().split()
                merged = merge(l, r)
                merged_txt = ' '.join(' '.join(x) for x in merged)
            if i+2 == len(sn_li):
                return merged_txt
                break

def merge_diff_sn(li_str):
    '''
    Use diff score to combine names.
    '''
    if len(li_str) == 1:
        return li_str[0]
    else:
        all_together = []
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
                    else:
                        continue
            all_together.append(put_together)
        taken_li = []
        for ali in all_together:
            taken_li.append(combine_store_names(ali))
        return taken_li

def chk_li_empty(li):
    '''
    Check if a list is empty and return 'others' if it is.
    '''
    if isinstance(li, str):
        return [li]
    if len(li) < 1:
        return ['others']
    else:
        return li

def get_product_name_doc(reddit_doc, product_df):
    '''
    Get the product name from a document using the product dataframe.
    '''
    product_df['score'] = product_df['baseline_keywords'].apply(calc_doc_score, args=(reddit_doc,))
    take_df = product_df[product_df['score'] > 0.33]
    take_df = take_df.fillna('others')
    fl_li = clean_productline(set(take_df['first_level'].tolist()))
    sl_li = clean_productline(set(take_df['second_level'].tolist()))
    tl_li = clean_productline(set(take_df['third_level'].tolist()))
    take_df = take_df[take_df['store_name'].apply(lambda x: type(x) == list)]
    try:
        take_df['merged_sn'] = take_df['store_name'].apply(combine_store_names)
        merged_sn_li = list(set(take_df['merged_sn'].tolist()))
        merged_sn_li.sort(key=lambda s: len(s), reverse=True)
        sn_li = merge_diff_sn(merged_sn_li)
    except KeyError:
        sn_li = []
    final_di = {}
    final_di['first_level'] = chk_li_empty(fl_li)
    final_di['second_level'] = chk_li_empty(sl_li)
    final_di['third_level'] = chk_li_empty(tl_li)
    final_di['product_name'] = chk_li_empty(sn_li)
    return final_di

def product_name_inference_inhouse(input_post):
    '''
    Infer the product name from a post.
    '''
    clean_text = easy_cleansing_doc(input_post)
    return_text = get_product_name_doc(clean_text, final_product_df)
    return return_text

if __name__ == '__main__':
    # Demo TEXT:
    # User Inputs: 需自行先組合標題與內文（input_post = post_title + " " + post_body）
    # input_post = "Need a bit of help on getting myself up and running I can't seem to access 192.168.1.1 on my EdgeRouter 4. I tried it with nothing connected just the router on eth0 and the pc.\n\n2. I was able to adopt the unifi switch 8 when I go isp modem/router --&gt; switch (port1) --&gt; pc ( switch port 4). But I can't seem to get internet access. I tried isp modem/router --&gt; PC and I can access the net normally. Anything else I need to enable to get internet?\n\n3. I have 2 unifi AC on the switch 8 using PoE (adopted successfully). Setup done, but my devices can't seem to locate them... when I plug them to the isp modem/router, they seem fine. Did I miss any setup on the switch8?\n\nI'm using an offline unifi controller I have installed from a few years ago if that makes any difference. I hear they are pushing for cloud everything now..."
    # input_post = "I don't know how to buy Camera and what to pick in Camera G3-Instant"
    input_post = "What's required for port isolation? I've read docs and even opened a support case, but I'm still not 100% sure what is required to use the port isolation functionality. I need to isolate wired hosts from one another. The number of hosts will be well over 100, so creating a VLAN per host is not ideal.  Port isolation offers the functionality I'm looking for and I do realize it's isolation per switch - not network wide. Support referenced the link below and at first stated CloudKey or UDM. My follow to them resulted in UDM, but you don't need a Pro switch.  Hence my confusion. https://help.ui.com/hc/en-us/articles/115000166827-UniFi-Guest-Portal-and-Hotspot-System My question is what hardware is actually needed to do this?  Do I need the Pro series switches? Do I need a UDM?  I currently only have a CloudKey, AC AP, and a Pro 24 port in place.  I leverage Sonicwall as my firewall."
    print(product_name_inference_inhouse(input_post))