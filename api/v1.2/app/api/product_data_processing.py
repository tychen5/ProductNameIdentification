import pandas as pd
import numpy as np
import pickle
import re
import string
from collections import Counter
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import querying, flatten_dict_column

# Replace the following paths with your own paths
data_path = '/path/to/your/data/'

# Load data from pickle files
final_product_df = pickle.load(open(data_path + 'combined_product_df_fillpartlevelna.pkl', 'rb'))
fl_convert_dict = pickle.load(open(data_path + 'pl_mapping.pkl', 'rb'))
overlap_tokens = data_path + 'overlap_badtokens.pkl'
overlap_tokens = pickle.load(open(overlap_tokens, 'rb'))

# Tableau server configuration
tableau_server_config = {
    'my_env': {
        'server': 'https://your-tableau-server-url',
        'api_version': '3.10',
        'personal_access_token_name': 'enter_your_personal_access_token_name',
        'personal_access_token_secret': 'enter_your_personal_access_token_secret',
        'site_name': '',
        'site_url': ''
    }
}

# Connect to Tableau server
conn = TableauServerConnection(tableau_server_config, env='my_env')
conn.sign_in()

# Get views and data from Tableau server
site_views_df = querying.get_views_dataframe(conn)
site_views_detailed_df = flatten_dict_column(site_views_df, keys=['name', 'id'], col_name='workbook')
relevant_views_df = site_views_detailed_df[site_views_detailed_df['workbook_name'] == 'Product Name List']
table_id = relevant_views_df[relevant_views_df['name'] == 'Product SKU and NAME']['id'].to_list()[0]
store_raw_data = querying.get_view_data_dataframe(conn, view_id=table_id)

# Process store data
store_useful_data = store_raw_data[['brand', 'category', 'Sku', 'Name', 'Days_LastSeen', 'anonymous_users']]

# Load and process Shopify data
shopify_export_data_us = data_path + 'products_export_us.csv'
shopify_raw_data = pd.read_csv(shopify_export_data_us)
shopify_data = shopify_raw_data[['Vendor', 'Type', 'Title', 'Handle', 'Variant SKU', 'Published', 'Status', 'Variant Grams', 'Variant Requires Shipping', 'Variant Taxable']]
shopify_data.rename(columns={'Vendor': 'brand', 'Type': 'category', 'Title': 'Name', 'Handle': 'Sku', 'Variant SKU': 'Sku2'}, inplace=True)
useful_data = shopify_data[['brand', 'category', 'Name', 'Sku', 'Sku2']]

# Clean and merge store and Shopify data
useful_data = useful_data.dropna(subset=['brand', 'category', 'Name'], thresh=2)
useful_data1 = useful_data[['brand', 'category', 'Name', 'Sku']]
useful_data1 = useful_data1.dropna(thresh=2)
useful_data2 = useful_data[['brand', 'category', 'Name', 'Sku2']]
useful_data2.rename(columns={'Sku2': 'Sku'}, inplace=True)
useful_data2 = useful_data2.dropna(thresh=2)
useful_data = pd.concat([useful_data1, useful_data2])
store_useful_data = pd.concat([store_useful_data, useful_data])

# Filter bad entries and clean data
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