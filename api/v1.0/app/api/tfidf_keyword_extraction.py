
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


# Replace the following lines with your actual data
first_level_tagsku_doc = pd.DataFrame()
first_level_storename_doc = pd.DataFrame()
final_product_df = pd.DataFrame()

first_level_tagsku_keword_di = construct_keywords(first_level_tagsku_doc, 'first_level')
first_level_storename_keyword_di = construct_keywords(first_level_storename_doc, 'first_level')
all_keywords = list(first_level_storename_keyword_di.values())
all_keywords.extend(list(first_level_tagsku_keword_di.values()))
all_keywords = list(itertools.chain.from_iterable(all_keywords))
puncs = string.punctuation
keyword_punc = []
for kw in all_keywords:
    for punc in puncs:
        if punc in kw:
            keyword_punc.append(punc)
need_filter_punc = set(puncs) - set(keyword_punc)
need_filter_punc = ''.join(list(need_filter_punc))



final_product_df['first_level'] = final_product_df.apply(lambda x: fill_firstlevel(x.first_level, x.tag_sku, x.store_name,
                                    first_level_tagsku_keword_di, first_level_storename_keyword_di), axis=1)


final_product_df['second_level'] = final_product_df.apply(lambda x: clean_sl(x.second_level, x.tag_sku), axis=1)


final_product_df[['first_level', 'second_level', 'third_level']] = final_product_df.apply(lambda x: fill_secondlevel(x.first_level, x.second_level, x.third_level,
                                                                                            x.tag_sku, x.store_name,
                                                                                            third_level_tagsku_keword_di, third_level_storename_keyword_di), axis=1, result_type='expand')

# Replace the following line with your actual data path
data_path = '/path/to/your/data/'
pickle.dump(file=open(data_path + 'combined_product_df_fillpartlevelna.pkl', 'wb'), obj=final_product_df)
