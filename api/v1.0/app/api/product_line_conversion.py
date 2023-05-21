import itertools
import pandas as pd
import pickle

def convert2pl(flstr):
    """Convert first level string to product line."""
    convert = fl_convert_dict[flstr]
    return convert[0]

useful_dict['productline'] = useful_dict['first_level'].map(convert2pl)

data_path = '/path/to/your/data/'
unifi_li, amplifi_li, uisp_li = pickle.load(open(data_path + 'bigrule_pl.pkl', 'rb'))

othername_path = data_path + 'Product_name_revision.xlsx'
xls = pd.ExcelFile(othername_path)

newadd_name = {}
baddel_name = {}

for i in xls.sheet_names:
    df = pd.read_excel(othername_path, sheet_name=i)
    newadd_name[i] = list(filter(None, df['Name'].tolist()))
    baddel_name[i] = list(filter(None, df['badnames'].tolist()))

detect_di = {}
pl_merge_df = useful_dict[useful_dict['productline'] != 'accessories']

all_detectnames = pl_merge_df['clean_name'].tolist()
all_detectnames.extend(pl_merge_df['clean_sku'].tolist())
all_pls = pl_merge_df['productline'].tolist()

for detectli, pl in zip(all_detectnames, all_pls):
    try:
        addnames = newadd_name[pl]
        addnames = [x for x in addnames if str(x) != 'nan']
        badnames = baddel_name[pl]
        badnames = [x.lower() for x in badnames if str(x) != 'nan']
    except KeyError:
        addnames = []
        badnames = []

    for name in detectli:
        if name.lower() not in badnames:
            detect_di[name] = pl

    for name in addnames:
        if name.lower() not in badnames:
            detect_di[name] = pl

    if pl.lower() not in badnames:
        detect_di[pl] = pl

detect_di['Unifi controller'] = 'unifi consoles'
detect_di['UniFi access point'] = 'unifi network'

pickle.dump(obj=detect_di, file=open('../data/reverse_pn2pl_di.pkl', 'wb'))

store_productname_save_path = data_path + 'productline_keywords_df.pkl'
pl_merge_df = pickle.load(open(store_productname_save_path, 'rb'))

othername_path = data_path + 'Product_name_revision.xlsx'
xls = pd.ExcelFile(othername_path)

li = list(fl_convert_dict.values())
allpl = set(itertools.chain.from_iterable(li))

newadd_name = {}
baddel_name = {}

for i in xls.sheet_names:
    df = pd.read_excel(othername_path, sheet_name=i)
    newadd_name[i] = list(filter(None, df['Name'].tolist()))
    baddel_name[i] = list(filter(None, df['badnames'].tolist()))

detect_di = {}
pl_merge_df = pl_merge_df[pl_merge_df['productline'] != 'accessories']

all_detectnames = pl_merge_df['detect_names2'].tolist()
all_pls = pl_merge_df['productline'].tolist()

for detectli, pl in zip(all_detectnames, all_pls):
    try:
        addnames = newadd_name[pl]
        addnames = [x for x in addnames if str(x) != 'nan']
        badnames = baddel_name[pl]
        badnames = [x.lower() for x in badnames if str(x) != 'nan']
    except KeyError:
        addnames = []
        badnames = []

    for name in detectli:
        if (name.lower() not in badnames) and name.isascii():
            detect_di[name] = pl

    for name in addnames:
        if name.lower() not in badnames:
            detect_di[name.lower()] = pl

    if pl.lower() not in badnames:
        detect_di[pl] = pl

detect_di['unifi controller'] = 'unifi consoles'
detect_di['unifi access point'] = 'unifi network'

pickle.dump(obj=detect_di, file=open(data_path + 'reverse_pn2pl_di_lowercase.pkl', 'wb'))
