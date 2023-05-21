
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

# Replace the following path with the path to your GloVe file
en_vocabulary = load_glove_model('/path/to/your/glove.6B.50d.txt')

# Replace the following path with the path to your stop words file
with open('/path/to/your/stop_words_english.txt', 'r') as file:
    stop_words = file.read().splitlines()

# Replace the following path with the path to your data file
data_path = '/path/to/your/data/'

# Rest of the code
# ...

# Replace the following path with the path to your save file
store_productname_save_path = '/path/to/your/save/file'


def filter_out_bad_set(ori_set, bad_set):
    """
    Filters out bad set from the original set and adjusts token length.

    Args:
        ori_set (set): The original set of tokens.
        bad_set (set): The set of bad tokens to be removed.

    Returns:
        list: The filtered and adjusted set of tokens.
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
    if fl_name == 'unifi cameras':
        all_words.extend(['g4', "g4 pro’s", "g4 pro's", 'g4 instant', 'protect', ' ptz', 'ptz ', 'smart detection',
                          'doorbell', 'zoom', 'instant', 'instants', 'flex', 'flexes', 'face recognition',
                          'motion detect', 'motion zone', 'zone', 'g4 pro', 'bullet', 'ai bullet', 'detect',
                          'detection', 'smart detect', 'motion detection', 'motion', 'person detect', 'package detect',
                          'vehicle detect', 'facial recognition', 'object detection', 'protect app', 'motion event',
                          'unifi protect', 'g3', 'facial', 'detection', 'g5', 'smart', ' cams ', 'person', 'vehicle', 'animal',
                          'g3 instant', 'my cameras', 'playback', 'g3 flex cameras',
                          'g3 instants', 'protect cameras', 'g4 wireless cameras', 'unvr', 'wifi cameras', 'nvr',
                          'g4 pro', 'g4 pros', 'g5 cameras', 'g5 camera', 'g5', 'hd cameras', 'doorbells',
                          'protect systems', 'protect systems', 'grid views', 'camera view', 'unvr pro',
                          'unvr pros', 'g3 micro', 'g3 flexes', 'g4 flexes', 'g5 flexes', 'g4 dome',
                          'g5 dome', 'a g4 dome', 'a g4 bullet', 'g5 bullet', 'g4 pro', 'g5 pro',
                          'g4 pros', 'g4 instants', 'g4 bullets', 'unvr pro came', 'protect doorbell',
                          'protect cameras', 'protect camera', 'g3 bullets', 'g3 bullet', 'g4 flex',
                          'ai flex', 'ai 360', 'ai theta', 'doorbell mechanical chime', 'protect recordings',
                          'recording cameras', 'video camera', 'cameras vehicle', 'ai360'])
    # Add similar conditions for other fl_name values
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
    # Add similar conditions for other fl_name values

import itertools


def construct_detect_di(lilili):
    """Construct a list of unique sets from a list of lists of lists.

    Args:
        lilili (list): A list of lists of lists.

    Returns:
        list: A list of unique sets.
    """
    processed_set = []
    twod_li = list(itertools.chain.from_iterable(lilili))

    for oned_li in twod_li:
        oned_set = set(oned_li)
        if oned_set not in processed_set:
            processed_set.append(oned_set)

    return processed_set


# Replace 'new_em_df' with your actual DataFrame variable
new_em_df['detect_names'] = new_em_df['detect_names'].apply(construct_detect_di)

# Replace '/path/to/your/pickle' with the actual path where you want to save the pickle file
new_em_df.to_pickle('/path/to/your/pickle/em2_detect_df.pkl')