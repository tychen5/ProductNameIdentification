# Product Name Inference

This Python script, `product_name_inference.py`, is designed to infer product names from user-generated text, such as Reddit posts. The script processes the input text, cleans it, and then calculates a similarity score for each product name in a pre-defined dataset. Based on these scores, the script returns the most likely product names and their associated categories.

### Features

- Text cleansing and preprocessing
- Fuzzy string matching using RapidFuzz library
- Product name inference based on similarity scores
- Merging and combining store names using difflib library

### Dependencies

- Python 3.x
- RapidFuzz
- difflib (built-in library)
- re (built-in library)
- html (built-in library)
- os (built-in library)
- pickle (built-in library)

### Usage

To use the `product_name_inference.py` script, simply import the `product_name_inference_inhouse` function and pass the input text as an argument:

```python
from product_name_inference import product_name_inference_inhouse

input_post = "Guys, G4 Instants &amp; G4 Bullets available in the store. GO GO GO!"
result = product_name_inference_inhouse(input_post)
print(result)
```

### Functions

The script contains the following functions:

- `easy_cleansing_doc(doc)`: Performs basic text cleansing on the input document.
- `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a given keyword in the Reddit text.
- `clean_productline(pl_set)`: Cleans the product line set by removing 'others' and sorting the remaining items.
- `merge(l, r)`: Merges two lists of strings using the difflib library.
- `combine_store_names(sn_li)`: Combines a list of store names using the `merge()` function and the difflib library.
- `merge_diff_sn(li_str)`: Combines a list of store names using the difflib library and a similarity threshold.
- `chk_li_empty(li)`: Checks if a list is empty and returns a list containing 'others' if it is.
- `get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.94)`: Gets the product name from the Reddit document using the product dataframe and a similarity threshold.
- `product_name_inference_inhouse(input_post)`: Performs product name inference on the input post.

### Dataset

The script uses a pre-defined dataset stored in a pickle file (`api_tuples_data.pkl`). This dataset contains product names, categories, and associated keywords. The dataset is loaded into the script at runtime and used for product name inference.